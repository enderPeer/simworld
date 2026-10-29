"""M4 aggregate electron capture with a hydrogenic binding scale (BUILD0).

I = 1/2 alpha_em^2 m_e is computed from configured constants. The binding
for the next capture level is I*q^2 for remaining charge q. One captured-
electron count per nuclide/cell plus spread filling replaces individual
orbital states; free electrons are total nuclear charge minus bound count.
This is a charge ledger, not dynamical electron or photon transport.

Capture and reverse events use a shared fitted prefactor, and saha_x_e
provides an internal equilibrium reference. The implemented kernel does
not guarantee that equilibrium: fully captured species are excluded from
updates, making a completely neutral state absorbing. Above T_GATE no
updates occur; a pre-existing bound population is not reset or ionized.
These limitations are documented rather than changed in this baseline.
"""

import math

import numpy as np

from . import constants as C
from .network import SPECIES

I_MEV = 0.5 * C.ALPHA_EM ** 2 * C.M_E  # hydrogenic ground-state scale
T_GATE = 3.0 * I_MEV                   # updates are allowed at or below 3I
_Z = np.array([Z for Z, _A in SPECIES], dtype=np.int64)


P_BUDGET = 12  # Poisson draws reserved per channel per tick


def _prefactor(T):
    # Effective alpha ~ T^-1/2 law; C_REC sets the per-tick rate scale.
    # A fitted prefactor alone does not establish equilibration accuracy.
    return C.C_REC * math.sqrt(C.T_REC_REF / T) / C.V_CELL


def _lam3(A, T):
    mu = C.M_E * A / (A + 1.0)
    return (mu * T * C.SAHA_PHI_E) ** 1.5


def _prob(rate):
    if rate <= 0.0:
        return 0.0
    return min(0.9, 1.0 - math.exp(-rate))


def _binding(Z, cap):
    q = Z - cap  # hydrogenic anchor: remaining ion charge
    return I_MEV * q * q


class AtomStore:
    def __init__(self, cells):
        self.cells = int(cells)
        # captured[c, i] = electrons bound to nuclide i in cell c, 0..Z*n.
        # Spread-filling: every nucleus reaches capture level cap before
        # any reaches cap+1 (more tightly bound electrons added first), so
        # the scalar count fully determines the level distribution.
        self.captured = np.zeros((self.cells, len(SPECIES)), dtype=np.int64)

    def free_electrons(self, nuc_counts, cell):
        z_nuc = _Z * nuc_counts[:, cell]
        return int(z_nuc.sum() - self.captured[cell].sum())

    def total_charge(self, nuc_counts, cell):
        return int((_Z * nuc_counts[:, cell]).sum())

    def columns(self):
        return [self.captured.reshape(-1).astype(np.float64)]


def step(atom, nuc, ctx, tick, cell, T, sub=3):
    """Update partial capture levels and return the number of events.

    Fully captured species are skipped below as well as above the gate.
    That prevents reverse events from a fully neutral initial state; tests
    of partial-state reverse events do not establish global reversibility.
    """
    if T > T_GATE:
        return 0
    counts = nuc.counts[:, cell]
    channels = []
    for i, (Z, A) in enumerate(SPECIES):
        n_tot = int(counts[i])
        if Z == 0 or n_tot <= 0 or int(atom.captured[cell, i]) >= Z * n_tot:
            continue
        channels.append((i, _binding(Z, int(atom.captured[cell, i]) // n_tot),
                         A))
    e_free = atom.free_electrons(nuc.counts, cell)
    if not channels or (e_free <= 0 and not any(
            int(atom.captured[cell, c[0]]) % int(counts[c[0]])
            for c in channels)):
        return 0
    f = _prefactor(T)
    m = len(channels)
    r = ctx.draws(tick, "react", cell=cell, sub=sub, n=m * (1 + P_BUDGET),
                  payload=[float(m), float(T), float(e_free)], cause="atoms")
    events = 0
    for j, (i, B, A) in enumerate(channels):
        n_tot = int(counts[i])
        cap = int(atom.captured[cell, i]) // n_tot
        if e_free > 0:
            # Knuth in log space; the mean re-thins off the committed
            # state, so budget exhaustion never wedges the channel
            k, acc = 0, 0.0
            for s in range(P_BUDGET):
                acc += -math.log(1.0 - r[m + j + m * s])
                if acc >= (n_tot * (cap + 1) - atom.captured[cell, i]
                           - k) * f * e_free:
                    break
                atom.captured[cell, i] += 1
                e_free -= 1
                k += 1
            events += k
        m_up = int(atom.captured[cell, i]) % n_tot  # ions one level up
        if m_up > 0 and r[j] < _prob(
                m_up * f * _lam3(A, T) * math.exp(-B / T)):
            atom.captured[cell, i] -= 1
            events += 1
    return events


def jump_quiet(atom, nuc, cell, T, span=C.JUMP_SPAN):
    """No atomic channel may fire during a jump span. Capture rates grow
    as the cell cools, so the worst case is the landing temperature: if
    the span crosses T_GATE at all, atoms are not quiet."""
    T_land = T * C.EXPANSION_RATE ** (-span / 2.0)
    return T_land >= T_GATE


def saha_x_e(N, T):
    """Closed-form Saha ionized fraction for hydrogen at total density N.

    Charge-neutral solution of (1 - x)/x = N x e^{I/T} / lam3, i.e.
    N L x^2 + x - 1 = 0 with L = e^{I/T} / lam3.
    """
    if T > T_GATE:
        return 1.0
    L = math.exp(I_MEV / T) / _lam3(1, T)
    K = N * L
    if K <= 0.0:
        return 1.0
    return (math.sqrt(1.0 + 4.0 * K) - 1.0) / (2.0 * K)
