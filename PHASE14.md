# Phase 14 — Perception, LOD & Existence (the render/sim contract)

**Goal:** the engine stops pretending and says the quiet part as a
contract: **nothing is computed that no one could tell the difference
of, and no one believes finer than the world exists.** Phases 0–13
did this as engineering hygiene (jump-states, compressed agents,
histogram beliefs); Phase 14 makes it a *world-principle with an
owner*. The missing piece found while planning: the observation map
that D4's collapse accounting and Phase 1's tier scheduler consume has
always been an **external scripted input** — the `probe/` observer
bubble "stands in for Phase 14" (seam S21). This phase *is* that
replacement: the map becomes a function of the world's own perceivers
— gaze (line-of-sight against Phase 7 heightfields), Phase 9's brain
budgets grown into a constant per-being **frame budget** (seam S22:
allocation from *simulated* scene complexity, never host wall-clock,
rider on the replay chain), and testimony that makes distant regions
real. Physical collapse stays interaction-based exactly as D4 ruled —
this phase adds **epistemic** records beside it, two levels that must
reconcile against the physical ledger with zero contradiction (D14).
Existence gets a center (perceptual overlap), a resolution schedule
(unobserved decays to histogram), and a witness: written records are
physical observers too, so a literate polity literally persists at
finer resolution — memory extended onto matter, measured. And the
phase pays rent: the governor's pruning must cut the money world's
tick cost ≥ 40% at *epistemic parity*, measured with the honesty of
the P12 ordering tests — the phase that makes everything cheaper
except itself.

**Prerequisites (hard gate, from Phase 13 + seam round eight):**

- Phase 13 gate green: the `infra::` freeze line (this phase may
  render and prune, never move) and its two acceptance pre-orders:
  pruning changes no ledger beyond tolerance, and someone notices
  when the lights-analog go out unobserved.
- Seam round eight: **S21** wording landed (PHASE1.md annotated
  same-sitting: the bubble is a test fixture; the Phase 14 gaze map
  becomes the world-internal source for D4 accounting + tier
  scheduling; D14 drafted in `spec/decisions.md` at gate). **S22**
  landed upstream in the replay chain: frame-budget allocation traces
  deterministic from seed + simulated complexity, hashed into the
  chain (sibling contract of S16/D10); lint: no host-clock reads in
  any allocation path.
- S7/S16 machinery + honesty tax extended to *beliefs* (existence
  tax: a compressed believer's restored beliefs must survive
  demotion bit-exactly — Phase 8's compression discipline recursed
  onto knowledge itself).
- Phase 9 brain budgets + compressed-agent machinery; Phase 10
  claims/net ledgers (testimony channel); Phase 11 intelligibility
  matrix; Phase 12 claims-vs-replication machinery (propaganda is
  this phase's adversarial case).

**Definition of done:** the observer bubble is deleted from the demo
and the world does not notice: **the observation map now comes from
the agents themselves** (gaze sets, instrument reads, archive
consults), the scripted bubble survives only as a green regression
fixture, and D4's collapse statistics are bit-identical under a
gaze-derived map for the same scripted attention track (the S21
equivalence test — the replacement must be exact where the maps
agree). An agent staring at a detector-analog in the computer-belt
owns a *knowledge record* of the outcome; a second agent who didn't
see the dial holds a different record; their testimony round-trip
reconciles both against the physical ledger with **zero
contradictions**, and the engine's lint can name which records were
priors (confabulation is prior-sampling, ledger-flagged, never
silently believed). Inattentional blindness is a real measurement:
budget-starved agents miss a wall-analog changing color while a
social goal eats their frame budget, miss-rate correlates with the
allocation trace (sign asserted), and the same minute under threat
is *remembered denser* (records-per-scene in the memory ledger —
experienced time as a stat, not a metaphor). The trade city loses
its last resident observer and **its resolution schedule decays to
histogram on the gaze-overlap clock** — meanwhile the archive town
across the pass, unread but *recorded*, holds a measurably finer
floor (written records as physical witnesses: literacy extends
existence, the two decay schedules reported side by side as the
phase's signature figure); returnees find the ledger intact and
their own memory-records of the gap **refutable by the archive**.
A rumor-analog crosses the intelligibility matrix the way Phase 11
says it must: fidelity decays with hops × barrier, two hops across a
language border collapse measurably more than one hop inside it —
and when the telegraph-analog arrives, a knowledge-timestamp finally
**precedes every physical arrival-timestamp** for a distant event
(news outruns weather: the world begins living in its information,
the Phase 12 propaganda loop inherits a faster horse). Three
witnesses to a collapse-analog (Phase 13's cascade) encode
*complementary* subsets — line-of-sight occlusion geometry from the
heightfield predicts who missed what — and their testimonies
converge to the union within tolerance, the occluded agent filling
gaps with ledger-flagged priors. The anomaly-injection test closes
existence: an unobserved light-analog failure is discovered by the
**meter record, not the physics** — uncomputed is not unrecorded, and
the difference is visible in the ledgers. Finally the rent: the same
money world, governor ON, drops ≥ 40% tick cost at epistemic parity
(blinded before/after comparison, protocol fixed *before*
optimizing), the full existence suite green, and no agent, archive
or replay can tell the compiled world from the naive one beyond
published error budgets.

---

## Scale contract

- Observation map: ~10² regions × instantiated observers; compressed
  agents contribute *scheduled* gaze (cohort-level attention
  histograms), not per-tick rays.
- Epistemic records: full (value, resolution, confidence) triples
  only for on-scene agents; elsewhere beliefs are region-histograms
  with confidence — belief compression mirrors body compression, and
  the existence tax audits both.
- Gaze = occlusion queries against Phase 7 heightfields at the
  region's *current* resolution (you cannot be occluded below the
  resolution you exist at — resolution and belief stay coupled).
- Allocation traces: ~10⁴ agents × coarse budget class per tick —
  compressed as class-histograms; the hash rides the chain, the
  detail does not.
- Acceptance rigs: the bubble-equivalence strip, the
  inattentional-balance pair, the vanishing city vs archive town,
  the rumor pass, the witness triangle, the anomaly-injection room,
  the rent measurement (money world, governor ON/OFF).

## Architecture

Two packages: one new (`mind/`), one engine-side scheduler (`exist/`)
that is explicitly *allowed to touch the tier scheduler* because the
tier scheduler was always waiting for this input:

```
sim/
  mind/
    gaze/       perceiver geometry: position × facing × light budget
                (Phase 6 optics) against Phase 7 heightfield
                occlusion; instrument-analog extension (a telescope
                is a gaze with better range - Phase 10 artifacts as
                gaze modifiers); archive consults = gaze onto records;
                reality is rendered only to what is observable and
                relevant - this block is where that clause of the
                roadmap becomes code
    budget/     the constant per-being frame budget (roadmap law);
                allocation policy inherited from Phase 9 brain
                budgets (threat/novelty salience = learned/evolved);
                scene complexity from the region's active-entity
                ledger (never host timing - S22); the roadmap's
                per-agent *perceived frame rate* as a real stat =
                allocation / complexity; allocation traces ->
                replay chain
    memory/     epistemic ledgers: (value, resolution, confidence)
                records; the band-memory sweep read path (agent
                memory literally reads the band-ladder compressed
                representations - fidelity bounded by band + tier,
                the roadmap's "sweep the band memory" made literal);
                forgetting = fidelity decay curves; written records
                = physical witnesses with their own decay (Phase 9
                surface-mark persistence + Phase 10 storage)
    echo/       testimony: claims-ledger records (Phase 10) about
                world-state, propagated on net/ (Phase 10) through
                the intelligibility matrix (Phase 11); fidelity
                decay = hops × barrier × time; reconciliation on
                contact = belief merge with provenance, NOT averaging
                (the merge keeps both records until the physical
                ledger arbitrates - the anti-gaslighting design rule);
                culture = the long-time tail of the same propagation,
                variants selected for retained-not-true (Phase 11
                meaning machinery rides this channel; news is its
                fast headline)
  exist/
    governor/   the LOD scheduler: existence resolution = f(gaze
                overlap, causal proximity to observed regions, record
                anchoring) - detail connects only to what is
                close-related, everything else decays to compressed
                state (roadmap law, verbatim); prune futures to
                jump/histogram (never
                re-sorts the past - pruning schedules forward only);
                hysteresis bands against oscillation; rent accounting
    map/        the observation map itself - S21's artifact: the
                world-internal input to D4 logged-interaction
                accounting + Phase 1 tier scheduler; scripted bubble
                demoted to test fixture
    invariant/  the render/sim contract as CI: (a) no ledger moves
                beyond published error budgets when pruning toggles;
                (b) NO BELIEF FINER THAN EXISTENCE: the epistemic
                ledger may not hold detail at resolution r unless
                the physical ledger held it at r when recorded, or
                the belief is confidence-labeled prior - linted,
                every tick
```

Data rules:

- **Two-level observation, one spine.** Physical collapse: D4
  unchanged, interaction-based, anti-mystical (the word
  "consciousness" is banned below the test layer, grep gate).
  Epistemic collapse: knowledge records enter only via gaze/echo
  channels. The reconciliation lint is the only bridge.
- **The governor moves resolution, not outcomes** — beyond published
  error budgets. The error budget is the licensed freedom; outside
  it, ledger conservation is the whole law (Phase 13's freeze line,
  now with an executor).
- **Beliefs are records, not fields.** No global "what everyone
  knows" matrix; there are only agents' ledgers and the physical
  records between them. Shared world = reconciled overlap, computed
  when needed.
- **Allocation is simulated before it is felt.** Frame budgets come
  from scene-complexity ledgers; a host hiccup may change wall-time
  of the run, never the world's experienced time (S22; CI lint).

## Work packages

W1 builds gaze + budget and replaces the bubble (S21 equivalence
first — the phase must prove its predecessor green before it is
allowed to be the map); W2 needs W1 (records need witnesses); W3 the
governor needs W2's parity metric to prove rent; W4 rides W2+W3; W5
needs W1's map + Phase 1 collapse stats; W6 rigs; W7 freeze.

### W1 — Gaze, frame budgets, the bubble's funeral (S21/S22 upstream first)

- [ ] Gaze sets + occlusion queries; budget allocation policy +
      fps-analog stat; allocation-trace writer into the replay chain
      (S22 red-first).
- [ ] **Tests:** *bubble equivalence* — scripted attention track,
      gaze map, D4 collapse statistics + tier schedule bit-identical
      where maps agree; S22 determinism: allocation traces replay
      identical, host-clock lint green (inject a fake clock skew:
      world-time unchanged); inattentional blindness miss-rate ~
      allocation (sign test); threat-minute memory-density test.

### W2 — Memory: witnesses, records, forgetting

- [ ] Epistemic ledgers + band-memory sweep path; fidelity decay;
      written-record witnesses with Phase 9/10 physical decay.
- [ ] **Tests:** belief-finer-than-existence lint (inject the
      violation, catch it); archive-refutes-memory test (returnees'
      priors lose to the record under reconciliation); confabulation
      flagged as prior, never believed as record; existence tax:
      compressed believer's beliefs restored bit-exact.

### W3 — Governor + rent

- [ ] Resolution scheduler with hysteresis; prune-to-jump path reuse
      (Phase 0/1 jump machinery, first real-world customer); rent
      accounting + epistemic parity metric defined BEFORE optimizing
      (blinded protocol, fixed in the test file first).
- [ ] **Tests:** the two pre-ordered acceptance lines from Phase 13
      executed (toggle-pruning ledger-diff within budgets; anomaly
      found by meter, not physics — uncomputed ≠ unrecorded); rent:
      ≥ 40% tick-cost cut at parity, both numbers reported; no
      resolution oscillation under hysteresis (adversarial gaze
      dither).

### W4 — Echo: rumor, news, reconciliation

- [ ] Testimony records on net through the intelligibility matrix;
      merge-with-provenance reconciliation; news latency model.
- [ ] **Tests:** rumor fidelity ~ hops × barrier matrix (correlation
      with Phase 11's matrix, no new tuning knob); witness triangle
      converges to union, occluder's gaps stay priors (geometry
      predicts who missed what — heightfield is the oracle);
      telegraph-analog event: knowledge-timestamp precedes
      physical-timestamp (the world's first anachronism, timed).

### W5 — Quantum hook: two levels, zero contradiction

- [ ] Gaze-derived observation map live for D4 + tier scheduler
      (bubble remains fixture); epistemic records of quantum-scale
      outcomes via instrument-analog gaze.
- [ ] **Tests:** detector-analog reconciliation: disagreeing
      knowledge records, zero contradictions vs physical ledger
      (the S21 keystone); "consciousness" grep gate green; scripted
      bubble suite still green (fixture regression).

### W6 — Existence phenomenology + acceptance harness

- [ ] Vanishing city vs archive town rig (dual decay schedules — the
      signature figure); propaganda coupling: Phase 12's
      virulence/veracity race re-run with W4 latencies (the loop
      inherits its speed from this phase — reported, not set).
- [ ] Full existence suite wired; compiled-vs-naive indistinguish-
      ability battery (state diffs + agent-belief diffs, both within
      budget).

### W7 — Freeze + decisions

- [ ] D14 (two-level observation semantics; observation map as sole
      world-internal source) and D15 (frame-budget determinism +
      allocation-trace chain, S22) into `spec/decisions.md`.
- [ ] Freeze `mind::`/`exist::` contracts (below).

## Performance budget (fill from W1–W3)

| Path                                          | Budget              | Measured |
|-----------------------------------------------|---------------------|----------|
| gaze occlusion query (region at res r)        | < 5 µs              | ___      |
| observation map recompute (10² regions)       | < 2 ms / tick       | ___      |
| allocation trace write (class-histogram)      | < 1 µs / tick       | ___      |
| epistemic step (10⁴ beliefs, compressed)      | < 20 ms / tick      | ___      |
| governor decision pass                        | < 1 ms / tick       | ___      |
| testimony diffusion (10⁴ records + net)       | < 3 ms / tick       | ___      |
| **rent: money-world tick cost, governor ON**  | **≥ 40% below OFF** | ___      |
| phase acceptance suite (offline)              | < 2 h wall          | ___      |
| CI-fast bubble-equivalence + S22 lint         | < 10 min wall       | ___      |

## Interface exposed to Phase 15 (the hyperoptimized runtime)

> Phase 15 may read the whole world — it is its compiler. It may
> write **scheduling, batching and offload decisions only**, and must
> prove each one preserves: (a) the replay hash chain bit-identical,
> **including S22 allocation traces**; (b) every Phase 0–13 ledger
> within its published error budget; (c) the epistemic invariant —
> no agent believes finer than the compiled world exists. Phase 14
> freezes the *semantic* LOD contract (what may be skipped and what
> it costs, region by region); Phase 15 discovers the *mechanical*
> one, an order of magnitude cheaper. The gate is unfair on purpose:
> Phase 15 passes when **this phase's own existence suite runs
> unmodified against its runtime** — the world must not notice it was
> compiled, and no one inside it, including the replayers, may be
> able to tell.

## Verification strategy

1. Oracle: `tests/oracle/exist/` — bubble-equivalence (bit-identity
   where maps agree), belief-finer-than-existence lint, ledger-diff
   under pruning toggles vs published budgets, reconciliation
   zero-contradiction, rumor fidelity vs the *frozen* Phase 11
   matrix (no refitting).
2. Blinded parity protocol: the epistemic-parity metric and its
   comparison script land in W3's test file **before** the governor
   optimization exists — the rent number cannot shop for a softer
   metric (the P12 ordering-test discipline turned on this phase's
   own economics).
3. Two-clock determinism: every rig runs twice — once with injected
   host-clock jitter; world diffs must be empty (S22 as a suite-wide
   gate, not a unit test).
4. Existence suite = Phase 15's unmodified gate (contract: the suite
   file is frozen at W7, hash-registered in `spec/interfaces.md`).
5. Surprises ledger: which regions the governor starves first,
   literacy-anchor schedule gap (the figure), which rumor variants
   survive the pass, whether any polity's religion-analog claims the
   unobserved world (Phase 11 meaning machinery meeting W3 — report
   the theology, lint the physics), measured rent %, oscillation
   incidents caught by hysteresis.

## Sequencing

```
Wk 1-2             Wk 2-4            Wk 3-6               Wk 5-7          Wk 7-9
─────              ─────             ──────               ─────           ─────────
W1 gaze+budget     W2 memory         W3 governor + rent   W4 echo         W6 phenomenology
(S21 equivalence   (band sweep,      (parity metric       (rumor/news,    +acceptance
 first, S22        witnesses,        first, blinded)      witness tri-    +W7 freeze
 trace landed)     lint)                                  angle)          gate Phase 15
                                                          W5 quantum
                                                          hook (parallel
                                                          from wk 4)
```

## Risks

| Risk | Mitigation |
|---|---|
| Host-clock contamination smuggles nondeterminism into experienced time | S22 chain + suite-wide two-clock gate (every rig replayed with jitter); lint bans wall-clock reads in allocation paths, CI-enforced |
| Observation re-mystified (mind-over-matter collapse creeps in) | D14's two-level wording, "consciousness" banned below tests, reconciliation lint is the only bridge between levels; W5 fixture regression keeps D4's ghost dead |
| Governor oscillation makes resolution a toy (regions flicker) | hysteresis bands + adversarial dither test; oscillation incidents are surprise-ledger entries, not silent retunes |
| Epistemic ledgers explode (beliefs × regions × agents) | belief compression mirrors body compression; existence tax audits restored beliefs bit-exactly; full triples only for on-scene agents |
| Rent gamed by a soft parity metric | parity metric frozen before optimization (blinded protocol in W3's test file); the suite Phase 15 inherits cannot be edited after W7 (hash-registered) |
| Phase 14 itself becomes the expensive phase | rent accounting includes this phase's own overhead; perf table row for every hot path; the phase that prunes everything must also prune itself |

**Gate:** Phase 15 starts when: the existence suite is green
offline-nightly (bubble equivalence, S22 two-clock determinism,
inattentional sign test, belief lint, dual decay schedules, rumor
fidelity, witness convergence, detector reconciliation, anomaly-by-
meter, ≥ 40% rent at blinded parity), S22's chain contract merged
upstream, D14/D15 in `spec/decisions.md`, and the `mind::`/`exist::`
lines plus the suite hash are frozen in `spec/interfaces.md`.
