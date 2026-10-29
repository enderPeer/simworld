"""M2 acceptance: thermal tracking, probe semantics, statistical equivalence.

BUILD0 M2 checklist: population tracks the thermal target within a band;
probe-covered cells collapse first and theta collapse stays a trickle
(>=99% of unprobed quanta end superposed); reaction statistics are
statistically equivalent probe on/off over 20 seeds.
"""

import json

import pytest

from sim import constants as C
from sim import condense
from sim.demo import run, run_recorded
from sim.log import EventContext, read_entries
from sim.probe import Probe


def _off_run(seed, ticks, cells, probe_cells=(), jump=False):
    ctx = EventContext(seed, mode="off")
    chain, world = run(seed, ticks, cells, ctx,
                       probe=Probe(probe_cells), jump=jump)
    return chain, world


def test_population_tracks_thermal_target():
    _chain, world = _off_run(42, 900, 8)
    st = world.stats
    assert st["created"] > 100_000, "hot start must materialize"
    assert 0.0 < st["pop_max_rel_err"] < 0.10, (
        f"max deviation {st['pop_max_rel_err']:.3f} outside 10% band "
        f"(tick {st['pop_max_rel_err_tick']})")


def test_tick_zero_fill_equals_target():
    tgts = condense.targets(C.T0_MEV)
    expected = 8 * sum(tgts)
    _chain, world = _off_run(7, 1, 8)
    assert world.stats["created"] == expected


def test_probe_collapses_first_theta_trickle(tmp_path):
    out = tmp_path / "probe-on"
    summary = run_recorded(7, 200, 8, out, probe_cells=(2, 3), jump=False)
    entries = [e for e in read_entries(out / "run.jsonl.gz")
               if e.get("k") not in ("header", "end")]
    probes = [e for e in entries if e.get("cause") == "probe"]
    thetas = [e for e in entries if e.get("cause") == "theta"]
    assert probes, "probe cells must collapse quanta"
    # Since M3 the probe also catches the odd later refill (weak-depleted
    # quark rows re-condense), but the tick-0 fill must stay dominant.
    assert all(e["cell"] in (2, 3) for e in probes)
    t0 = sum(len(e["q"]) for e in probes if e["t"] == 0)
    assert t0 >= 0.99 * sum(len(e["q"]) for e in probes)
    assert thetas, "theta rule must fire somewhere unprobed"
    assert min(e["t"] for e in probes) < min(e["t"] for e in thetas)
    assert all(e["cell"] not in (2, 3) for e in thetas)
    unprobed_created = summary["created"] - summary["collapsed_probe"]
    assert summary["collapsed_theta"] <= 0.01 * unprobed_created


class CountingContext(EventContext):
    """mode='off' context that tallies stochastic draws and events by kind."""

    def __init__(self, seed):
        super().__init__(seed, mode="off")
        self.calls = {}
        self.total = {}
        self.events = {}

    def draws(self, tick, kind, **kw):
        n = kw.get("n")
        if n is None:
            p = kw.get("payload")
            n = len(p) if p is not None else len(kw.get("q", ()))
        self.calls[kind] = self.calls.get(kind, 0) + 1
        self.total[kind] = self.total.get(kind, 0) + n
        return super().draws(tick, kind, **kw)

    def event(self, tick, kind, **kw):
        self.events[kind] = self.events.get(kind, 0) + 1
        return super().event(tick, kind, **kw)


def _counts(seed, probe_cells):
    ctx = CountingContext(seed)
    _chain, world = run(seed, 6, 4, ctx, probe=Probe(probe_cells), jump=False)
    return ctx, world


@pytest.mark.parametrize("seed", range(20))
def test_probe_statistical_equivalence(seed, monkeypatch):
    monkeypatch.setattr(C, "V_CELL", 0.002)
    ctx_off, w_off = _counts(seed, ())
    ctx_on, w_on = _counts(seed, (2, 3))
    # M3 scoping: weak u<->d acts on superposed rows only, so a probe
    # collapsing quark rows legitimately changes the flavor sector (flip
    # draws and target refills). Statistical equivalence is asserted on
    # the thermal boson sector, where the probe must stay inert.
    assert ctx_off.calls["annih"] == ctx_on.calls["annih"]
    assert ctx_off.total["annih"] == ctx_on.total["annih"]
    assert w_off.stats["created_bosons"] == w_on.stats["created_bosons"]
    assert w_off.stats["annihilated"] == w_on.stats["annihilated"]
    assert ctx_off.total.get("decay", 0) == 0
    assert ctx_on.total.get("decay", 0) > 0


def test_probe_cells_never_jump(tmp_path):
    out = tmp_path / "jump-probe"
    summary = run_recorded(42, 2400, 8, out, probe_cells=(2, 3))
    assert summary["jumps"] >= 1
    jumps = [e for e in read_entries(out / "run.jsonl.gz")
             if e.get("k") == "jump"]
    assert jumps and all(e["cell"] not in (2, 3) for e in jumps)
