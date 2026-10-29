# Decisions D1–D5 — CLOSED at physics_build 0.1 (frozen 2026-10-28)

Each decision lists rationale, rejected alternatives, and the acceptance
test that keeps it closed. Transcribed from BUILD0.md §Decisions when the
named tests passed.

## D1 — quanta are sampled rows, not persistent fields — CLOSED

A quant is a row in two numpy SoA tables sharing one id space
(superposed: species/energy/phase; collapsed: + cell/pos/momentum).
Collapse is a row move, an append, never an allocation in the hot loop.

- Rationale: Spike A measured 2.81e8 quant/s on the row layout — 28x
  over budget; nothing else needed to be true for the cost model to hold.
- Rejected: persistent per-quant objects (allocation in the hot loop);
  packed bit-level structs (Spike A: no packing fix needed at 10^7).
- Kept closed by: `tests/test_m2_physics.py::test_population_tracks_thermal_target`
  (invariants: no row in both tables, `species` always in the field table).

## D2 — five effective fields, not the Standard Model — CLOSED

Field table `q_u, q_d, el, gl, ph` (`sim/fields.py` as data, not
branching). Couplings are the only tuning knobs.

- Rationale: D2's acceptance is structural and it passes in code: exactly
  two stable baryon charges (+1, 0) and one massless carrier emerge from
  the couplings, asserted by
  `tests/test_m3_nuclei.py::test_baryon_rule_two_charges_one_carrier`.
- Rejected: literal gauge theory (cost without benefit at this layer);
  a particle list (violates the roadmap's emergence-first rule).

## D3 — seed = (prng u64, physics_build, T0, expansion_rate, eta) — CLOSED

Initial state is a per-cell (T, tick) distribution in superposed form;
nothing is materialized until condensation or collapse. Any constant
change bumps `physics_build`.

- Rationale: replay is bit-identical same-machine/same-build; the log
  header pins seed + physics_build + meta and replay refuses mismatches.
- Rejected: float seeds / stochastic warm starts (no golden-vector
  discipline possible); cross-machine bit-stability claims (deferred to
  Phase 1 golden vectors, deliberately not promised now).
- Kept closed by: `tests/test_replay.py`, `tests/test_m4_atoms.py::test_m4_run_replays`,
  and the acceptance run's bit-identical fresh rerun (BUILD0 M4 gate).

## D4 — observation = theta over logged interactions, or probe cover — CLOSED

Collapse when a quantum's cumulative logged-interaction count in its cell
exceeds theta, or when a probe cell covers its cell. Entangled partners
collapse together (edge table kept for the shape).

- Rationale: measured — probe cells collapse their entire tick-0 fill
  (cause `probe`) while theta batches stay a trickle: 0.033% of unprobed
  quanta observation-collapse over 2400 ticks (>=99% retained required);
  and physics is statistically identical with the probe on or off across
  20 seeds (draw counts, created, annihilated, created_bosons).
- Rejected: conscious-observer collapse (untestable today); perception
  affecting existence (perception controls render detail, not existence).
- Kept closed by: `tests/test_m2_physics.py` (probe-first, retention,
  statistical-equivalence tests).

## D5 — geometric ticks; unobserved cells jump-state — CLOSED

`t_{n+1} = t_n * 1.01` from `t0 = 1e-5 s`; tick count is a run parameter
(default `TOTAL_TICKS = 3400` since M4, carrying through recombination).
Jump-state = analytic propagation logged as one entry; v0 covers the
cooling + annihilation closed form for *cooled, quiet* cells only.

- Rationale: a 1000-tick jump of a cooled cell is observationally
  transparent — the jump run's final hash equals the full-tick reference
  bit-for-bit, T exact, and eligibility now also refuses jumps whose span
  would cross the atoms capture gate (`atoms.jump_quiet` lands worst-case
  at the landing temperature).
- Rejected: continuous time (log/replay needs event order anyway);
  state-dependent (observer-based) jump eligibility beyond the proven
  cooled+quiet gate.
- Kept closed by: `tests/test_m2_jump.py` (hash equality vs reference),
  `tests/test_m4_atoms.py::test_jump_never_straddles_capture`.
