# Phase 1 — Quantum Layer

**Goal:** turn the Phase 0 decisions into a running engine: a quantum layer
that stores quanta, ticks them, collapses them by the observation rule,
correlates them through entanglement, and replays bit-for-bit from
`seed + observation log`.

**Prerequisites (hard gate, from Phase 0):**

- `spec/decisions.md` D1–D5 closed, each with a passing acceptance test.
- Spike C replay harness promoted into `sim/` (it is now CI, not a spike).
- Spike A numbers on disk (ns/quant/tick, CPU and GPU) — the performance
  budget below is derived from them, not guessed.
- `spec/interfaces.md` exists with the Phase 0 → Phase 1 contract line.

**Definition of done:** the micro-seed demo has been refactored into the
real engine; a run advances N ticks, produces collapse statistics that
match theory (blackbody spectrum shape, interference where unobserved,
correct entanglement correlations), stays inside the tick budget, and
replays bit-for-bit from `seed + log`. `sim/` keeps running with **zero**
chemistry, nuclei or planet — just fields, quanta, observation.

---

## Architecture

```
sim/
  core/        tick scheduler: tiers, promotion/demotion, jump-state
  store/       quant SoA blocks per cell per tier (from D1 record)
  fields/      the D2 effective field set + coupling kernels
  collapse/    decoherence-threshold engine (D4) + entanglement graph
  rng/         counter-based per-quant RNG streams (seeded, replayable)
  log/         observation log: append-only, compressed, the spine
  jump/        analytical region summaries (D5)
  probe/       scripted "observer bubble" — stands in for Phase 14
               (seam S21, Phase 14 planning: the gaze-derived
               observation map becomes the world-internal source for
               D4 accounting + tier scheduling; probe::covers stays as
               the test fixture the map must bit-match where they agree)
```

Data rules:

- Quanta are SoA rows in cell blocks. Collapse = tier promotion within the
  block; no allocations in the hot loop, ever.
- Superposed rows carry only `phase, energy, species` (packed); collapsed
  rows gain `cell-coords, refinement tier`. Two arrays, one id space.
- Entanglement is an edge table, not per-quant lists, so the graph can be
  validated (degree, hop count) independently.
- The RNG is counter-based (`hash(seed, quant_id, tick)`) — replay needs no
  RNG state serialization, only the log of what was *observed*.
- **Every state mutation outside superposed-only evolution goes through the
  log writer.** No exceptions, not even tests.

## Work packages

Order matters; W1/W2 parallel, then W3, then W4/W5 parallel.

### W1 — Quant store (implements D1)

- [ ] SoA cell-block layout for both tiers (superposed / collapsed).
- [ ] Pack/unpack round-trip; id ↔ (block, row) addressing.
- [ ] Disk snapshot format + `physics_build` version stamp.
- [ ] Benchmark: ≥ 10⁷ superposed quanta/s sustained; collapse promotion
      < 50 ns/quant. **Test:** synthetic 100M-quant universe, tick-only.

### W2 — Field kernels (implements D2)

- [ ] Effective field set as data (field table + coupling matrix), not code.
- [ ] Interaction kernel: within-cell pair sampling by coupling strength.
- [ ] Condensation rule: cooling distribution → quanta appear (from D3).
- [ ] **Test:** 1D toy run reproduces the two stable nucleon-ish species
      and one massless carrier from Phase 0's acceptance test, unchanged.

### W3 — Tick scheduler + jump-state (implements D5)

- [ ] Tick tiers with hysteresis-free promotion/demotion rule.
- [ ] Jump-state summaries: T, composition distribution, free energy,
      entropy debt; resumable on observation.
- [ ] 1000× time-skip over an unobserved region. **Test:** skip vs.
      full-tick reference agrees within D5's tolerance AND the skipped
      region replays identically from its log entry.

### W4 — Collapse engine (implements D4)

- [ ] Decoherence-threshold rule from PHASE0 pseudocode, incl. the hunted
      failure cases (watched-pot freeze, entanglement chains).
- [ ] θ config + live sensitivity readout (per-region collapse rate).
- [ ] **Tests:** double-slit analog — interference pattern persists when
      unobserved, disappears when the probe bubble covers the screen;
      entangled pair collapses update both partners same tick.

### W5 — Entanglement graph + RNG streams

- [ ] Edge table: create via W2 interactions, preserve across collapse.
- [ ] Correlation check without signaling (partner stats change, marginals
      don't). **Test:** Bell-style correlation score within theory band.
- [ ] Counter-based per-quant streams; determinism fuzz: 100 runs, one seed,
      one log → identical hashes.

### W6 — Probe + acceptance harness

- [ ] Scripted observer bubble (position track over time) as Phase 14's
      stand-in interface: `probe::covers(cell) -> tier`.
- [ ] Acceptance run: big-bang seed → cool → W2 condenses quanta → W4
      collapses → emergent H/He/Li ratios (Phase 0 demo, now on the real
      engine) → full replay check in CI.
- [ ] Collapse-stat physics check: unobserved cavity reaches a blackbody
      spectrum matching theory shape within tolerance.

## Performance budget (fill from Spike A, then hold the line)

| Path                              | Budget        | Measured |
|-----------------------------------|---------------|----------|
| superposed evolve                 | ≥ 10⁷ quant/s | ___      |
| collapse promotion                | < 50 ns/quant | ___      |
| observation-log write             | < 20 ns/event | ___      |
| 1000× jump-skip                   | O(1)/cell     | ___      |
| total universe at t0              | ≤ 1 GB        | ___      |

## Interface exposed to Phase 2 (nuclear)

Write this line into `spec/interfaces.md` when W1–W4 land:

> Phase 2 may read: quanta in collapsed cells (species, energy, momentum),
> collapse events, jump-state composition summaries. Phase 2 may write:
> binding events as new interaction outcomes via the W2 coupling table.
> Nothing else crosses the boundary.

Phase 2's binding curve is therefore testable against Phase 1 without any
knowledge of storage internals.

## Verification strategy

1. **Replay CI** (from Spike C): every merge runs acceptance run + replay
   bit-for-bit.
2. **Theory-band stats:** blackbody shape, interference on/off, Bell
   correlations, H/He/Li — numeric bands in `tests/physics_bands.toml`,
   tuned once, never widened to hide regressions.
3. **Budget CI:** nightly perf run against the table above; a merge that
   breaks a budget must fix or re-baseline with a written reason.

## Sequencing

```
Wk 1-2        Wk 2-3          Wk 3-4           Wk 4-5          Wk 5-6
─────         ──────          ─────────        ──────────      ──────────
W1 store      W3 scheduler →  W4 collapse  →   W6 acceptance    budget CI
W2 fields     jump-state      W5 entangle      run + replay     green 1 wk
(parallel)    + probe stub    + replay CI      in CI            → gate Phase 2
```

## Risks

| Risk | Mitigation |
|---|---|
| Interference/entanglement stats never land in theory band at coarse precision | raise sample counts in tests (offline), keep engine coarse; if still off, it's a real D4 bug — stop and fix the rule, don't tune the band |
| Log volume explodes early-universe | batch collapse events per cell-tick; compression ratio is itself a metric |
| GPU kernel fights SoA layout | W1 benchmark decides CPU-vs-GPU split before W2 is optimized; CPU-only fallback path stays correct |
| Phase 14 probe contract wrong | probe is one file (`probe/`), swapping it later touches one interface |

**Gate:** Phase 2 starts only when the acceptance run is in CI, budgets are
measured-filled, and the interface line is written.
