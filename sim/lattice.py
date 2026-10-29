"""8-cell periodic ring with a shared analytic expansion (radiation era).

T ∝ 1/a, a ∝ t^(1/2). Pure closed form in M0; jump-state and per-cell
deviations arrive in M2.
"""

import numpy as np

from . import constants as C


class Lattice:
    def __init__(self, n_cells=None):
        self.n = C.N_CELLS if n_cells is None else int(n_cells)
        self.T = np.full(self.n, C.T0_MEV, dtype=np.float64)
        self.t = C.T0_S

    def step(self, tick, expansion_rate=C.EXPANSION_RATE, t0_mev=C.T0_MEV):
        self.t = C.time_at(tick, expansion_rate)
        self.T[:] = C.temperature(self.t, t0_mev)

    def columns(self):
        return [self.T]
