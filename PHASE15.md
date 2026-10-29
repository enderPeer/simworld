# Phase 15 — Hyperoptimized Runtime

**Goal:** the same world, one order of magnitude cheaper per tick —
and *provably* the same world. This is the compiler phase: Phase 14
froze the **semantic** LOD contract (what may be skipped, what it
costs); Phase 15 finds the **mechanical** one, and its entire
permitted vocabulary is scheduling, batching and offload decisions.
Three engineering theses, each test-first. (1) **Determinism is a
property of the schedule, not of the math** — the compiled runtime
replays bit-identical from seed + observation log, because every
reduction has a fixed order, every GPU kernel is deterministic, and
the runtime build fingerprint rides the replay-chain header (seam
S23: bit-identity is a *per-compiler* promise; naive-vs-compiled
equivalence is within published error budgets, which is what Phase
14's compiled-vs-naive battery already measures — the chain finally
says *which compiler* was identical). (2) **Published error budgets
are physical quantities** — they are the bit widths of the fixed-
point channels between GPU physics and CPU cognition; a budget is no
longer a tolerance someone hopes in, it is how many bits the bus
carries, and the causal lane is lossless-by-construction while only
epistemic/aggregate channels may delay. (3) **Every layer must be
allowed to sleep** — tiered ticks need per-layer jump-states with
interval certificates, and biology/society/ledgers never defined one
(seam S24, owed upstream): the scheduler may generalize Phase 0's
jump machinery across layers but may not invent what a coarse
population histogram *means*; each layer signs for its own coarse
state. The phase's honesty devices: Phase 14's existence suite runs
**unmodified** (hash-registered at its W7) against the compiled
runtime; all fifteen phases' acceptance suites are the conversion's
specification; and every number in the budget table — atoms, agents,
reactions per ms — is measured on suite runs, nightly, with ±5%
regression alerts, not guessed on a microbenchmark podium.

**Prerequisites (hard gate, from Phase 14 + seam round nine):**

- Phase 14 gate green: existence suite frozen and hash-registered;
  governor + observation map live; S22 allocation traces on the
  chain; the Phase 14 freeze line is this phase's entire bill of
  rights.
- Seam round nine, both land upstream **before W2/W3 open**:
  - **S23** — replay-chain header carries the **runtime build
    fingerprint** (extends D7's `physics_build` to the compiler/
    runtime build); cross-runtime comparison is defined as within-
    budget, never bit-identity; `spec/decisions.md` D16 drafted.
  - **S24** — Phases 5/8/10/11/12 each publish a `::jump_state()`
    contract: interval-certified coarse summaries for their layer
    (population histograms, throughput bounds, graph moments, wealth
    distribution tails), with violation semantics — the certificates
    are what the tiered scheduler ticks against and what the naive
    replay checks on interval crossing.
- S7/S9/D7 versioning discipline; S16/D10 nested-sim determinism
  (nested children are compiled too, and their chain headers pin
  their own runtime builds).
- Phase 13's ledger-conservation executor (error-budget meters
  already exist per ledger; this phase spends them knowingly).

**Definition of done:** the same seed, run naive and compiled, lands
every Phase 0–14 ledger within its published budget, and the
compiled run replays **bit-identical against itself** a thousand
times while host scheduling jitter, async copy depths and queue
reorders are injected on purpose — the chain does not flinch, because
the schedule is part of the seed's story, not of the machine's
(keystone torture test). The existence suite, file untouched, hash
verified, runs green against the compiled runtime; all fifteen
phases' acceptance suites run green after the ECS conversion, which
is the conversion's only specification — a suite that notices a
silently-dropped row is a suite doing its job. Duty-cycle histograms
show the tiering promise kept: on the money world, quantum ticks at
full rate only in observed cells, biology ticks ~10³ slower on
compressed populations, society ~10³ slower still on graph moments —
and unobserved regions of **every layer** sit in jump-states whose
interval certificates are checked by the naive replay, including one
adversarial seed where a certificate would be violated if anyone
computed it naively; the violation is *caught, reported and
refined*, never smoothed (a lying jump-state is red CI, by
construction). The bus is the budget, literally: GPU physics and CPU
cognition exchange fixed-point interval channels whose widths *are*
the published error budgets, bytes/sec on the narrow side is measured
against the naive model's in-memory traffic (the ratio is a reported
headline number), the causal lane delivers every flux/choice event
losslessly while the epistemic lane is observed delaying a gaze-map
update and losing nothing. Whole-world snapshot is a memcpy:
serialize = segments out + ledger logs, restore = bit-exact, and no
pointer ever crossed a layer boundary to make that lie unnecessary
(grep gate: entity refs are indices). The budget table is filled
with measured numbers on the named reference machine — quanta,
atoms, reactions, agents, ledger events per ms, naive-vs-compiled
ratios per tier — checked nightly at ±5%, and the headline demo is
the roadmap's promise cashed: **a full acceptance world (10⁴ agents
plus full physics through the society layer) ticks interactively on
one card of the reference generation**, measured, printed on the run
record, and replayable from seed + observation log by tomorrow's CI
on a different machine of the same build.

---

## Scale contract

- Reference machine is *named and versioned* in every perf number
  (gen-2 cluster: the 4090 box; one row per card class, hardware-
  relative ratios reported alongside absolutes).
- ECS: all SoA stores unified into archetype segments; cross-layer
  references are 32-bit indices into published segment tables; world
  snapshot = concat(segments) + ledger logs, target < 10 s for the
  money world.
- Tiered ticks: 5 tick classes observed on the money world — quantum
  (observed cells only), physics/chemistry (cell ladder + jumps),
  biology (histogram + certificates), society/ledgers (graph moments),
  existence/governor (map recompute); duty-cycle histogram is a
  published artifact of every acceptance run.
- Bus: causal lane lossless (flux, choice, liability events —
  fixed-point payloads within per-channel budgets); epistemic lane
  (gaze map, aggregate stats) may delay ≤ 1 tick class.
- Acceptance rigs: the torture pair (naive/compiled + jitter), the
  existence-suite rerun, the adversarial-certificate seed, the
  snapshot round-trip, the single-card demo world, the nightly perf
  ledger.

## Architecture

No new world-state. One new engine layer, zero new `sim/` packages —
this is where the freeze line is honored most literally:

```
runtime/                      (engine/, not sim/ - the compiler)
  store/      whole-world ECS: data-oriented, cache-friendly
              archetype/SoA store - every layer's rows in
              published segments; change-filter masks per segment;
              cross-layer refs = indices only (grep gate); snapshot
              = memcpy of segments + ledger logs
  ticks/      tiered scheduler: tick classes × region resolution
              (reads Phase 14's observation map + governor orders);
              per-layer S24 certificates gate every jump; interval
              crossing => exact re-instantiation, same tick, ordered
              by the causal lane (cross-layer event ordering rides
              the existing sub-lane contract - no new clock)
  split/      device partition: cell-layers (quantum, physics,
              chemistry, tracers, fluids) on GPU with deterministic
              kernels (fixed-order reductions, no float atomics -
              ordered accumulators or fixed-point); agent cognition
              on CPU - society and ledgers on CPU too; multi-GPU = graph-partition
              the cell lattice minimizing cross-partition flux,
              repartition only on governor orders
  bus/        the narrow bandwidth between the devices (roadmap
              wording, honored literally): fixed-point interval
              channels between
              devices; channel widths = published error budgets
              (budgets become bit widths, versioned with D7 build
              ids); causal lane lossless + ordered; epistemic lane
              best-effort; every channel's spend metered
  replay/     chain v2: header pins runtime build fingerprint (S23)
              alongside physics_build (D7) + observation log + S22
              allocation traces + schedule trace (partition map,
              queue depths as seed-derived values); two-clock gate
              extended with device-jitter injection
  meters/     perf ledger as a first-class run artifact: throughput
              rows (per tier), bus bytes, budget spend, duty cycles
              - replayable, diffable, nightly-regressed
```

Data rules:

- **The scheduler never invents semantics.** Every coarse state it
  runs on is signed by its layer (S24 certificates); an unsigned
  coarse read is a red build, not a fallback.
- **Budgets are spent, tracked, and reported** — per-ledger error-
  budget meters already exist (Phase 14's executor); this phase
  makes them *visible in the run record*, and exhaustion is a
  decision event (re-tune needs a `spec/decisions.md` entry), never
  a slider drag.
- **Causality is lossless; perception may lag.** No flux, choice or
  liability event is ever dropped or delayed across a device or
  partition boundary; gaze maps and aggregate stats may be a class
  late, and that is a measured fact, not a race.
- **No new world-state tokens.** Grep gate: `runtime/` contains no
  species, agents, claims, prices or beliefs — it moves rows, it does
  not know what they mean.

## Work packages

W1 converts (store), W2 tiers (needs S24 upstream), W3 splits (needs
W1+W2 shapes), W4 reproves (chain, after everything it must pin), W5
measures throughout, W6 gates, W7 freezes.

### W1 — The store: whole-world ECS conversion

- [ ] Unified archetype segments; index-only cross-layer refs;
      change filters; memcpy snapshots; ledger semantics untouched.
- [ ] **Tests:** all fifteen phases' acceptance suites green on the
      converted store (the suites are the specification — any suite
      going red is a lost row, hunt it, do not edit the suite);
      snapshot round-trip bit-exact incl. ledger logs; grep gate:
      zero address-valued cross-layer refs; conversion diff to naive
      within budget on the full rig set.

### W2 — Tiered ticks + certificates (S24 upstream first)

- [ ] Tick classes wired to observation map + governor; per-layer
      `::jump_state()` consumers; interval-crossing re-instantiation
      ordered through the causal lane.
- [ ] **Tests:** duty-cycle histograms show the tiering promise
      (quantum only where observed; biology/society ratios reported,
      bands not targets); adversarial seed: certificate violation
      caught -> refined -> reported, never smoothed; certificates
      unsigned anywhere = build fails; era-compression chain (D8/D9/
      D10/D11/D13) runs re-expressed as certificates (the decisions
      become machine-checkable here or the seams re-open).

### W3 — The split: GPU physics, CPU cognition, narrow bus

- [ ] Deterministic GPU kernels (fixed-order reductions, no float
      atomics); fixed-point interval channels; graph-partition
      sharding; causal/epistemic lane discipline.
- [ ] **Tests:** device-jitter torture — async copies, queue-depth
      randomization, partition reshuffles injected; chain bit-identical
      across all of it (schedule is seed-derived); bus bytes/sec vs
      naive in-memory traffic (headline ratio, reported); lossless
      causal lane under epistemic-lane starvation (starve the gaze
      map: no world event may be lost — count events both sides);
      channel budget == channel width (property test: a payload
      needing one more bit refuses to fit, loudly).

### W4 — Reproducibility: seed + observation log, now with compiler

- [ ] Chain v2: runtime build fingerprint in header (S23 upstream
      first); schedule trace folded in; replay driver for the whole
      phase-acceptance corpus.
- [ ] **Tests:** cross-machine replay (same build, different cards)
      bit-identical; cross-build replay classified within-budget,
      never bit-identity (D16 semantics asserted both directions);
      nightly matrix: full corpus replays from seed + log; a build
      bump without a header bump fails CI.

### W5 — Budget targets: measured, not guessed

- [ ] Perf ledger as run artifact; naive-vs-compiled ratio table per
      tier; reference-machine protocol (named hardware, locked
      clocks); nightly regression alerts at ±5%.
- [ ] **Tests:** budget table complete — quanta/atoms/reactions/
      agents/ledger-events per ms, all from suite runs (podium
      microbenchmarks excluded by tooling: the profiler only reads
      suite harnesses); single-card demo world ticks interactively
      on the reference card (the roadmap's promise, measured and
      printed on the record); every Phase perf-table row from
      Phases 0–14 re-measured and back-filled (the fifteen plans
      finally get their blanks filled — this is the phase that
      pays the paperwork debt of the whole campaign).

### W6 — The gate: existence suite, unmodified

- [ ] Phase 14 existence suite hash-checked and run against the
      compiled runtime; Phase 13 ledger-diff executor re-run on
      compiled toggles; compiled-vs-naive battery at full rig scale.
- [ ] **Tests:** suite untouched (hash verified before and after);
      compiled world passes P14's own rent line with its governor
      ON (rent stacks: P14's ≥40% is measured against naive; this
      phase must not hand it back); no agent-belief diff beyond
      budget anywhere in the corpus.

### W7 — Freeze + decisions

- [ ] D16 (cross-runtime equivalence semantics; build fingerprint in
      chain) into `spec/decisions.md` with S23 closure.
- [ ] Freeze `runtime/` contracts (below); perf-ledger schema frozen
      as Phase 16's read interface.

## Performance budget (fill from W1–W5 — this table is the deliverable)

| Path (reference machine, named)          | Naive   | Compiled | Ratio | Target      |
|------------------------------------------|---------|----------|-------|-------------|
| quanta ticks / ms (observed cells)       | ___     | ___      | ___   | ≥ 5× naive  |
| chemistry reactions / ms                 | ___     | ___      | ___   | ≥ 5× naive  |
| physics cell-steps / ms (GPU)            | n/a     | ___      | ---   | device-1st  |
| biology pop-steps / ms                   | ___     | ___      | ___   | ≥ 10× naive |
| society graph-steps / ms                 | ___     | ___      | ___   | ≥ 10× naive |
| agents ticked / ms                       | ___     | ___      | ___   | ≥ 3× naive  |
| ledger events / ms                       | ___     | ___      | ___   | ≥ 4× naive  |
| bus bytes / tick (causal lane)           | n/a     | ___      | ---   | fits budgets|
| money-world tick cost vs P14-ON          | ___     | ___      | ___   | ≥ 3× P14-ON |
| whole-world snapshot (money world)       | ___     | ___      | ___   | < 10 s      |
| full phase-acceptance corpus (nightly)   | ___     | ___      | ---   | overnight   |
| demo world interactive on one ref card   | n/a     | ___      | ---   | real-time   |

## Interface exposed to Phase 16 (the full emergent loop)

> Phase 16 may touch the world only through the frozen ledgers and
> event channels of Phases 0–13, exactly as always — Phase 15
> promises no new state and grants no new writes. What it hands over
> is certainty with numbers: measured throughput (atoms/agents/
> reactions per ms, reference machine named), tiered duty cycles,
> bus widths as budgets, error-budget spend meters per ledger, the
> replay chain pinned to build identity, and the existence suite as
> a standing proof that speed was bought without a lie. Phase 15's
> only API is "same world, one tick cheaper." Phase 16's charge is
> the first honest one: run the whole thing from nucleosynthesis to
> civilization at interactive speed, and let the numbers be the
> review.

## Verification strategy

1. **Unmodified-suite law:** Phase 14's existence suite hash-
   registered at its W7 is this phase's gate; the fifteen phases'
   acceptance suites are the ECS conversion's specification. No
   suite file may be edited to go green; suite-edit proposals go to
   the surprises ledger for review, not merged.
2. Torture-before-optimization: jitter/queue/partition injection
   lands as red tests **before** the kernels they attack are written
   (the P12 ordering discipline applied to the compiler itself).
3. Budget arithmetic is CI arithmetic: channel width == published
   budget (property tests), spend meters in the run record,
   exhaustion without a decisions entry = red.
4. Cross-runtime equivalence per D16: bit-identity only same-build;
   within-budget across builds — both directions asserted, never
   conflated (a green suite that quietly compares across builds is
   the phase's own gaslighting test inverted).
5. Surprises ledger: naive-vs-compiled ratios per tier (which layer
   surprised), bus headline ratio, partition boundaries the
   geography chose, which certificates fired on the adversarial
   seed, single-card demo headline, budget rows Phases 0–14 finally
   fill in.

## Sequencing

```
Wk 1-2          Wk 2-4              Wk 4-6               Wk 5-7         Wk 7-9
─────           ─────               ──────               ─────          ─────────
W1 store ECS    W2 tiered ticks    W3 device split      W4 chain v2    W6 existence-suite
(suites as      +S24 certificates  +deterministic GPU   +torture       gate + W7 freeze
 spec)          (upstream first)   +narrow bus          (build ids)    gate Phase 16
                                  (W5 measurement       (nightly       (W5 budget table
                                   runs throughout)     matrix)        complete)
```

## Risks

| Risk | Mitigation |
|---|---|
| Bit-identity vs GPU parallelism (the classic betrayal: "close enough" compilers) | determinism is the gate, not the fine print: fixed-order reductions, no float atomics, schedule seed-derived; where exactness is unaffordable, fixed-point channels whose widths are the published budgets (approximation is declared in bits, never hidden in epsilons) |
| ECS conversion silently eats ledger semantics | the fifteen suites are the spec; conversion is row-by-row auditable (segment diff vs naive snapshot); any red suite is a bug hunt, suite edits are quarantined for review |
| Error budgets compound across eras until meaning drains out | per-ledger spend meters in the run record; exhaustion is a decisions event, not a slider; adversarial certificate seed proves lying jumps are caught, not absorbed |
| Perf theater: numbers from curated microbenchmarks, world stays slow | throughput measured only inside suite harnesses; nightly regression ±5%; the single-card demo is a whole world, not a kernel |
| Causal events lost across the narrow bus under load | lossless causal lane by construction (backpressure, not drop); starvation test counts events on both sides; epistemic lane explicitly allowed to lag and measured doing it |
| Phase 15 becomes where the roadmap's promises get quietly downgraded | the only writable artifacts are contracts + budgets; downgrade proposals require decisions entries visible to the gate; the existence suite is immutable by hash |

**Gate:** Phase 16 starts when: the unmodified existence suite is
green against the compiled runtime (hash verified), all fifteen
phases' suites green post-conversion, the torture suite passes
(device jitter, queue randomization, partition reshuffle; chain
bit-identical same-build), cross-build equivalence lands within
budget on the full corpus, certificates fire correctly on the
adversarial seed with zero unsigned coarse reads, the perf ledger
table is complete and regressing nightly at ±5%, the single-card
demo world ticks interactively on the reference machine, D16 is in
`spec/decisions.md`, and the `runtime/` lines are frozen in
`spec/interfaces.md`.
