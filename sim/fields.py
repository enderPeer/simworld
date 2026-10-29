"""Field table as data (BUILD0 physics-build 0.1), not branching code.

Five fields. Masses are the constants table; nothing here may hold a
real-world value (oracle discipline) — these are engine units (MeV).
"""

from . import constants as C

# (id, name, rest_mass, spin, charge, couplings)
FIELDS = (
    (0, "q_u", C.M_Q * (1.0 + C.DELTA_FLAVOR), 0.5, +2.0 / 3.0, ("strong", "em")),
    (1, "q_d", C.M_Q, 0.5, -1.0 / 3.0, ("strong", "em")),
    (2, "el", C.M_E, 0.5, -1.0, ("em",)),
    (3, "gl", C.LAMBDA_CONF, 1.0, 0.0, ("strong",)),
    (4, "ph", 0.0, 1.0, 0.0, ("em",)),
)

NAME = {f[0]: f[1] for f in FIELDS}
MASS = {f[0]: f[2] for f in FIELDS}
SPIN = {f[0]: f[3] for f in FIELDS}
CHARGE = {f[0]: f[4] for f in FIELDS}
COUPLINGS = {f[0]: f[5] for f in FIELDS}

N_SPECIES = len(FIELDS)


def degeneracy(species):
    """g = 2s+1."""
    return int(round(2 * SPIN[species] + 1))


def is_fermion(species):
    return SPIN[species] * 2 % 2 == 1
