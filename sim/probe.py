"""Probe: probe::covers(cell) -> bool (Phase 14 stand-in, BUILD0 D4).

Perception controls render detail, not existence: the probe only *observes*
(its collapses consume the 'decay' draw stream so condense/annihilate
statistics are untouched — the statistical-equivalence test pins this).
"""


class Probe:
    def __init__(self, cells=()):
        self.cells = frozenset(int(c) for c in cells)

    def covers(self, cell):
        return int(cell) in self.cells

    def covered_cells(self, n_cells):
        return [c for c in range(n_cells) if self.covers(c)]
