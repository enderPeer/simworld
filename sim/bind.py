"""Structural baryon rules, channel cache and effective nucleon formation.

The baryon enumerator explicitly selects mixed-flavor triples with charge
0 or +1. This is an imposed stability rule, not a force calculation.
Reaction eligibility combines fitted binding differences with additional
mass-number and charge-balance filters. The registry memoizes those rules;
clearing the cache recomputes the same eligibility values.

Below Lambda_conf the driver consumes available quanta in triples and
samples neutron/proton labels from the frozen weak ratio. The consumed
flavors need not match the sampled label. This "sea completion" is a
documented approximation, not a conservation proof for constituent charge
or a dynamical treatment of confinement and emitted binding energy.
"""

import itertools

from . import nucbind
from .fields import CHARGE, FIELDS, MASS

QUARK_IDS = (0, 1)


def _quark_name(sid):
    return FIELDS[sid][1]


def stable_baryons():
    """Enumerate the two allowed charges under the baseline's explicit rule."""
    out = []
    for combo in itertools.combinations_with_replacement(QUARK_IDS, 3):
        if len(set(combo)) < 2:
            continue  # assumed exclusion of single-flavor triples
        q = round(sum(CHARGE[s] for s in combo))
        if q in (0, 1):
            out.append((q, tuple(_quark_name(s) for s in combo)))
    return sorted(out)


def massless_carriers():
    return [f[1] for f in FIELDS if f[2] == 0.0]


# -- channel registry (pure cache) ----------------------------------------

_REGISTRY = {}


def _unbound(Zs, As):
    """Apply imposed exclusions beyond the fitted liquid-drop expression.

    The mass-5 gap and |N-Z| <= 1 window shape available channels directly;
    they should not be reported as predictions of the binding fit alone.
    """
    Ns = As - Zs
    return As == 5 or abs(Ns - Zs) > 1


def channel(Z1, A1, Z2, A2):
    key = ((Z1, A1), (Z2, A2)) if (Z1, A1) <= (Z2, A2) else ((Z2, A2), (Z1, A1))
    hit = _REGISTRY.get(key)
    if hit is not None:
        return hit
    (Za, Aa), (Zb, Ab) = key
    Zs, As = Za + Zb, Aa + Ab
    gap = -1.0 if _unbound(Zs, As) else (
        nucbind.binding(Zs, As) - nucbind.binding(Za, Aa)
        - nucbind.binding(Zb, Ab))
    _REGISTRY[key] = gap
    return gap


def channel_open(Z1, A1, Z2, A2):
    return channel(Z1, A1, Z2, A2) > 0.0


def clear_registry():
    _REGISTRY.clear()


def registry_size():
    return len(_REGISTRY)


# -- nucleon formation ------------------------------------------------------

def bind_nucleons(store, ctx, tick, cell, p_neutron, sub=1):
    """Consume confined quanta in triples below Lambda_conf.

    Returns (n_neutrons, n_protons, n_quanta_left). Labels are drawn from
    the frozen weak ratio; triples consume any available flavors (sea
    completion). No explicit emitted carrier or binding-energy deposit is
    tracked here; the background bath and reaction weights are effective
    inputs to this demonstration rather than a closed energy calculation.
    """
    pu, pd = store.superposed_pool(cell, 0), store.superposed_pool(cell, 1)
    cu, cd = store.collapsed_pool(cell, 0), store.collapsed_pool(cell, 1)
    total = len(pu) + len(pd) + len(cu) + len(cd)
    n_bar = total // 3
    r = ctx.draws(tick, "react", cell=cell, sub=sub, n=n_bar,
                  payload=[float(p_neutron)], cause="bind",
                  event="draw.react@1/bind")
    neutrons = 0
    for j in range(n_bar):
        for _ in range(3):
            _pop_any(store, cell)
        if r[j] < p_neutron:
            neutrons += 1
    left = (len(pu) + len(pd) + len(cu) + len(cd))
    return neutrons, n_bar - neutrons, left


def _pop_any(store, cell):
    for sp in (1, 0):
        pool = store.superposed_pool(cell, sp)
        if pool:
            store.remove_superposed_at(cell, sp, len(pool) - 1)
            return
        cpool = store.collapsed_pool(cell, sp)
        if cpool:
            store.remove_collapsed_at(cell, sp, len(cpool) - 1)
            return
