"""M3 acceptance: baryon rule, freeze-out + yields bands, registry, replay.

BUILD0 M3 checklist: n/p freezes in 0.10-0.20 below Lambda_conf; Y_p in
0.20-0.30; X_H in 0.69-0.80; D/H is sub-granularity at this baryon count
and must read exactly zero or land in-band (surprise ledger); the baryon
rule yields exactly two stable charges from the quark multisets; the
channel registry is a pure cache (cache-off runs hash-identical); nuclide
keys are (Z, A) only - no element names anywhere in sim/.
"""

import json
import pathlib

from sim import bind, nucbind
from sim.demo import _yields, run, run_recorded
from sim.log import EventContext
from sim.probe import Probe
from sim.replay import replay_dir

_HERE = pathlib.Path(__file__).resolve().parent


def _run(seed, ticks=2400, cells=8, jump=True):
    ctx = EventContext(seed, mode="off")
    chain, world = run(seed, ticks, cells, ctx,
                       probe=Probe((2, 3)), jump=jump)
    return chain, world


def test_baryon_rule_two_charges_one_carrier():
    baryons = bind.stable_baryons()
    assert sorted({q for q, _ in baryons}) == [0, 1]
    assert len(baryons) == 2
    assert bind.massless_carriers() == ["ph"]


def test_liquid_drop_reproduces_anchors():
    anchors = json.loads(
        (_HERE / "oracle" / "nuc_anchors.json").read_text(encoding="utf-8"))
    for a in anchors["anchors"]:
        got = nucbind.binding(a["Z"], a["A"])
        assert abs(got - a["B"]) < 0.30, (
            f"binding({a['Z']},{a['A']}) = {got:.3f} vs anchor {a['B']}")


def test_stability_rules_shape_the_channels():
    assert not bind.channel_open(1, 1, 1, 1)   # diproton: N-Z drip edge
    assert not bind.channel_open(0, 1, 2, 4)   # n + He4 -> A=5 gap
    assert not bind.channel_open(1, 2, 1, 3)   # d + t -> A=5 gap
    assert not bind.channel_open(0, 1, 1, 3)   # n + t -> past drip edge
    assert bind.channel_open(1, 1, 0, 1)       # p + n -> d
    assert bind.channel_open(1, 2, 1, 2)       # d + d -> He4
    assert bind.channel_open(1, 2, 0, 1)       # d + n -> t
    assert bind.channel_open(1, 3, 1, 1)       # t + p -> He4
    assert bind.channel_open(2, 3, 0, 1)       # He3 + n -> He4


def test_freeze_out_and_yield_bands():
    _chain, world = _run(42)
    st, y = world.stats, _yields(world)
    assert 0.10 <= st["n_p_freeze"] <= 0.20
    assert 0.0 < st["T_freeze_mev"] < 5.0
    assert 0 < st["freeze_out_tick"] < 1246  # freeze precedes bind
    assert 0.20 <= y["Y_p"] <= 0.30
    assert 0.69 <= y["X_H"] <= 0.80
    assert y["D_H"] == 0.0 or 1e-6 <= y["D_H"] <= 5e-4
    assert y["Li_H"] >= 0.0  # record-only (surprise ledger)


def test_nucleons_form_below_lambda_conf():
    _chain, world = _run(7, jump=False)
    st = world.stats
    assert st["nucleons"] >= 1200, "baryon condensation must bind most quarks"
    assert st["nucleons"] == st["neutrons"] + st["protons"]
    assert st["reactions"] > 0
    store = world.store
    quanta_left = int(store.n_s.sum() + store.n_c.sum())
    assert quanta_left <= 2 * 8  # only unpairable per-cell leftovers live on


def test_registry_cache_off_identical_hash(tmp_path):
    ref_dir = tmp_path / "reg-on"
    off_dir = tmp_path / "reg-off"
    ref = run_recorded(42, 2400, 8, ref_dir, probe_cells=(2, 3))
    original = bind.channel

    def clearing_channel(*args):
        bind.clear_registry()
        return original(*args)

    bind.channel = clearing_channel
    try:
        off = run_recorded(42, 2400, 8, off_dir, probe_cells=(2, 3))
    finally:
        bind.channel = original
    assert off["final_hash"] == ref["final_hash"]
    assert replay_dir(ref_dir, quiet=True)
    assert replay_dir(off_dir, quiet=True)


def test_no_element_names_in_sim():
    names = ("helium", "lithium", "deuter", "tritium", "beryllium", "boron")
    root = pathlib.Path(__file__).resolve().parents[1] / "sim"
    offenders = []
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        offenders += [f"{path.name}: {n}" for n in names if n in text]
    assert not offenders, "nuclide layer must speak (Z, A) only"
