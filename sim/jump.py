"""Jump-state (BUILD0 D5 + M2): analytic propagation for empty cooling cells.

A cell with no live quanta, outside the probe, and with a full JUMP_SPAN
still ahead propagates by closed form: cooling is analytic already, and an
empty cell has nothing to annihilate, so the jump is exactly one `jump`
log entry plus skipping the cell's physics loop. Materialization after
landing just condenses straight to the (lower) target at the landing tick.
"""

from . import constants as C
from .log import event_digest


def eligible(store, probe, cell, tick, ticks, skip_until, jump_on,
             processed_once, nuc_quiet=True, cooled=False):
    """Only cells that were once alive and have cooled empty may jump;
    pristine empty cells (tick 0) must materialize the hot start first.
    Since M3 a cell also needs a quiet nuclide network: every open channel
    must sit below jump_max_prob over the whole span, or the skipped ticks
    would hide real reactions. `cooled` lets a cell count as empty when its
    only residents are the inert quark leftovers of baryon condensation
    (<= 2 quanta: unpairable, weak-frozen, and below this slice's
    annihilation bookkeeping)."""
    if not jump_on:
        return False
    if not processed_once[cell]:
        return False
    if int(skip_until[cell]) > tick:
        return False
    if tick + C.JUMP_SPAN >= ticks:
        return False
    if probe.covers(cell):
        return False
    if not nuc_quiet:
        return False
    return store.cell_empty(cell) or cooled


def try_jump(store, lat, ctx, tick, cell, ticks):
    """Log the jump and return the landing tick, else None."""
    t_land = C.time_at(tick + C.JUMP_SPAN)
    T_land = C.temperature(t_land)
    ctx.event(tick, "jump", cell=cell, q=(),
              s=[event_digest((), [T_land])], cause="thermal")
    return tick + C.JUMP_SPAN
