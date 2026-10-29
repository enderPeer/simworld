"""Collapse rules (BUILD0 D4 + M2 acceptance).

- theta rule: each annihilation event in a cell is one logged interaction;
  every THETA-th cumulative interaction collapses THETA_BATCH superposed
  quanta (oldest ids first) with cause 'theta'. Non-stochastic.
- probe: every superposed quantum inside a covered cell collapses on the
  tick it would be superposed, with cause 'probe'; positions/momenta come
  from the 'decay' draw stream so the condense/annih streams stay aligned
  (statistical equivalence, M2 checklist).
"""

import numpy as np

from .log import event_digest


def probe_sweep(store, ctx, tick, cell):
    """Collapse all superposed quanta in a covered cell. Returns count."""
    ids = sorted(store.superposed_ids_in(cell))
    if not ids:
        return 0
    n = len(ids)
    r = ctx.draws(tick, "decay", cell=cell, q=ids, n=6 * n, cause="probe")
    r = r.reshape(n, 6)
    pos = r[:, 0:3] - 0.5
    mom = (r[:, 3:6] - 0.5) * 2.0
    store.collapse_moved(ids, pos, mom)
    return n


def theta_sweep(store, ctx, tick, cell, cell_events, theta, theta_batch):
    """Collapse a theta batch if the cell crossed a threshold. Returns count."""
    v = int(cell_events[cell])
    if v == 0 or v % int(theta) != 0:
        return 0
    ids = store.oldest_superposed_in(cell, theta_batch)
    if not ids:
        return 0
    ctx.event(tick, "collapse", cell=cell, q=ids,
              s=[event_digest(ids, None)], cause="theta")
    store.collapse_moved(ids, np.zeros((len(ids), 3)), np.zeros((len(ids), 3)))
    return len(ids)
