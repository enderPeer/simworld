"""M2 acceptance: jump-state empty cooling cells vs full-tick reference.

BUILD0 M2: 1000x jump on empty cooling cells; temperature must agree with
the full-tick reference within 0.1%; the replayed summary must match.
"""

import json

from sim.demo import run_recorded
from sim.replay import replay_dir


def test_jump_matches_full_tick_reference(tmp_path):
    ref_dir = tmp_path / "reference"
    jmp_dir = tmp_path / "jumping"
    ref = run_recorded(11, 2400, 8, ref_dir, probe_cells=(), jump=False)
    jmp = run_recorded(11, 2400, 8, jmp_dir, probe_cells=(), jump=True)

    # jump must be observationally transparent: identical sampled states
    assert ref["final_hash"] == jmp["final_hash"]
    assert abs(jmp["T_end_mev"] - ref["T_end_mev"]) <= 1e-3 * ref["T_end_mev"]
    assert jmp["t_end_s"] == ref["t_end_s"]

    assert jmp["jumps"] >= 1
    assert jmp["ticks_skipped"] == 1000 * jmp["jumps"]
    assert jmp["created"] == ref["created"]
    assert 0.0 < ref["pop_max_rel_err"] < 0.10
    assert 0.0 < jmp["pop_max_rel_err"] < 0.10

    assert replay_dir(ref_dir, quiet=True)
    assert replay_dir(jmp_dir, quiet=True)
