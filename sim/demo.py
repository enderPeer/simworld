"""Tick loop (BUILD0 tick order): expand, jump, condense, weak/bind, react
network, collapse (theta batch then probe), hash + flush.

M3 landed: quark species are the eps_b-baked net excess (no thermal
annihilation), weak u<->d conversion freezes out emergently, nucleons bind
below Lambda_conf, and the BBN network runs on registry channels.

Kept importable as the replay driver: run(seed, ticks, cells, ctx, ...) must
stay call-compatible because sim.replay rebuilds runs through it.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from . import atoms
from . import bind
from . import collapse
from . import condense
from . import constants as C
from . import jump as jump_mod
from . import network, weak
from .fields import MASS, N_SPECIES
from .lattice import Lattice
from .log import EventContext
from .probe import Probe
from .quanta import QuantStore
from .state import HashChain

HASH_EVERY = 100
_TWO_PI = 2.0 * math.pi


class World:
    def __init__(self, lat, store, nuc, atom, stats):
        self.lat = lat
        self.store = store
        self.nuc = nuc
        self.atom = atom
        self.stats = stats

    @property
    def t(self):
        return self.lat.t

    @property
    def T(self):
        return self.lat.T


def _annihilate(store, ctx, tick, cell, sp, k):
    """Remove k quanta of one species from a cell, superposed first.

    Returns the number actually removed. Draw count k is fixed regardless of
    pool composition so probe on/off stays stream-aligned.
    """
    r = ctx.draws(tick, "annih", cell=cell, payload=[float(k)], n=k,
                  cause="thermal")
    removed = 0
    pool = store.superposed_pool(cell, sp)
    take = min(k, len(pool))
    for j in range(take):
        idx = min(int(r[j] * len(pool)), len(pool) - 1)
        store.remove_superposed_at(cell, sp, idx)
    removed += take
    if take < k:
        cpool = store.collapsed_pool(cell, sp)
        for j in range(k - take):
            if not cpool:
                break
            idx = min(int(r[take + j] * len(cpool)), len(cpool) - 1)
            store.remove_collapsed_at(cell, sp, idx)
            removed += 1
    return removed


def _np_ratio(store, probe, ncells):
    """Net d/u over unprobed cells: the engine's n/p bookkeeping."""
    u = d = 0
    for c in range(ncells):
        if not probe.covers(c):
            u += store.alive(c, 0)
            d += store.alive(c, 1)
    return d / u if u else 0.0


def run(seed, ticks, cells, ctx, probe=None, jump=True):
    if probe is None:
        probe = Probe()
    lat = Lattice(cells)
    store = QuantStore(lat.n)
    nuc = network.NucStore(lat.n)
    atom = atoms.AtomStore(lat.n)
    chain = HashChain()
    skip_until = np.zeros(lat.n, dtype=np.int64)
    processed_once = np.zeros(lat.n, dtype=bool)
    bound = np.zeros(lat.n, dtype=bool)
    stats = dict(created=0, created_bosons=0, annihilated=0, collapsed_theta=0,
                 collapsed_probe=0, jumps=0, ticks_skipped=0,
                 pop_max_rel_err=0.0, pop_max_rel_err_tick=-1,
                 flips=0, reactions=0, nucleons=0, neutrons=0, protons=0,
                 n_p_freeze=-1.0, T_freeze_mev=-1.0, freeze_out_tick=-1,
                 recomb_events=0, capture_first_tick=-1)

    for tick in range(ticks):
        # 1) expand (analytic; T uniform across cells in Phase 0)
        lat.step(tick)
        T = float(lat.T[0])
        tgts = condense.targets(T)

        # 2) jump: empty cooling cells ride the closed-form cooling curve
        if jump:
            for c in range(lat.n):
                q_at = atoms.jump_quiet(atom, nuc, c, T)
                if store.cell_empty(c):
                    cooled = True
                    quiet = network.jump_quiet(nuc, c, T) and q_at
                elif (weak.frozen(T)
                      and store.alive(c, 0) + store.alive(c, 1) <= 2
                      and not any(store.alive(c, sp)
                                  for sp in range(2, N_SPECIES))):
                    cooled = quiet = (network.jump_quiet(nuc, c, T)
                                       and q_at)
                else:
                    cooled, quiet = False, True
                if jump_mod.eligible(store, probe, c, tick, ticks, skip_until,
                                     True, processed_once, quiet, cooled):
                    skip_until[c] = jump_mod.try_jump(store, lat, ctx, tick,
                                                      c, ticks)
                    stats["jumps"] += 1

        worst = 0.0
        for c in range(lat.n):
            if tick < skip_until[c]:
                stats["ticks_skipped"] += 1
                continue
            processed_once[c] = True

            # 3) condense toward the thermal target (eps_b baked into sampling)
            for sp in range(N_SPECIES):
                need = tgts[sp] - store.alive(c, sp)
                if need > 0:
                    r = ctx.draws(tick, "condense", cell=c,
                                  payload=[float(need)], n=2 * need,
                                  cause="thermal").reshape(need, 2)
                    m = MASS[sp]
                    add = store.add_superposed
                    for j in range(need):
                        add(sp, m + T * r[j, 0], _TWO_PI * r[j, 1], cell=c)
                    stats["created"] += need
                    if sp >= 2:
                        stats["created_bosons"] += need

            # 4) weak u<->d conversion on the free quark rows (parton-level
            #    n<->p); no-ops once the pools drain at confinement.
            stats["flips"] += weak.step(store, ctx, tick, c, T, sub=0)

            # 4b) nucleons condense below Lambda_conf (once per cell)
            if not bound[c] and T < C.LAMBDA_CONF:
                r = (stats["n_p_freeze"] if stats["freeze_out_tick"] >= 0
                     else _np_ratio(store, probe, lat.n))
                p_n = r / (1.0 + r) if r > 0.0 else 0.0
                n_n, n_p, _left = bind.bind_nucleons(store, ctx, tick, c, p_n,
                                                     sub=1)
                if n_n + n_p:
                    nuc.add(c, 0, 1, n_n)
                    nuc.add(c, 1, 1, n_p)
                    stats["nucleons"] += n_n + n_p
                    stats["neutrons"] += n_n
                    stats["protons"] += n_p
                bound[c] = True

            # 5a) BBN network on registry channels
            stats["reactions"] += network.step(nuc, ctx, tick, c, T, sub=2)

            # 5b) atoms: electron capture below the gate; above it the
            #     world is ionized by construction, not by dynamics
            ev = atoms.step(atom, nuc, ctx, tick, c, T, sub=3)
            if ev:
                stats["recomb_events"] += ev
                if stats["capture_first_tick"] < 0:
                    stats["capture_first_tick"] = int(tick)

            # 5c) annihilate surplus back toward target, rate-limited so
            #    the population visibly *tracks* the target (with a band).
            #    Quark species are exempt: they are the eps_b-baked net
            #    excess, pairs are below this slice's bookkeeping.
            for sp in range(2, N_SPECIES):
                surplus = store.alive(c, sp) - tgts[sp]
                if surplus <= 0:
                    continue
                k = surplus - surplus // 2
                removed = _annihilate(store, ctx, tick, c, sp, k)
                if removed:
                    stats["annihilated"] += removed
                    store.interactions[c] += 1
                    # 6a) theta batch on every THETA-th cell interaction
                    stats["collapsed_theta"] += collapse.theta_sweep(
                        store, ctx, tick, c, store.interactions, C.THETA,
                        C.THETA_BATCH)

            # 6b) probe: covered cells collapse everything superposed
            if probe.covers(c):
                stats["collapsed_probe"] += collapse.probe_sweep(
                    store, ctx, tick, c)

            for sp in range(2, N_SPECIES):
                tgt = tgts[sp]
                if tgt >= 100:
                    rel = abs(store.alive(c, sp) - tgt) / tgt
                    if rel > worst:
                        worst = rel

        # weak freeze-out is emergent: the last tick whose per-quark
        # conversion probability still beats the expansion rate
        if stats["freeze_out_tick"] < 0 and weak.frozen(T):
            stats["freeze_out_tick"] = int(tick)
            stats["T_freeze_mev"] = T
            stats["n_p_freeze"] = _np_ratio(store, probe, lat.n)

        if worst > stats["pop_max_rel_err"]:
            stats["pop_max_rel_err"] = worst
            stats["pop_max_rel_err_tick"] = tick

        if (tick + 1) % HASH_EVERY == 0 or tick + 1 == ticks:
            chain.add(tick + 1,
                      lat.columns() + store.columns() + nuc.columns()
                      + atom.columns(),
                      C.PHYSICS_BUILD)

    return chain, World(lat, store, nuc, atom, stats)


def _yields(world):
    tot = world.nuc.totals()
    a_tot = sum(A * int(t) for t, (Z, A) in zip(tot, network.SPECIES))

    def cnt(Z, A):
        return int(tot[network.IDX[(Z, A)]])

    p, d, a4 = cnt(1, 1), cnt(1, 2), cnt(2, 4)
    li = cnt(3, 6) + cnt(3, 7)
    out = {
        "Y_p": (4.0 * a4 / a_tot) if a_tot else 0.0,
        "X_H": (p / a_tot) if a_tot else 0.0,
        "D_H": (d / p) if p else 0.0,
        "Li_H": (li / p) if p else 0.0,
    }
    atom = getattr(world, "atom", None)
    if atom is not None:
        counts = world.nuc.counts
        ncells = counts.shape[1]
        e_free = sum(atom.free_electrons(counts, c) for c in range(ncells))
        q_tot = sum(atom.total_charge(counts, c) for c in range(ncells))

        def neutral(Z, A):
            # spread-filling: nuclei reach full neutrality last
            i = network.IDX[(Z, A)]
            return sum(max(0, int(k) - (Z - 1) * int(n))
                       for k, n in zip(atom.captured[:, i],
                                       world.nuc.counts[i]))

        out.update({
            "X_e": (e_free / q_tot) if q_tot else 0.0,
            "X_neutral": 1.0 - (e_free / q_tot) if q_tot else 0.0,
            "e_free": int(e_free),
            "n_atoms_H": neutral(1, 1),
            "n_atoms_He": neutral(2, 4),
            "n_atoms_Li": neutral(3, 6) + neutral(3, 7),
        })
    return out


def run_recorded(seed, ticks, cells, out_dir, probe_cells=(), jump=True):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    meta = {
        "ticks": int(ticks),
        "cells": int(cells),
        "hash_every": HASH_EVERY,
        "probe_cells": sorted(int(c) for c in probe_cells),
        "jump": bool(jump),
    }
    ctx = EventContext(seed, mode="record", path=out / "run.jsonl.gz",
                       physics_build=C.PHYSICS_BUILD, meta=meta)
    chain, world = run(seed, ticks, cells, ctx,
                       probe=Probe(meta["probe_cells"]), jump=jump)
    ctx.finish(chain.final())
    chain.write(out / "hashes.json")
    st = world.stats
    summary = {
        "seed": int(seed),
        "ticks": int(ticks),
        "cells": int(cells),
        "physics_build": C.PHYSICS_BUILD,
        "t_end_s": world.t,
        "T_end_mev": float(world.T[0]),
        "final_hash": chain.final(),
        "n_superposed": world.store.n_superposed(),
        "n_collapsed": world.store.n_collapsed(),
        "created": st["created"],
        "annihilated": st["annihilated"],
        "collapsed_theta": st["collapsed_theta"],
        "collapsed_probe": st["collapsed_probe"],
        "jumps": st["jumps"],
        "ticks_skipped": st["ticks_skipped"],
        "pop_max_rel_err": st["pop_max_rel_err"],
        "pop_max_rel_err_tick": st["pop_max_rel_err_tick"],
        "probe_cells": meta["probe_cells"],
        "jump": meta["jump"],
        "n_p_freeze": st["n_p_freeze"],
        "T_freeze_mev": st["T_freeze_mev"],
        "freeze_out_tick": st["freeze_out_tick"],
        "recomb_events": st["recomb_events"],
        "capture_first_tick": st["capture_first_tick"],
        "nucleons": st["nucleons"],
        "neutrons": st["neutrons"],
        "protons": st["protons"],
        "flips": st["flips"],
        "reactions": st["reactions"],
        **_yields(world),
    }
    with open(out / "summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sim.demo")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ticks", type=int, default=C.TOTAL_TICKS)
    ap.add_argument("--cells", type=int, default=C.N_CELLS)
    ap.add_argument("--out", type=str, default="runs/demo")
    ap.add_argument("--probe-cells", type=str, default="2,3",
                    help="comma-separated cells to probe; empty disables")
    ap.add_argument("--no-jump", action="store_true")
    args = ap.parse_args(argv)
    probe_cells = tuple(int(x) for x in args.probe_cells.split(",") if x != "")
    summary = run_recorded(args.seed, args.ticks, args.cells, args.out,
                           probe_cells=probe_cells, jump=not args.no_jump)
    for key in ("final_hash", "t_end_s", "T_end_mev", "created",
                "collapsed_theta", "collapsed_probe", "jumps",
                "n_p_freeze", "T_freeze_mev", "freeze_out_tick", "nucleons",
                "neutrons", "protons", "flips", "reactions",
                "Y_p", "X_H", "D_H", "Li_H", "X_neutral", "e_free",
                "capture_first_tick", "n_atoms_H", "n_atoms_He"):
        print(f"{key}: {summary[key]}")
    print(f"written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
