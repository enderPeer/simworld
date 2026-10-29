"""M4 acceptance: atoms emerge by detailed balance (BUILD0 M4 gate).

Gates: capture only below the hydrogenic gate T ~ I, the final ionized
fraction sits at the order of Saha, charge is conserved event by event,
the reverse (photoionization) channel demonstrably fires, jump spans
never straddle the capture window, and the 3400-tick run replays bit
for bit.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from sim import atoms, network
from sim.demo import run_recorded
from sim.log import EventContext

TICKS = 3400


def _tick_T(tick):
    from sim import constants as C
    return C.T0_MEV * C.EXPANSION_RATE ** (-tick / 2.0)


@pytest.fixture(scope="module")
def m4_summary(tmp_path_factory):
    out = tmp_path_factory.mktemp("m4run")
    return run_recorded(42, TICKS, 8, out, probe_cells=(2, 3), jump=True)


def test_capture_only_below_gate(m4_summary):
    s = m4_summary
    tick = s["capture_first_tick"]
    assert 2900 <= tick <= 3050
    # the first capture happens at a temperature at or below the gate,
    # i.e. below "a few times I" - never in the ionizing era
    assert _tick_T(tick) <= atoms.T_GATE * 1.001


def test_final_state_order_of_saha(m4_summary):
    s = m4_summary
    cells = s["cells"]
    q_tot = s["e_free"] / max(s["X_e"], 1e-12)
    N_per_cell = q_tot / cells
    S = atoms.saha_x_e(N_per_cell, s["T_end_mev"])
    # coarse-grained engine freezes over-neutralized (the reverse channel
    # dies with e^{-I/T}); the bar is never far above equilibrium and
    # not more than three e-folds below it
    assert s["X_e"] <= 2.0 * S
    assert s["X_e"] >= S / 8.0
    assert s["X_neutral"] >= 0.9


def test_charge_conserved_per_step():
    ctx = EventContext(5, mode="off")
    nuc = network.NucStore(2)
    atom = atoms.AtomStore(2)
    for c in range(2):
        nuc.add(c, 1, 1, 40)
        nuc.add(c, 2, 4, 8)
        nuc.add(c, 1, 2, 3)
    q = [atom.total_charge(nuc.counts, c) for c in range(2)]
    T = atoms.T_GATE * 0.4
    for t in range(300):
        for c in range(2):
            atoms.step(atom, nuc, ctx, t, c, T, sub=3)
        for c in range(2):
            bound = int(atom.captured[c].sum())
            assert atom.free_electrons(nuc.counts, c) + bound == q[c]
            n_tot = {i: int(nuc.counts[i, c]) for i in range(len(network.SPECIES))}
            for i, (Z, _A) in enumerate(network.SPECIES):
                assert 0 <= int(atom.captured[c, i]) <= Z * n_tot[i]


def test_reverse_channel_fires():
    # just below the gate photoionization is Boltzmann-visible: over a
    # long soak the event count must exceed the net capture count
    ctx = EventContext(9, mode="off")
    nuc = network.NucStore(1)
    atom = atoms.AtomStore(1)
    nuc.add(0, 2, 4, 40)
    net = sum(atoms.step(atom, nuc, ctx, t, 0, atoms.T_GATE / 1.2, sub=3)
              for t in range(2000))
    assert int(atom.captured[0, network.IDX[(2, 4)]]) > 0
    assert net != int(atom.captured[0, network.IDX[(2, 4)]])


def test_jump_never_straddles_capture():
    ctx = EventContext(1, mode="off")
    nuc = network.NucStore(1)
    atom = atoms.AtomStore(1)
    nuc.add(0, 1, 1, 10)
    # a jump at tick 1260 lands at tick 1760, far above the gate
    assert atoms.jump_quiet(atom, nuc, 0, _tick_T(1260))
    # a jump at tick 2260 would land at 2760, inside the capture window
    assert not atoms.jump_quiet(atom, nuc, 0, _tick_T(2260))


def test_no_lithium_atoms(m4_summary):
    assert m4_summary["n_atoms_Li"] == 0


def test_m4_run_replays(tmp_path):
    out = tmp_path / "replay"
    run_recorded(7, TICKS, 8, out, probe_cells=(2, 3), jump=True)
    r = subprocess.run(
        [sys.executable, "-m", "sim.replay", str(out)],
        capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "REPLAY PASS" in r.stdout
