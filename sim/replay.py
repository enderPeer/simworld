"""python -m sim.replay <run-dir>: re-run recorded at <dir>, validate the log
bit-for-bit, and compare the hash chain. BUILD0 M0: replay validates causes.
"""

import argparse
import gzip
import json
import sys
from pathlib import Path

from . import constants as C
from .demo import run
from .log import EventContext, LogError
from .state import HashChain


def replay_dir(run_dir, quiet=False):
    run_path = Path(run_dir)
    log_path = run_path / "run.jsonl.gz"
    with gzip.open(log_path, "rt", encoding="utf-8") as fh:
        header = json.loads(fh.readline())
    if header.get("physics_build") != C.PHYSICS_BUILD:
        raise LogError(
            f"physics_build mismatch: log {header.get('physics_build')} != code {C.PHYSICS_BUILD}")
    meta = header["meta"]
    ctx = EventContext(header["seed"], mode="verify", verify_path=log_path,
                       physics_build=C.PHYSICS_BUILD, meta=meta)
    from .probe import Probe
    chain, _world = run(header["seed"], meta["ticks"], meta["cells"], ctx,
                        probe=Probe(meta.get("probe_cells", ())),
                        jump=meta.get("jump", True))
    ctx.finish(chain.final())
    stored = HashChain.read(run_path / "hashes.json")
    diff = chain.diff(stored)
    if diff is not None:
        raise LogError(f"hash chain diverged at index {diff[0]}: {diff[1]} != {diff[2]}")
    if not quiet:
        print(f"REPLAY PASS: {len(chain.pairs)} hashes, final {chain.final()}")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sim.replay")
    ap.add_argument("run_dir")
    args = ap.parse_args(argv)
    try:
        replay_dir(args.run_dir)
    except LogError as exc:
        print(f"REPLAY FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
