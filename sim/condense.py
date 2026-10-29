"""Thermal targets (BUILD0 tick step 3): populations a cell wants at T.

v0 number density: relativistic n = 2*zeta(3)/pi^2 * T^3 (fermions x3/4),
massive suppression f(x) = 1 for x = m/T <= X_REL, else (X_REL/x)*exp(-(x-X_REL))
— continuous at the knee, Boltzmann-like beyond it. Counts per cell scale
with the calibration volume V_CELL. All computed; no tables.
"""

import math

from . import constants as C
from .fields import MASS, N_SPECIES, degeneracy, is_fermion

_ZETA_3 = 1.2020569031595942  # mathematical constant, not an oracle value
_X_REL = 0.5


def _suppression(mass, T):
    if mass <= 0.0:
        return 1.0
    x = mass / T
    if x <= _X_REL:
        return 1.0
    return (_X_REL / x) * math.exp(_X_REL - x)


def target_count(species, T):
    """Expected superposed quanta of one species in one cell at temperature T."""
    if T <= 0.0:
        return 0
    n_unit = 2.0 * _ZETA_3 / (math.pi * math.pi) * T**3
    g = degeneracy(species)
    fac = 0.75 if is_fermion(species) else 1.0
    n = g * fac * _suppression(MASS[species], T) * n_unit
    return int(round(n * C.V_CELL))


def targets(T):
    return [target_count(sp, T) for sp in range(N_SPECIES)]
