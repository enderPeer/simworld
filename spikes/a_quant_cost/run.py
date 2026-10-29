"""Spike A — quant cost (BUILD0.md §Spikes). Throwaway; feeds the budget table.

10^6 superposed + 10^4 collapsed quanta in SoA, 10^5 random pair
interactions/tick, 100 ticks, CPU. Pairs come from the engine RNG
(sim.rng.draws) so the counter-RNG cost is inside the measurement.
Target: evolve pass >= 1e7 quanta/s.
"""

import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sim.rng import draws  # engine RNG: the honest cost includes this

N_SUP = 10**6
N_COL = 10**4
N_INT = 10**5
TICKS = 100
SEED = 42
THETA = 12
COOL = 1.0 / 1.01
DT = 1e-8
TWO_PI = 6.283185307179586

rng = np.random.default_rng(1)

species = rng.integers(0, 6, N_SUP, dtype=np.uint8)
energy = rng.uniform(0.1, 1.0, N_SUP)
phase = rng.uniform(0.0, TWO_PI, N_SUP)
icount = np.zeros(N_SUP, dtype=np.uint16)

col_cell = np.zeros(N_COL, dtype=np.uint32)
col_pos = np.empty((N_COL, 3), dtype=np.float64)
col_energy = np.empty(N_COL, dtype=np.float64)
col_fill = 0

evolve_s = []
rng_s = []
interact_s = []
collapse_s = []
batches = 0

for tick in range(TICKS):
    t0 = time.perf_counter()
    energy *= COOL
    phase += TWO_PI * energy * DT
    t1 = time.perf_counter()

    r = draws(SEED, tick, "collide", 2 * N_INT)
    i1 = (r[:N_INT] * N_SUP).astype(np.uint64)
    i2 = (r[N_INT:] * N_SUP).astype(np.uint64)
    t2 = time.perf_counter()

    e = 0.5 * (energy[i1] + energy[i2])
    energy[i1] = e
    energy[i2] = e
    icount[i1] += np.uint16(1)
    icount[i2] += np.uint16(1)
    t3 = time.perf_counter()

    hit = np.flatnonzero(icount >= THETA)
    if hit.size:
        batches += 1
        k = min(hit.size, N_COL - col_fill)
        if k > 0:
            col_cell[col_fill : col_fill + k] = hit[:k] % 8
            col_pos[col_fill : col_fill + k] = rng.uniform(0.0, 1.0, (k, 3))
            col_energy[col_fill : col_fill + k] = energy[hit[:k]]
            col_fill += k
        icount[hit] = 0
        energy[hit] = 0.0
    t4 = time.perf_counter()

    evolve_s.append(t1 - t0)
    rng_s.append(t2 - t1)
    interact_s.append(t3 - t2)
    collapse_s.append(t4 - t3)

mean = lambda xs: sum(xs) / len(xs)
ev = mean(evolve_s)
ri = mean(rng_s)
ia = mean(interact_s)
co = mean(collapse_s)

report = {
    "spike": "A quant cost",
    "config": {
        "superposed": N_SUP,
        "collapsed_capacity": N_COL,
        "interactions_per_tick": N_INT,
        "ticks": TICKS,
        "theta": THETA,
        "collapsed_total": int(col_fill),
        "collapse_batches": batches,
    },
    "cpu": platform.processor() or "unknown",
    "python": platform.python_version(),
    "numpy": np.__version__,
    "evolve_ns_per_quant_per_tick": round(ev / N_SUP * 1e9, 4),
    "evolve_quanta_per_s": round(N_SUP / ev),
    "evolve_target_ge_1e7_quanta_s": bool(N_SUP / ev >= 1e7),
    "rng_index_quanta_pairs_per_s": round(N_INT / ri),
    "interactions_per_s": round(N_INT / ia),
    "interact_ns_per_pair": round(ia / N_INT * 1e9, 4),
    "collapse_ns_per_batch_mean": round(sum(collapse_s) / max(batches, 1) * 1e9, 1),
    "full_tick_s_mean": round(ev + ri + ia + co, 6),
    "notes": (
        "elementwise numpy SoA, no packing changes; scatter collisions "
        "(same index twice in one tick) left benign by design"
    ),
}

out = Path(__file__).resolve().parent / "report.json"
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
