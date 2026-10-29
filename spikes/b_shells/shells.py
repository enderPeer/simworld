"""Shell bookkeeping from Z alone: Madelung aufbau, outer electron, block position.

No element table: orbital order comes from the (n+l, n) rule, block starts
fall out of the aufbau sequence itself. Real IP values live only in
oracle_ips.json (test-oracle side).
"""

import math

RY = 13.6  # eV


def aufbau_order(max_n=7):
    orbs = []
    for n in range(1, max_n + 1):
        for l in range(n):
            orbs.append((n, l))
    return sorted(orbs, key=lambda o: (o[0] + o[1], o[0]))


def fill(z):
    """Return {subshell (n,l): count} for element z by aufbau filling."""
    occ = {}
    left = z
    for n, l in aufbau_order(8):
        cap = 2 * (2 * l + 1)
        take = min(cap, left)
        if take:
            occ[(n, l)] = take
        left -= take
        if left <= 0:
            break
    return occ


def block_starts():
    """First Z at which each (n,l) subshell starts filling, by aufbau."""
    starts = {}
    z = 0
    for n, l in aufbau_order(8):
        if (n, l) not in starts:
            starts[(n, l)] = z + 1
        z += 2 * (2 * l + 1)
    return starts


STARTS = block_starts()
D_START = {n: STARTS[(n, 2)] for n in range(3, 8) if (n, 2) in STARTS}
D_END = {n: STARTS[(n, 2)] + 10 - 1 for n in range(3, 8) if (n, 2) in STARTS}


def d_row(z):
    for n, lo in D_START.items():
        if lo <= z <= D_END[n]:
            return n
    return None


def outer_state(z):
    """(n, l, nshell_count) of the highest-n shell; transition flag."""
    occ = fill(z)
    n = max(k[0] for k in occ)
    l = max(k[1] for k in occ if k[0] == n)
    count = sum(c for (nn, ll), c in occ.items() if nn == n)
    return n, l, count


def features(z):
    """Features for the per-l plane fit: n, row position, class l, transition."""
    n, l, count = outer_state(z)
    trans = d_row(z)
    if trans is not None:
        l_class = 2  # d class owns transition metals
        l_d, _ = STARTS[(trans, 2)], None
        pos = z - STARTS[(trans, 2)]
        return {"n": n, "l_class": l_class, "pos": pos, "transition": True}
    if l == 3:
        l_class = 3
        pos = z - STARTS[(n, 3)] if (n, 3) in STARTS else 0
    elif l == 2:
        l_class = 2
        pos = z - STARTS[(n, 2)]
    elif l == 1:
        l_class = 1
        pos = z - STARTS[(n, 1)]
    else:
        l_class = 0
        pos = z - STARTS[(n, 0)]
    return {"n": n, "l_class": l_class, "pos": pos, "transition": False}


def y_of(ip, n):
    """Hydrogenic effective-n inverse: y = sqrt(IP/Ry) * n_outer."""
    return math.sqrt(ip / RY) * n


def hydrogenic(z, n):
    return RY * z * z / (n * n)
