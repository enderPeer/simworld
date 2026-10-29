"""Acceptance meta-test: one full run scored against physics_bands.toml.

This is the file nightly CI runs (plus the unit suites). The bands are
the published BUILD0 bands; a failure here means the physics drifted,
not that a helper broke.
"""

import tomllib
from pathlib import Path

import pytest

from sim import atoms
from sim.demo import run_recorded

TOML = Path(__file__).parent / "physics_bands.toml"


def _bands():
    with open(TOML, "rb") as fh:
        return tomllib.load(fh)


@pytest.fixture(scope="module")
def acceptance(tmp_path_factory):
    out = tmp_path_factory.mktemp("bands")
    return run_recorded(42, 3400, 8, out, probe_cells=(2, 3), jump=True)


def test_bands_file_parses():
    b = _bands()
    assert b["nuc"]["Y_p"] == [0.20, 0.30]


def test_nucleosynthesis_bands(acceptance):
    b, s = _bands()["nuc"], acceptance
    assert b["n_p_ratio"][0] <= s["n_p_freeze"] <= b["n_p_ratio"][1]
    assert b["Y_p"][0] <= s["Y_p"] <= b["Y_p"][1]
    assert b["X_H"][0] <= s["X_H"] <= b["X_H"][1]


def test_D_H_zero_or_in_band(acceptance):
    b, s = _bands()["nuc"], acceptance
    if s["D_H"] > 0.0:
        assert b["D_H"][0] <= s["D_H"] <= b["D_H"][1]


def test_atoms_band(acceptance):
    b, s = _bands()["atoms"], acceptance
    assert b["X_neutral"][0] <= s["X_neutral"] <= b["X_neutral"][1]
    S = atoms.saha_x_e(s["e_free"] / s["X_e"] / s["cells"], s["T_end_mev"])
    assert s["X_e"] <= b["X_e_over_saha_max"] * S


def test_jumps_happened(acceptance):
    assert acceptance["jumps"] >= _bands()["jumps"]["min_jumps"]
