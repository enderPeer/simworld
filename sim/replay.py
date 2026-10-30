"""python -m sim.replay <run-dir>: re-run recorded at <dir>, validate the log
bit-for-bit, and compare the hash chain. BUILD0 M0: replay validates causes.
"""

import argparse
import gzip
import json
import sys
from pathlib import Path

from . import constants as C
from . import manifest as manifest_mod
from .demo import run
from .log import EventContext, LogError
from .manifest import ManifestError
from .state import HashChain


def replay_dir(run_dir, quiet=False):
    run_path = Path(run_dir)
    log_path = run_path / "run.jsonl.gz"
    manifest_path = run_path / "manifest.json"
    if not manifest_path.is_file():
        raise LogError(manifest_mod.LEGACY_INSTRUCTION)
    try:
        recorded = manifest_mod.read_manifest(manifest_path)
        manifest_mod.preflight(recorded)
    except ManifestError as exc:
        raise LogError(str(exc)) from None
    expected_digest = manifest_mod.semantic_digest(recorded)
    with gzip.open(log_path, "rt", encoding="utf-8") as fh:
        header = json.loads(fh.readline())
    if header.get("physics_build") != recorded["physics_build"]:
        raise LogError(
            f"physics_build mismatch: log {header.get('physics_build')} != "
            f"manifest {recorded['physics_build']}")
    config = recorded["config"]
    meta = {
        "ticks": config["ticks"],
        "cells": config["cells"],
        "hash_every": config["hash_every"],
        "probe_cells": config["probe_cells"],
        "jump": config["jump"],
    }
    if header.get("meta") != meta:
        raise LogError(
            f"manifest and log header contradict: meta {header.get('meta')!r} != {meta!r}")
    ctx = EventContext(config["seed"], mode="verify", verify_path=log_path,
                       physics_build=C.PHYSICS_BUILD, meta=meta,
                       log_schema=recorded["schemas"]["log"],
                       manifest_digest=expected_digest)
    from .probe import Probe
    chain, _world = run(config["seed"], config["ticks"], config["cells"], ctx,
                        probe=Probe(config["probe_cells"]),
                        jump=config["jump"])
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
    except (LogError, ManifestError) as exc:
        print(f"REPLAY FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
