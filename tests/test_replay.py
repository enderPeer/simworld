import gzip
import json

import numpy as np
import pytest

from sim import constants as C
from sim.demo import run_recorded
from sim.lattice import Lattice
from sim.log import EventContext, LogError, read_entries
from sim.quanta import QuantStore
from sim.replay import replay_dir
from sim.state import HashChain, canonical_hash

TICKS = 200
CELLS = 8


class ToyWorld:
    def __init__(self):
        self.lat = Lattice(CELLS)
        self.store = QuantStore()
        self.chain = HashChain()

    def columns(self):
        return self.lat.columns() + self.store.columns()

    def run(self, ctx, ticks):
        for tick in range(ticks):
            self.lat.step(tick)
            hits = ctx.draws(tick, "collide", cell=0, n=self.lat.n, cause="thermal")
            for c in np.flatnonzero(hits < 0.05):
                qid = self.store.add_superposed(0, float(self.lat.T[c]), 0.0)
                phase = ctx.draws(tick, "condense", cell=int(c), q=[qid], cause="thermal")[0]
                self.store.set_phase(qid, float(phase))
            ids = self.store.superposed_ids()
            if ids:
                rolls = ctx.draws(tick, "decay", cell=0, q=ids, cause="theta")
                victims = [qid for qid, roll in zip(ids, rolls) if roll < 0.002]
                if victims:
                    self.store.collapse(victims, cell=0)
            if (tick + 1) % 20 == 0 or tick + 1 == ticks:
                self.chain.add(tick + 1, self.columns(), C.PHYSICS_BUILD)


def run_toy(seed, mode, tmp_path, name=None, ticks=TICKS):
    meta = {"ticks": ticks, "cells": CELLS}
    path = str(tmp_path / f"{name}.jsonl.gz") if name else None
    ctx = EventContext(seed, mode=mode,
                       path=path if mode == "record" else None,
                       verify_path=path if mode == "verify" else None,
                       physics_build=C.PHYSICS_BUILD, meta=meta)
    world = ToyWorld()
    world.run(ctx, ticks)
    ctx.finish(world.chain.final())
    return world


def test_toy_world_actively_makes_history(tmp_path):
    world = run_toy(42, "record", tmp_path, name="r1")
    assert world.store.n_superposed() > 0
    assert world.store.n_collapsed() > 0
    assert len(world.chain.pairs) == TICKS // 20


def test_fresh_rerun_is_bit_identical(tmp_path):
    a = run_toy(42, "record", tmp_path, name="ra")
    b = run_toy(42, "record", tmp_path, name="rb")
    assert a.chain.pairs == b.chain.pairs
    assert a.store.n_superposed() == b.store.n_superposed()
    assert a.store.n_collapsed() == b.store.n_collapsed()


def test_replay_validates_log(tmp_path):
    recorded = run_toy(42, "record", tmp_path, name="rv")
    replayed = run_toy(42, "verify", tmp_path, name="rv")
    assert replayed.chain.pairs == recorded.chain.pairs


def test_different_seed_diverges(tmp_path):
    a = run_toy(42, "record", tmp_path, name="sa")
    b = run_toy(43, "record", tmp_path, name="sb")
    assert a.chain.final() != b.chain.final()


def test_verify_rejects_tampered_history(tmp_path):
    run_toy(42, "record", tmp_path, name="rt")
    entries = list(read_entries(tmp_path / "rt.jsonl.gz"))
    victim = next(i for i, e in enumerate(entries) if e.get("q"))
    entries[victim]["q"] = [entries[victim]["q"][0] + 1000]
    with gzip.open(tmp_path / "rt-bad.jsonl.gz", "wt", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(json.dumps(entry) + "\n")
    with pytest.raises(LogError):
        run_toy(42, "verify", tmp_path, name="rt-bad")


def test_verify_rejects_shortened_history(tmp_path):
    run_toy(42, "record", tmp_path, name="rl")
    with pytest.raises(LogError):
        run_toy(42, "verify", tmp_path, name="rl", ticks=TICKS - 5)


def test_demo_cli_empty_world_replays(tmp_path, capsys):
    out = tmp_path / "run1"
    summary = run_recorded(42, 240, CELLS, out)
    assert summary["final_hash"]
    assert replay_dir(out, quiet=True) is True
    captured = capsys.readouterr()
    assert "REPLAY PASS" not in captured.out


def test_canonical_hash_is_order_and_build_sensitive():
    col = np.array([1.0, 2.0])
    base = canonical_hash(C.PHYSICS_BUILD, 5, [col])
    assert base == canonical_hash(C.PHYSICS_BUILD, 5, [col.copy()])
    assert base != canonical_hash(C.PHYSICS_BUILD, 6, [col])
    assert base != canonical_hash("0.2", 5, [col])
    assert base != canonical_hash(C.PHYSICS_BUILD, 5, [col[::-1]])
    assert base != canonical_hash(C.PHYSICS_BUILD, 5, [col, col])
