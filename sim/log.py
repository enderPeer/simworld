"""Append-only event records used to verify deterministic re-execution.

Record mode writes compressed JSONL event keys, payload digests and a final
state hash. Verify mode reruns the model, regenerates its counter-based
draws, and checks each event against the next recorded entry. It does not
restore a saved checkpoint or apply an event log as authoritative state.
The replay driver also compares periodic state hashes from state.py.

The intended contract is that stochastic mutations use EventContext.
This class records calls, not arbitrary writes to the underlying stores.
Repeated calls with identical stream coordinates currently reuse draws;
repeatability must therefore be distinguished from statistical independence.
"""

import gzip
import hashlib
import json

import numpy as np

from . import rng


class LogError(RuntimeError):
    pass


def event_digest(q, payload):
    h = hashlib.sha256()
    for qid in q:
        h.update(int(qid).to_bytes(8, "little"))
    if payload is not None:
        arr = np.ascontiguousarray(payload, dtype=np.float64)
        h.update(arr.tobytes())
    return int.from_bytes(h.digest()[:8], "big")


class LogWriter:
    def __init__(self, path, seed, physics_build, meta=None, log_schema=None,
                 manifest_digest=None):
        self.path = str(path)
        self._fh = gzip.open(self.path, "wt", encoding="utf-8", compresslevel=6)
        header = {
            "k": "header",
            "seed": int(seed),
            "physics_build": physics_build,
            "meta": meta or {},
        }
        if log_schema is not None:
            header["log_schema"] = log_schema
        if manifest_digest is not None:
            header["manifest_digest"] = manifest_digest
        self._write(header)

    def _write(self, obj):
        self._fh.write(json.dumps(obj, separators=(",", ":")) + "\n")

    def event(self, tick, kind, cell, q, s, cause):
        self._write({
            "t": int(tick),
            "k": kind,
            "cell": int(cell),
            "kind": rng.entry_kind_hash(kind) & 0xFFFF,
            "q": [int(x) for x in q],
            "s": [int(x) for x in s],
            "cause": cause,
        })

    def end(self, final_hash):
        self._write({"k": "end", "h": final_hash})
        self.close()

    def close(self):
        if self._fh is not None:
            self._fh.close()
            self._fh = None


def read_entries(path):
    with gzip.open(str(path), "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


class EventContext:
    """Modes: 'record' (needs path), 'verify' (needs verify_path + expectations), 'off'."""

    def __init__(self, seed, mode="record", path=None, verify_path=None,
                 physics_build=None, meta=None, log_schema=None, manifest_digest=None):
        if mode not in ("record", "verify", "off"):
            raise LogError(f"unknown mode {mode!r}")
        self.seed = int(seed)
        self.mode = mode
        self._writer = None
        self._events = None
        self._pending = None
        if mode == "record":
            if path is None:
                raise LogError("record mode needs path")
            self._writer = LogWriter(path, seed, physics_build, meta, log_schema,
                                     manifest_digest)
        elif mode == "verify":
            if verify_path is None:
                raise LogError("verify mode needs verify_path")
            entries = list(read_entries(verify_path))
            header, *body = entries
            if header.get("k") != "header":
                raise LogError("log does not start with header entry")
            if int(header.get("seed", -1)) != self.seed:
                raise LogError("replay seed != logged seed")
            if physics_build is not None and header.get("physics_build") != physics_build:
                raise LogError(
                    f"physics_build mismatch: {header.get('physics_build')} != {physics_build}")
            if log_schema is not None and header.get("log_schema") != log_schema:
                raise LogError(
                    f"log_schema mismatch: log {header.get('log_schema')!r} != expected {log_schema!r}")
            if manifest_digest is not None and header.get("manifest_digest") != manifest_digest:
                raise LogError(
                    "log is not bound to the run manifest: header manifest_digest "
                    f"{header.get('manifest_digest')!r} != manifest {manifest_digest!r}")
            if meta is not None and header.get("meta") != meta:
                raise LogError(f"log header meta mismatch: {header.get('meta')!r} != {meta!r}")
            self._end = body[-1] if body and body[-1].get("k") == "end" else None
            self._events = iter(body[:-1] if self._end is not None else body)

    def draws(self, tick, kind, *, cell=0, sub=0, q=(), payload=None, n=None,
              cause="thermal"):
        """Record/verify a draw batch, then generate values at fixed coordinates.

        Payload and IDs enter the event digest, but not the RNG address.
        Calling twice at the same seed/tick/kind/cell/sub restarts the same
        prefix. Distinct species or events need separate addresses before
        independence can be claimed; changing that schema changes replay.
        """
        if n is None:
            n = len(payload) if payload is not None else len(q)
        if n == 0:
            return np.empty(0, dtype=np.float64)
        if n >= 1 << 24:
            raise LogError(f"draw batch too large: {n}")
        s = [event_digest(q, payload)]
        if self.mode == "verify":
            self._check(tick, kind, cell, q, s, cause)
        # Cells and sub-lanes partition the counter range for current sizes.
        # There is no call counter: another batch at this address reuses it.
        start = (int(cell) << 24) + (int(sub) << 48)
        values = rng.draws(self.seed, tick, kind, n, start=start)
        if self.mode == "record":
            self._writer.event(tick, kind, cell, q, s, cause)
        return values

    def event(self, tick, kind, *, cell=0, q=(), s=(), cause="thermal"):
        """Non-stochastic log entry (jump, theta collapse): key-checked in replay."""
        if self.mode == "verify":
            self._check(tick, kind, cell, q, s, cause)
        elif self.mode == "record":
            self._writer.event(tick, kind, cell, q, s, cause)

    def _check(self, tick, kind, cell, q, s, cause):
        try:
            entry = next(self._events)
        except StopIteration:
            raise LogError(
                f"replay produced more events than the log at tick {tick} ({kind})") from None
        expected = {"t": int(tick), "k": kind, "cell": int(cell),
                    "q": [int(x) for x in q], "s": [int(x) for x in s]}
        for key, want in expected.items():
            got = entry.get(key)
            if key == "q":
                got = [int(x) for x in got]
            if got != want:
                raise LogError(
                    f"replay diverged at tick {tick} kind {kind!r}: log has {entry!r}, replay has {expected!r}")
        if (entry.get("kind") & 0xFFFF) != (rng.entry_kind_hash(kind) & 0xFFFF):
            raise LogError(f"replay diverged: kind id mismatch at tick {tick}")
        if cause is not None and entry.get("cause") != cause:
            raise LogError(f"cause mismatch at tick {tick}: {entry.get('cause')!r} != {cause!r}")

    def finish(self, final_hash):
        if self.mode == "record":
            self._writer.end(final_hash)
        elif self.mode == "verify":
            try:
                next(self._events)
            except StopIteration:
                pass
            else:
                raise LogError("replay ended before the log did")
            if self._end is None:
                raise LogError("log has no end entry")
            if self._end.get("h") != final_hash:
                raise LogError(
                    f"final hash mismatch: log {self._end.get('h')} != replay {final_hash}")
