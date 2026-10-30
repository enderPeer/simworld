"""Finite-population nuclear reaction demonstration (BUILD0 tick step 5).

Nuclides are integer counts keyed by (Z, A), within configured bounds.
bind.py supplies channel eligibility from fitted binding and structural
stability rules. Forward weights use population products and a Gamow
factor for charged pairs; the reverse expression uses a calibrated bath
factor and total product binding. No explicit carrier energy is deposited.

These are effective per-tick rules, not an exact continuous-time sampler.
General detailed balance is not established: pairs are enumerated only
when both forward reactants exist, and the reverse coefficient uses total
binding rather than channel Q and omits the forward Gamow factor. These
limitations are retained in physics_build 0.1 for reproducible comparison.
"""

import math

import numpy as np

from . import bind, constants as C, nucbind

_H_RATE = math.log(C.EXPANSION_RATE) / 2.0

SPECIES = [(Z, A) for Z in range(C.NUC_Z_MAX + 1)
           for A in range(1, C.NUC_A_MAX + 1) if Z <= A]
IDX = {k: i for i, k in enumerate(SPECIES)}


class NucStore:
    def __init__(self, cells):
        self.cells = int(cells)
        self.counts = np.zeros((len(SPECIES), self.cells), dtype=np.int64)

    def add(self, cell, Z, A, k=1):
        self.counts[IDX[(Z, A)], cell] += int(k)

    def totals(self):
        return self.counts.sum(axis=1)

    def columns(self):
        return [self.counts.T.reshape(-1).astype(np.float64)]


def _gamow(Zi, Zj, T):
    if Zi == 0 or Zj == 0:
        return 1.0
    return math.exp(-C.GAMOW_G * Zi * Zj / T ** (1.0 / 3.0))


def _rates(nuc, cell, T):
    """Return (i, j, kC, R_fwd, R_rev) in deterministic species order.

    Known limitation: absent forward reactants suppress enumeration of the
    reverse pathway too, even when its product population is nonzero.
    """
    counts = nuc.counts[:, cell]
    out = []
    nch = 0
    for ia in range(len(SPECIES)):
        ni = int(counts[ia])
        if ni <= 0:
            continue
        Zi, Ai = SPECIES[ia]
        for ib in range(ia, len(SPECIES)):
            nj = int(counts[ib])
            if nj <= 0:
                continue
            Zj, Aj = SPECIES[ib]
            Zs, As = Zi + Zj, Ai + Aj
            if As > C.NUC_A_MAX or Zs > C.NUC_Z_MAX:
                continue
            if not bind.channel_open(Zi, Ai, Zj, Aj):
                continue
            nf = ni * (nj - 1) if ia == ib else ni * nj
            kfwd = C.C_CAP * _gamow(Zi, Zj, T) * nf / C.V_CELL
            mu = Ai * Aj / As
            Bc = nucbind.binding(Zs, As)
            krev = (C.C_CAP / C.V_CELL * (Ai * Aj / As)
                    * (mu * T * C.SAHA_PHI) ** 1.5
                    * math.exp(-Bc / T) * int(counts[IDX[(Zs, As)]]))
            out.append((ia, ib, IDX[(Zs, As)], kfwd, krev))
            nch += 1
    return out


def _prob(rate):
    if rate <= 0.0:
        return 0.0
    return min(0.9, 1.0 - math.exp(-rate))


def step(nuc, ctx, tick, cell, T, sub=2):
    """Try at most one forward-or-reverse event per enumerated channel.

    Weights are computed from the pre-step counts; accepted events mutate
    counts sequentially. Capped probabilities and ordering are part of this
    baseline, so both need validation when interpreting physical kinetics.
    """
    ch = _rates(nuc, cell, T)
    if not ch:
        return 0
    r = ctx.draws(tick, "react", cell=cell, sub=sub, n=2 * len(ch),
                  payload=[float(len(ch)), float(T)], cause="network",
                  event="draw.react@1/network")
    counts = nuc.counts[:, cell]
    fired = 0
    for j, (ia, ib, kc, kf, kr) in enumerate(ch):
        if r[2 * j] < _prob(kf) and counts[ia] > 0 and counts[ib] > (1 if ia == ib else 0):
            counts[ia] -= 1
            counts[ib] -= 1
            counts[kc] += 1
            fired += 1
        elif r[2 * j + 1] < _prob(kr) and counts[kc] > 0:
            counts[kc] -= 1
            counts[ia] += 1
            counts[ib] += 1
            fired += 1
    return fired


JUMP_MAX_PROB = 1e-8  # Heuristic per-channel, per-tick quietness threshold.
                      # Nonzero hazard can accumulate over a skipped span.


def jump_quiet(nuc, cell, T):
    """Test current enumerated weights against the quietness threshold.

    This is not a proof of zero event probability over an entire jump.
    Replay comparisons cover selected runs; accumulated hazard and missing
    reverse pathways remain limitations of the general approximation.
    """
    for ia, ib, kc, kf, kr in _rates(nuc, cell, T):
        if _prob(kf) >= JUMP_MAX_PROB or _prob(kr) >= JUMP_MAX_PROB:
            return False
    return True
