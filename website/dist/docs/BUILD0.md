# Build Spec 0 — the Micro-Seed (first buildable slice)

**Scope:** the first thing this project builds is the Phase 0 runnable
deliverable: a hot dense seed that expands, cools, condenses quanta, binds
them into nuclei, captures electrons into atoms, and lands roughly the right
H/He/Li ratios — from the rules alone, no element tables, no scripted
nucleosynthesis — and replays bit-for-bit from `seed + observation log`.

This spec is the binding engineering contract for that slice. Where
PHASE0.md *recommends* a position, BUILD0 **adopts** it as the v0 default;
a decision stays re-openable only until its acceptance test passes, after
which changing it is a physics-build bump, not an edit.

**Definition of done:** identical to PHASE0.md's, plus the acceptance run
(`python -m sim.demo`) is green on the bands in this file, the three spike
reports are on disk, and `spec/decisions.md`, `spec/constants.md`,
`spec/interfaces.md` are written and frozen at `physics_build 0.1`.

---

## Environment (pinned, verified 2026-10-27)

| Item    | Version                                    |
|---------|--------------------------------------------|
| OS      | Windows 11 (recorded development host)     |
| Python  | 3.11.9                                     |
| numpy   | 2.4.6                                      |
| pytest  | 9.1.1                                      |
| extras  | none — stdlib + numpy only                 |

Rules:

- Pure Python + numpy. No SciPy, no matplotlib, no GPU. The engine later
  moves to Rust; nothing in this slice may depend on more than these.
- float64 everywhere; elementwise numpy only in hot paths (no `matmul`, no
  BLAS) so results are bit-stable across runs.
- Replay determinism is guaranteed **same-machine, same-build**. That is
  enough for Phase 0; cross-machine golden vectors arrive with Phase 1 CI.
- `requirements.txt`: `numpy==2.4.6`, `pytest==9.1.1`. Nothing else.

## What ships (maps to PHASE0.md deliverables)

1. `spec/decisions.md` — D1–D5 closed, each with rationale + rejected
   alternatives (transcribed from §Decisions below when its test passes).
2. `spec/constants.md` — the physics-build 0.1 table + calibration anchors.
3. `spikes/a_quant_cost/`, `spikes/b_shells/` — throwaway, with
   `report.json` each. Spike C is not throwaway: it lands as `sim/rng` +
   `sim/log` + the replay harness in milestone M0.
4. `sim/` — the micro-seed demo package, laid out to grow into Phase 1.
5. `tests/` — pytest suite incl. the acceptance run; `tests/oracle/` holds
   every real-world number the engine may never import.

## Decisions (adopted as v0 defaults)

- **D1 quant:** continuous fields sampled on demand. A quant is a row in
  two numpy SoA tables sharing one id space:
  - superposed: `species u8, energy f64, phase f64`
  - collapsed: `+ cell u16, pos f64×3, momentum f64×3`
  Collapse is a row move from table S to table C — an append, never an
  allocation in the hot loop. Invariants (must never be true): a row in
  both tables; a collapsed row with no log entry; `species` outside the
  field table.
- **D2 fields:** the effective set below — five fields, not the Standard
  Model. Couplings are the tuning knobs. Rejected: literal gauge theory
  (cost without benefit at this layer); particle list (violates the roadmap).
- **D3 seed:** `Seed = (prng u64, physics_build str, T0 f64, expansion_rate f64, eta f64)`.
  Initial state is a per-cell `(T, tick)` distribution in superposed form;
  nothing is materialized until condensation or collapse. Constants are
  versioned: changing any constant bumps `physics_build`.
- **D4 observation:** collapse when a quantum's **cumulative logged-
  interaction count** within its cell exceeds θ, or when a probe cell
  covers its cell; entangled partners (edge table, kept for the shape)
  collapse together. Rejected: conscious-observer collapse (untestable
  today). Perception controls render detail, not existence.
- **D5 time:** discrete ticks, geometric step `t_{n+1} = t_n · 1.01` from
  `t0 = 1e-5 s` (~1670 ticks ≈ 180 s of cosmic history; the demo default
  2400 ticks runs to ~2.3×10⁵ s, tick count is a run parameter). Unobserved cells
  may **jump-state**: analytic propagation recorded as one log entry.
  v0 jump covers cooling + annihilation closed form only.

## Physics build 0.1

Natural units, energies in MeV. Field table (data, in `sim/fields.py`, not
branching code):

| id | name (code-safe) | rest mass | spin | charge | couplings |
|----|------------------|-----------|------|--------|-----------|
| 0  | `q_u`            | m_q·(1+δ) | 1/2  | +2/3   | strong, em |
| 1  | `q_d`            | m_q       | 1/2  | −1/3   | strong, em |
| 2  | `el`             | m_e       | 1/2  | −1     | em        |
| 3  | `gl`             | Λ_conf    | 1    | 0      | strong (confined) |
| 4  | `ph`             | 0         | 1    | 0      | em        |

Constants (irreducible set, `spec/constants.md` owns the final table):
`m_q, δ (flavor split → nucleon mass gap), m_e, α_s, α_em, Λ_conf, η (baryon asymmetry), ε_b (matter–antimatter excess), T0, H0, C_w (effective weak rate), C_cap (radiative capture), S (astrophysical S-factor, charged fusion)`.

**Emergent structures, all computed:**

- *Nucleons:* 3 confined quanta at `T < Λ_conf`; `uud` → charge +1,
  `udd` → charge 0. That is D2's acceptance test in code: **two stable
  baryon species and one massless carrier exist because the couplings say
  so, and a test asserts exactly that.**
- *Nuclei:* residual binding `B(A,Z)` from a liquid-drop + pairing +
  asymmetry form with 5 coefficients fit on **five anchors only**
  (d, ⁴He, ⁵⁶Fe, plus asymmetry slope; anchors live in `tests/oracle/`
  and calibrate constants — never runtime lookups). Everything else in the
  chart is prediction; disagreements go to the surprises ledger.
- *Atoms:* binding scale `I = ½ α_em² m_e` computed from constants;
  electron capture is just another detailed-balance channel.

**Calibration protocol:** exactly three anchor runs — δ tuned so the
neutron/proton freeze-out ratio lands in band; C_cap so He-4 yield lands
in band; C_w so freeze-out happens at the right epoch. Every other
constant is exploration, fixed once and published. Rejected alternative:
calibrating against the yield table directly (that is scripted
nucleosynthesis).
**Result (M3, 2026-10-27):** δ kept at 0.01 (already in band); `C_cap` 1.0 →
5.0 (Y_p band); `C_w` 3.3e-3 (n/p band, freeze epoch). No other constant
moved; band table untouched.

## Engine architecture

```
simworld/
  BUILD0.md            ← this file
  ROADMAP.md  PHASE0..5.md
  requirements.txt
  sim/
    __init__.py
    constants.py       # physics_build 0.1 table + version string
    rng.py             # counter-based streams (spec below)
    log.py             # append-only observation log + replay driver
    state.py           # canonical state dump → sha256
    lattice.py         # 8-cell periodic ring; T field; expansion a(t)
    quanta.py          # SoA tables S/C, ids, quant add/move/collapse
    fields.py          # field table + coupling matrix as data
    condense.py        # thermal targets → quanta appear (superposed)
    bind.py            # nucleon/nucleus/atom registry: bound-state search
    network.py         # channel discovery + detailed-balance event sampler
    collapse.py        # θ rule + entanglement edges
    jump.py            # analytic cooling/annihilation summaries
    probe.py           # probe::covers(cell) -> bool (Phase 14 stand-in)
    demo.py            # acceptance run CLI
  spikes/
    a_quant_cost/  b_shells/          # each with report.json
  spec/
    decisions.md  constants.md  interfaces.md   # frozen at M4
  tests/
    oracle/            # ONLY place real numbers live (masses, IPs, BBN data)
    test_rng.py test_log.py test_replay.py test_physics_bands.py ...
    physics_bands.toml
  runs/                # demo output (gitignored)
```

### Data rules

- Quanta are rows; ids are stable `u32`. Reactions consume/produce ids
  through the log. **Every state mutation outside free cooling goes
  through the log writer — including tests.**
- The bound-state registry (`bind.py`) is an emergent cache: it records
  which `(A,B)` fusion channels exist because `B(A+B)` computed positive.
  Deleting it and recomputing must give identical hashes (CI-enforced,
  the discipline every later phase inherits).
- Reaction channels are discovered from the registry, never enumerated:
  for every nearby pair with a bound sum, the channel exists. This is why
  "every combination is computable" holds in this slice already.
- **Detailed balance by construction:** reverse rate = forward rate ÷
  Saha equilibrium constant built from the engine's *own* binding energies:
  `k_rev = k_fwd · (g_A g_B / g_C) (2πμ kT/h²)^{3/2} exp(−B_C/kT)`.
  Equilibrium in a closed box is therefore exact by architecture; a test
  checks it anyway.

### RNG (exact, so replay needs no state)

One stateless function; every random number in the sim comes from it:

```
draw(seed, tick, kind u16, i u64) -> u64:
    x = (seed + tick·0x9E3779B97F4A7C15 + fnv1a64(kind) + i)
    return splitmix64(x)          # stateless one-shot
splitmix64(x): x += 0x9E3779B97F4A7C15
    z = x; z = (z ^ (z>>30)) · 0xBF58476D1CE4E5B9
       ; z = (z ^ (z>>27)) · 0x94D049BB133111EB
       ; return z ^ (z>>31)
float() = top 53 bits / 2^53
```

`kind` is a small enum (`CONDENSE, COLLIDE, REACT, DECAY, ANNIH`).
`test_rng.py` pins golden bytes generated once from a reference
implementation and manually checked.

### Observation log (the spine, from day one)

JSONL, gzip-compressed on close. One entry per event batch:

```
{"t":tick,"k":"condense|collapse|react|bond|dissoc|annih|jump|probe",
 "cell":id,"kind":u16,"q":[affected ids],"s":[state digest ints],
 "cause":"theta|probe|thermal|<reaction signature>"}
```

Replay = re-run with same seed; before each stochastic draw the engine
asserts its event key equals the next log entry, so replay *validates*
that the causes match rather than trusting them. Canonical state dump =
concatenation of each SoA column (fixed field order, ids sorted, LE
float64) + tick + physics_build string; sha256 taken every 100 ticks and
at end. **Acceptance: run1 hash chain == run2 (fresh) == replay(run1)
log.**

### Physics flow per tick

1. Expand: `a(t)`, `T_c(t)` (radiation-dominated, `T ∝ 1/a`).
2. Jump check: cells outside the probe and above their skip threshold
   propagate analytically; log a `jump` entry; skip the rest for them.
3. Condense: compare populations to thermal targets; materialize the
   deficit as superposed quanta (species masses from the field table;
   `ε_b` bakes the net baryon excess into sampling).
4. Bind: when `kT` drops below a computed binding energy, bind eligible
   groups (quarks→nucleons at `Λ_conf`; nucleons→nuclei; `el`+nucleus→
   atom) and emit the carrier (`gl`/`ph`); reverse by detailed balance.
5. React: sample network channels by proximity (same-cell) with `C_cap`
   / Gamow-`S` rates; photodisintegration via the same detailed balance.
   Weak `n↔p↔` conversion at `C_w·T⁵` while it exceeds expansion —
   freeze-out is emergent, and `n/p = exp(−δ/T_freeze)` follows.
6. Collapse: increment per-quant interaction counts; ≥ θ → collapse batch
   (cause `theta`); probe cells → collapse all (cause `probe`).
7. Hash + log flush.

## Spikes

- **Spike A — quant cost** (`spikes/a_quant_cost/`): 10⁶ superposed +
  10⁴ collapsed quanta in SoA, 10⁵ random pair interactions/tick,
  100 ticks; `report.json` with ns/quant/tick CPU. Target: evolve pass
  ≥ 10⁷ quanta/s (v0 scale needs far less; the number feeds Phase 1's
  budget table). If missed on elementwise numpy, record the packing fix
  needed (more quanta/cache-line) — do not optimize further here.
- **Spike B — shells** (`spikes/b_shells/`): hydrogenic analytic +
  one generic screening correction → IP₁ for a probe set {H, He, Li, C,
  Fe}; oracle bands: H exact to 0.1% (analytic anchor), others ±40%
  (documented screening-only error). Emits `report.json` with the error
  curve CSV. Feeds how far past Spike B the Phase 3 SCF solver must go.
- **Spike C — replay** is M0 below (it is the spine, not a spike).

## Milestones

Order is strict; each gate is a pytest run, not an opinion.

### M0 — replay spine (Spike C lands here) — DONE 2026-10-27
- [x] Repo layout above; `requirements.txt`; `python -m sim.demo` runs on an empty world.
- [x] `rng.py` + golden-vector tests; `log.py` + canonical hash; toy-counter world replays bit-for-bit.
- **Gate:** `pytest tests/test_rng.py tests/test_replay.py` green — 15 passed; empty-world demo run twice produced identical final hashes and both replayed PASS.

### M1 — spikes — DONE 2026-10-27
- [x] Spike A + B `report.json` on disk; numbers transcribed into this file's budget table.
- **Gate:** Spike A (`spikes/a_quant_cost/`): evolve pass 2.81×10⁸ quant/s (3.55 ns/quant/tick, CPU) — 28× over the 10⁷ target, no packing fix needed; 10⁵ interactions/tick cost 49 ns/pair (2.0×10⁷ pairs/s incl. engine counter-RNG index generation). Spike B (`spikes/b_shells/`): aufbau + hydrogenic + one fitted per-l screening plane predicts IP₁ from Z alone — probe set errors H 0.0% (analytic anchor, band 0.1%), He −16.9%, Li +4.4%, C −18.2%, Fe −4.1% (band ±40%, all pass; train RMS 6.9%); bare-Z baseline spans +121%…+7171% — the error curve is `spikes/b_shells/errors.csv`. Phase 3 verdict: screening-only holds all five probes; SCF must go past smooth screening only for sub-chemical accuracy, worst residuals 1s² (He) and p-row trends; s/d-block first IPs need nothing exotic.

### M2 — quanta and cooling — DONE 2026-10-27
- [x] Lattice + expansion + condensation + annihilation; superposed population tracks thermal target within band.
- [x] Collapse θ + probe: with probe on cells {2,3}, those collapse first; ≥99% of unprobed quanta end superposed; reaction statistics unchanged whether or not the probe is on (statistical-equivalence test, 20 seeds).
- [x] Jump: 1000× skip of an empty cooling cell vs full-tick reference — T within 0.1%, log-replayed summary identical.
- **Gate:** D4/D5 acceptance tests green (`tests/test_m2_physics.py`, `tests/test_m2_jump.py`; full suite 46 passed). Measured: hot start materializes 734,680 quanta at tick 0 (== summed targets); rate-limited annihilation (half-surplus/tick) tracks the target with max deviation 3.97% at tick 13, band 10%; probe cells {2,3} collapse their whole tick-0 fill (183,670, cause `probe`, decay stream only) while θ batches stay a trickle — 180 quanta collapsed over 2400 ticks, 0.033% of unprobed creations (≤1% ⇒ ≥99.9% of unprobed quanta never observation-collapse); probe on/off draws + created + annihilated counts bit-equal for all 20 seeds. Jump: cells cool empty at T≈2.7 MeV (~tick 731), 8 cells × one 1000-tick skip = 8,000 cell-ticks skipped, T/t exact, both runs replay PASS, and the jump run's final hash equals the full-tick reference — the jump is observationally transparent.

### M3 — nuclei emerge — DONE 2026-10-27
- [x] Nucleons condense below `Λ_conf`: 1,318 nucleons from quark triples; test "exactly two stable baryon charges + one massless carrier" green (`udd`/`udu`, one `ph`).
- [x] Weak freeze-out: `n/p = 0.130` — band 0.10–0.20; freeze-out tick 910 (T ≈ 1.08 MeV), 336 ticks before bind.
- [x] BBN network → `Y_p = 0.2276`, `X_H = 0.7473` — bands 0.20–0.30 / 0.69–0.80 green; (Z,A)-keyed nuclides only; element-name grep gate in the test suite.
- **Gate:** `tests/test_m3_nuclei.py` green (7 tests; full suite 53 passed). Six seeds 0–2026: n/p 0.123–0.133, Y_p 0.210–0.232, X_H 0.741–0.767 — all bands green simultaneously, no seed cherry-picking. Calibration per protocol: δ fixed at 0.01, `C_cap = 5.0` (Y_p band; also burns He-3 in before the jump window shuts), `C_w = 3.3e-3` (n/p band + epoch — absorbs a 1.3× freeze-tracking lag, surprises ledger). Registry cache-off run hashes bit-identical to cache-on; acceptance run `--seed 42` (final `3513de47…`) REPLAY PASS. Jump extended to *cooled* cells (no bosons, ≤2 inert quark leftovers = bind's mod-3 residue, weak frozen, every channel prob < 1e-8): 6 jumps × 1,000 ticks, final hash still equals the full-tick reference — transparency survives the nuclear era. D/H measured 0: sub-granularity at 1,318 baryons, surprises ledger.

### M4 — atoms, acceptance, freeze — DONE 2026-10-28 (nightly gate pending)
- [x] Electron capture below `I`: `atoms.step` runs under gate `T_GATE = 3I` (I = ½α²mₑ computed, never stored); first capture tick 2958 all seeds; X_neutral = 0.9965, X_e = 0.0035 vs engine Saha 0.0057 — inside the published order-of-Saha band [S/8, 2S]; atoms measured as (Z, A) counts: 981 H, 75 He, 0 Li (n_atoms_* yields; no element names).
- [x] Acceptance run: `python -m sim.demo --seed 42` (3400 ticks) green end-to-end; fresh rerun uncompressed log sha256 bit-identical (`15e50cd6…`), REPLAY PASS 34 hashes, final `fe8e094a…` — evidence in `_m4run/`.
- [x] `spec/decisions.md` (D1–D5 closed with rejected alternatives + keeping tests), `spec/constants.md` (0.1 table + anchors + RNG lanes), `spec/interfaces.md` (freeze line verbatim + internal contracts incl. atoms) written; physics_build `0.1` tagged in `sim/constants.py`.
- **Gate:** full `pytest` green two nights in a row → Phase 1 starts. Suite green at freeze: **65 passed** (7 M4 + 5 bands meta-test added); nightly task `simworld-nightly-CI` = `pytest tests/test_replay.py tests/test_physics_bands.py` per BUILD0 verification strategy #1.

## Acceptance bands (`tests/physics_bands.toml`)

| Quantity                     | Band            | Reality |
|------------------------------|-----------------|---------|
| n/p at weak freeze-out       | 0.10 – 0.20     | ~0.14   |
| Y_p (⁴He mass fraction)      | 0.20 – 0.30     | 0.247   |
| X (H mass fraction)          | 0.69 – 0.80     | ~0.76   |
| D/H                          | 1e-6 – 5e-4     | ~2.5e-5 |
| Li/H (either isotope)        | 1e-11 – 1e-7    | 1e-10 (lithium problem: record whatever emerges, surprises ledger) |
| X_neutral after capture (M4) | ≥ 0.90          | ~1 by run end |
| X_e / Saha (M4)              | 1/8 – 2         | order of Saha; freeze gap in ledger |
| unprobed superposed retained | ≥ 99%           | —       |
| jump vs tick reference       | T ±0.1%, n ±1%  | —       |
| replay                       | bit-for-bit     | —       |

Bands are set once at M4 and may only be narrowed, never widened to hide
a regression (PHASE1 rule, adopted early).

## Performance budget (fill at M1/M4)

| Path                                  | Budget          | Measured |
|---------------------------------------|-----------------|----------|
| full acceptance run                   | < 10 min wall   | 4.9 s wall, 3400 ticks, seed 42, 37,083 log entries (2026-10-28) |
| peak quanta alive                     | ≤ 2×10⁶         | 734,725 at tick 0 (hot start) |
| evolve pass (Spike A)                 | ≥ 10⁷ quant/s   | 2.81×10⁸ quant/s, 3.55 ns/quant/tick, CPU (2026-10-27) |
| event + log write                     | < 5 µs          | 2.7 µs/entry (digest 0.8 + json 1.8 + gzip write; the 7.3 µs counter-RNG draw is separate) |
| replay of full run                    | < 2× run time   | 4.9 s = 1.0× run (subprocess incl. python startup) |
| log size compressed                   | < 200 MB        | 0.6 MB gz (4.8 MB raw) at 3400 ticks |

## Interface line to freeze at M4 (into `spec/interfaces.md`)

> Phase 1 may read: the quant tables (S/C) by id, the field/coupling
> table, the observation log, jump-state summaries, and the collapse
> rule's θ + interaction counts. Phase 1 may write: extended collapse
> causes (probe contract) and new field rows via a physics-build bump.
> Nothing else crosses the boundary; `bind`/`network` internals are
> private and get replaced wholesale by Phase 2's real kernels.

## Verification strategy

1. **Replay CI** = `pytest tests/test_replay.py tests/test_physics_bands.py`
   nightly (a scheduled task on this box until Gitea CI exists on adler40).
2. **Oracle discipline:** real-world numbers live only in `tests/oracle/`;
   a test greps `sim/` for banned names (any element/material name beyond
   `hydrogenic` analytic anchor) — the grep gate from PHASE3, started now
   so it can never be retrofitted.
3. **Surprises ledger:** `spec/surprises.md`, one dated line per emergent
   disagreement with reality and its measured gap.

## Not in this slice (explicitly deferred)

GPU/wgpu; Rust/ECS port; Bell tests and entanglement-graph validation
(Phase 1 W5); blackbody-spectrum and interference tests (Phase 1 W6);
full nuclear force kernel and decay chains (Phase 2 replaces M3's network
— M3 code is explicitly demo-grade); SCF solver (Phase 3); multi-cell
hydrodynamics; any rendering. Building these here is a spec violation.

## Risks

| Risk | Mitigation |
|---|---|
| Liquid-drop+pairing misses the ⁴He spike the yields need | He-4 yield depends mostly on n/p + available bound states, not the bump; if out of band, log surprise + allow one α-cluster term fit on the He anchor, documented as physics-build 0.2 |
| Li question (BBN lithium problem) makes a fair band impossible | band is 4 orders wide by design; the demo's job is to produce a number and a mechanism, not to solve cosmology |
| numpy float non-determinism between runs | elementwise-only hot path; hash-chain test in M0 catches any drift immediately |
| Calibration knobs absorb physics (tuning until everything passes) | exactly 3 anchors, declared before tuning; all other constants published untouched; band table written before M3 tuning starts |
| Spec drift — Phase 1 features creeping into the demo | "Not in this slice" list is a review checklist item at every milestone gate |

**Gate:** BUILD0 is done when PHASE0.md's definition of done is green via
the acceptance run, this file's band table passes, spike reports are on
disk, and the three spec files are frozen at `physics_build 0.1`. Phase 1
then proceeds per PHASE1.md, with Spike C promoted to CI as required there.
