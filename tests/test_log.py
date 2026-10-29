import gzip
import json

import numpy as np
import pytest

from sim import constants as C
from sim.log import EventContext, LogError, event_digest, read_entries


def _record(path, ticks=5, seed=7):
    ctx = EventContext(seed, mode="record", path=path,
                       physics_build=C.PHYSICS_BUILD, meta={"ticks": ticks})
    out = []
    for tick in range(ticks):
        values = ctx.draws(tick, "react", cell=tick % 3, q=[tick, tick + 1],
                           payload=np.array([tick * 1.5], dtype=np.float64))
        out.append((tick, float(values[0])))
    ctx.finish("final-hash")
    return out


def test_record_read_roundtrip(tmp_path):
    path = tmp_path / "log.jsonl.gz"
    got = _record(path)
    entries = list(read_entries(path))
    assert entries[0]["k"] == "header"
    assert entries[-1] == {"k": "end", "h": "final-hash"}
    events = entries[1:-1]
    assert len(events) == len(got)
    for entry, (tick, _v) in zip(events, got):
        assert entry["t"] == tick
        assert entry["k"] == "react"
        assert entry["q"] == [tick, tick + 1]


def test_verify_clean_log(tmp_path):
    path = tmp_path / "log.jsonl.gz"
    _record(path)
    ctx = EventContext(7, mode="verify", verify_path=path,
                       physics_build=C.PHYSICS_BUILD, meta={"ticks": 5})
    for tick in range(5):
        ctx.draws(tick, "react", cell=tick % 3, q=[tick, tick + 1],
                  payload=np.array([tick * 1.5], dtype=np.float64))
    ctx.finish("final-hash")


def test_verify_rejects_seed_mismatch(tmp_path):
    path = tmp_path / "log.jsonl.gz"
    _record(path)
    with pytest.raises(LogError):
        EventContext(8, mode="verify", verify_path=path,
                     physics_build=C.PHYSICS_BUILD, meta={"ticks": 5})


def test_verify_rejects_tampered_event(tmp_path):
    path = tmp_path / "log.jsonl.gz"
    _record(path)
    entries = list(read_entries(path))
    entries[2]["q"] = [99, 99]
    tampered = tmp_path / "bad.jsonl.gz"
    with gzip.open(tampered, "wt", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(json.dumps(entry) + "\n")
    ctx = EventContext(7, mode="verify", verify_path=tampered,
                       physics_build=C.PHYSICS_BUILD, meta={"ticks": 5})
    with pytest.raises(LogError):
        for tick in range(5):
            ctx.draws(tick, "react", cell=tick % 3, q=[tick, tick + 1],
                      payload=np.array([tick * 1.5], dtype=np.float64))


def test_verify_rejects_early_end(tmp_path):
    path = tmp_path / "log.jsonl.gz"
    _record(path)
    ctx = EventContext(7, mode="verify", verify_path=path,
                       physics_build=C.PHYSICS_BUILD, meta={"ticks": 5})
    for tick in range(4):
        ctx.draws(tick, "react", cell=tick % 3, q=[tick, tick + 1],
                  payload=np.array([tick * 1.5], dtype=np.float64))
    with pytest.raises(LogError):
        ctx.finish("final-hash")


def test_digest_depends_on_payload():
    a = event_digest([1], np.array([1.0]))
    b = event_digest([1], np.array([2.0]))
    c = event_digest([2], np.array([1.0]))
    assert a != b
    assert a != c
    assert a == event_digest([1], np.array([1.0]))
