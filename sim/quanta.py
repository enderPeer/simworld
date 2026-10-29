"""Quant records and population bookkeeping for the reduced micro-seed.

The S/C records are Python dictionaries of lists, with per-cell/species
pool lists and NumPy count arrays. This is not the array-only storage used
by the separate performance spike. Both record sets share one stable ID
space; collapse transfers a record from S to C, and removal deletes it.

"Superposed" and "collapsed" name storage states here, not a many-body
wavefunction representation. Each record has a home cell. The driver keeps
the model's quark excess by exempting quarks from thermal removal; this
store does not derive a matter-antimatter asymmetry. Canonical columns are
sorted by ID before hashing so dictionary insertion order is irrelevant.
"""

import numpy as np

from .fields import N_SPECIES


class QuantStore:
    """Own records, species pools and cached counts; mutate through methods."""

    def __init__(self, cells=8):
        self.cells = int(cells)
        self._next_id = 0
        self._s = {}  # qid -> [species, energy, phase, cell]
        self._c = {}  # qid -> [species, energy, cell, px, py, pz, mx, my, mz]
        self._s_pool = [[[] for _ in range(N_SPECIES)] for _ in range(self.cells)]
        self._c_pool = [[[] for _ in range(N_SPECIES)] for _ in range(self.cells)]
        self.n_s = np.zeros((self.cells, N_SPECIES), dtype=np.int64)
        self.n_c = np.zeros((self.cells, N_SPECIES), dtype=np.int64)
        self.interactions = np.zeros(self.cells, dtype=np.int64)

    # -- creation / ids -------------------------------------------------

    def add_superposed(self, species, energy, phase, cell=0):
        qid = self._next_id
        self._next_id += 1
        sp = int(species)
        c = int(cell)
        self._s[qid] = [sp, float(energy), float(phase), c]
        self._s_pool[c][sp].append(qid)
        self.n_s[c, sp] += 1
        return qid

    # -- inspection ------------------------------------------------------

    def superposed_ids(self):
        return sorted(self._s)

    def collapsed_ids(self):
        return sorted(self._c)

    def n_superposed(self):
        return len(self._s)

    def n_collapsed(self):
        return len(self._c)

    def alive(self, cell, species):
        return int(self.n_s[cell, species] + self.n_c[cell, species])

    def cell_empty(self, cell):
        return int(self.n_s[cell].sum() + self.n_c[cell].sum()) == 0

    def superposed_energy(self, qid):
        return self._s[qid][1]

    def superposed_pool(self, cell, species):
        return self._s_pool[cell][species]

    def collapsed_pool(self, cell, species):
        return self._c_pool[cell][species]

    def superposed_ids_in(self, cell):
        out = []
        for sp in range(N_SPECIES):
            out.extend(self._s_pool[cell][sp])
        return out

    def oldest_superposed_in(self, cell, k):
        best = []
        for sp in range(N_SPECIES):
            pool = self._s_pool[cell][sp]
            if pool:
                best.append(min(pool))
                best.sort()
                best = best[:k]
        return best

    # -- moves and removals ----------------------------------------------

    def set_phase(self, qid, phase):
        self._s[qid][2] = float(phase)

    def collapse(self, ids, cell, pos=(0.0, 0.0, 0.0)):
        """M0 compatibility move: fixed cell/pos, zero momentum."""
        for qid in ids:
            rec = self._s.pop(qid)
            sp, e = rec[0], rec[1]
            c = int(cell)
            self._c[qid] = [sp, e, c, float(pos[0]), float(pos[1]), float(pos[2]),
                            0.0, 0.0, 0.0]
            self._c_pool[c][sp].append(qid)
            self.n_c[c, sp] += 1
            self.n_s[rec[3], sp] -= 1
            pool = self._s_pool[rec[3]][sp]
            pool.remove(qid)

    def collapse_moved(self, ids, pos, mom):
        """Move S -> C at each row's own cell; momentum is scaled by energy.

        pos/mom are (len(ids), 3)-shaped float arrays; momentum rows are
        dimensionless and get multiplied by the quantum's energy on the way
        into the collapsed table. Pool excision is batched per (cell,
        species) so probe sweeps of ~1e5 quanta stay linear.
        """
        pos = np.asarray(pos, dtype=np.float64)
        mom = np.asarray(mom, dtype=np.float64)
        touched = {}
        for j, qid in enumerate(ids):
            rec = self._s.pop(qid)
            sp, e, _phase, c = rec
            self._c[qid] = [sp, e, c,
                            float(pos[j, 0]), float(pos[j, 1]), float(pos[j, 2]),
                            float(mom[j, 0]) * e, float(mom[j, 1]) * e,
                            float(mom[j, 2]) * e]
            self._c_pool[c][sp].append(qid)
            self.n_c[c, sp] += 1
            self.n_s[c, sp] -= 1
            touched.setdefault((c, sp), []).append(qid)
        for (c, sp), moved in touched.items():
            pool = self._s_pool[c][sp]
            if len(moved) <= 8:
                for qid in moved:
                    pool.remove(qid)
            else:
                gone = set(moved)
                pool[:] = [q for q in pool if q not in gone]

    def flip_species(self, qids, cell, old_species, new_species):
        """Weak conversion: rows move species via fresh ids (state change).

        Pool excision is batched so a tick of ~1e2 flips in a ~4e2 pool
        stays linear.
        """
        if not qids:
            return
        for qid in qids:
            rec = self._s.pop(qid)
            self.n_s[cell, old_species] -= 1
            self.add_superposed(new_species, rec[1], rec[2], cell)
        gone = set(qids)
        pool = self._s_pool[cell][old_species]
        pool[:] = [q for q in pool if q not in gone]

    def remove_superposed_at(self, cell, species, idx):
        pool = self._s_pool[cell][species]
        qid = pool[idx]
        pool[idx] = pool[-1]
        pool.pop()
        del self._s[qid]
        self.n_s[cell, species] -= 1
        return qid

    def remove_collapsed_at(self, cell, species, idx):
        pool = self._c_pool[cell][species]
        qid = pool[idx]
        pool[idx] = pool[-1]
        pool.pop()
        del self._c[qid]
        self.n_c[cell, species] -= 1
        return qid

    # -- hashing -----------------------------------------------------------

    def columns(self):
        cols = []
        s_ids = sorted(self._s)
        cols.append(np.array(s_ids, dtype=np.float64))
        for field in range(4):
            cols.append(np.array([self._s[i][field] for i in s_ids],
                                 dtype=np.float64))
        c_ids = sorted(self._c)
        cols.append(np.array(c_ids, dtype=np.float64))
        for field in range(9):
            cols.append(np.array([self._c[i][field] for i in c_ids],
                                 dtype=np.float64))
        cols.append(self.interactions.astype(np.float64))
        return cols
