"""Weak n<->p conversion at the parton level (BUILD0 tick step 5).

While quarks are free (T above Lambda_conf) the effective weak rate
C_w * T^5 converts u <-> d; freeze-out is emergent: when the per-tick
conversion probability drops below the expansion rate the ratio stops
tracking equilibrium, and n/p = exp(-delta/T_freeze) follows with
delta = m_q * delta_flavor, the declared nucleon mass gap (BUILD0: the
flavor split *is* the nucleon mass gap; the neutron side is the
Boltzmann-depleted side of the conversion). The measured ratio is
n/p := (net d quanta)/(net u quanta) over unprobed cells.
"""

import math

from . import constants as C

DM_NP = C.M_Q * C.DELTA_FLAVOR
H_TICK = math.log(C.EXPANSION_RATE) / 2.0  # d ln T / d tick (magnitude)


FLIP_CAP = 0.5  # per-tick ceiling above the tracking regime; the fixed
                # point d/u = exp(-DM_NP/T) is cap-independent


def flip_probs(T):
    """(p_u_to_d, p_d_to_u) per quanta per tick."""
    p = min(FLIP_CAP, C.C_W * T ** 5)
    return p * math.exp(-DM_NP / T), p


def frozen(T):
    return C.C_W * T ** 5 < H_TICK


def step(store, ctx, tick, cell, T, sub=0):
    """One tick of u<->d flips on the superposed rows of one cell.

    Both species are judged against one snapshot of the pools from a
    single draw batch, so the tick is a proper detailed-balance map
    (sequential updates would cascade flip-flops within the tick).
    """
    p_ud, p_du = flip_probs(T)
    if p_du <= 0.0:
        return 0
    pu = store.superposed_pool(cell, 0)
    pd = store.superposed_pool(cell, 1)
    nu, nd = len(pu), len(pd)
    if nu + nd == 0:
        return 0
    r = ctx.draws(tick, "react", cell=cell, sub=sub, n=nu + nd,
                  payload=[float(p_ud), float(p_du)], cause="weak")
    u_ids = [q for j, q in enumerate(pu) if r[j] < p_ud]
    d_ids = [q for j, q in enumerate(pd) if r[nu + j] < p_du]
    store.flip_species(u_ids, cell, 0, 1)
    store.flip_species(d_ids, cell, 1, 0)
    return len(u_ids) + len(d_ids)
