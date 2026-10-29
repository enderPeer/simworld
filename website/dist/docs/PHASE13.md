# Phase 13 — Infrastructure, Industry, Externalities

**Goal:** the world learns to move itself — and discovers, with
ledger-proof receipts, that every useful flow casts a shadow.
Infrastructure is **owned artifacts with a health history** (Phase 12's
S18 relation finally doing infrastructure duty): roads chosen by
Phase 7 orography, maintenance debt accumulating from real stress
events, collapse as a graph cascade no one scheduled. Traffic is
agents-on-edges whose **driving conventions are path-dependent
coordination equilibria** — which side you drive on is an accident of
history locked in by coordination cost, and the accident-spike where
two conventions meet is this phase's signature measurement. Industry
scales the Phase 10 machine fleet against Phase 7 geology: ore grades
deplete in the order the world actually deposited them, net-energy
(EROEI-analog) is *computed* from the mine-to-smelter joule chain, and
recycling rates emerge when the energy ledger makes waste cheaper than
rock. And the externality thesis, the whole point: emissions, dust,
metals, plastics-analog, radiation and orbit trash are **flux events
that finally carry their producer** (seam S19) and move at
street resolution (seam S20), so that liability (Phase 12) can cite
chemistry (Phases 3/4), transport (Phase 7), and harm (Phases 8/11) in
one citation chain — the first full-stack policy in the world's
history, enforceable as a computation. Disaster, when it comes, is
arithmetic: hazard (Phase 7 extremes) × exposure (where the phase's
buildings stand) × vulnerability (maintenance debt) — all three
already in ledgers, none of them named "risk" by anyone.

**Prerequisites (hard gate, from Phase 12 + seam round seven):**

- Phase 12 gate green: ownership ledger (S18 merged upstream),
  liability record class, enforcement graphs, price-analog fields.
- Seam round seven, both land upstream **before W4 opens**:
  - **S19** — flux events gain sparse **producer attribution tags**
    (agent/cohort refs above a production threshold, riding the
    Phase 7/8 flux-event contract); liability without attribution is
    a tribunal reading a ledger with the signatures whited out.
  - **S20** — Phase 7 climate gains a **bubble-scale near-surface
    tracer channel** (advect-diffect-deposit at settlement resolution;
    the coarse columns cannot answer "bad air" at street scale, and
    dose-response without local concentration is astrology).
- S7 LOD discipline for dense graphs (road/pipe nets, debris shells).
- Phase 10 machine/grid/orbit ledgers; Phase 11 health dose-response
  axis and calibration spectra; S2 (viscoelastic creep) merged —
  infrastructure fatigue leans on it; S13 articulated bodies for
  moving machinery.

**Definition of done:** on the money world, the rail/road-analog grid
pushes through Phase 7 orography and **the terrain authors the
engineering**: cut/fill volumes computed from the real heightfield,
pass-drawn lines where the mountain decided the pass, gradients that
select what the line can haul. Early lines lock **driving-convention
equilibria** — arbitrary at origin (two seeds, same geography, opposite
sides: asserted), then expensive to leave; travellers crossing a
convention border show a measurable collision-analog spike that decays
as predictions re-fit (borders are where culture becomes visible in
the accident ledger). Food-sheds size themselves: spoilage-analog
rates are Phase 4 chemistry at Phase 7 temperatures, so the radius a
perishable-analog can be hauled is a **thermal fact**; when a
refrigeration-analog spread event (Phase 10 machine class) lands, the
food-shed visibly re-draws and market-analog calendars flatten
seasonality. The aquifer-analog story: withdrawals exceed Phase 7
recharge, the water-table series bends down, wells deepen as ledger
events, and the settlement **migrates down-gradient without anyone
voting on hydrology** — then sanitation-analog and water-recycling-
analog close the loop and the epidemic-analog curve in the health
ledger dies a plumbing death. The emissions arc, the phase's spine:
stack-analog point sources tag their output (S19), S20 plumes carry
dust-analog and gas-analog downwind at street resolution, deposition
writes to Phase 7 surface ledgers, acid-deposition-analog shifts
lake-analog chemistry (Phase 4) and its biology (Phase 8) **inside a
different polity than the one that emitted** — and now the full-stack
citation test runs: one liability record cites Phase 2/3 isotope
signatures, Phase 4 speciation, Phase 7 transport lag, Phase 8/11 harm
curves, and a court-analog can execute enforcement **against the
atmosphere's bookkeeping**. When the policy-analog curbs bite, the
deposition ledger recovers **with the transport lag preserved** —
the recovery arrives late in the same books that convicted, both lags
reported, neither engineered. Waste streams are output ledgers nobody
owns until somebody does: landfill-analog capacity as owned-artifact
bookkeeping, and recycling-analog rates climbing **exactly when the
energy ledger makes waste-stream joules cheaper than depletion-grade
ore joules** (the circular economy as an EROEI crossover, not a
virtue — the crossover point is a surprise-ledger entry). The
damage-vector sweep runs on dose-response honestly: industrial
metal-analogs and dust-analogs move occupational exposure ledgers
(body-integrated concentration × time in work-cells) and the belt
town's Phase 11 calibration spectrum shifts **while its leisure
quarter's does not** (the gradient is the test); polymer-analog
fragments into the particle ledger with Phase 5 persistence times and
the exposure ledger fills **with effects honestly left unknown**
(we measure exposure, we do not invent harm — the honesty rule);
Phase 10 nuclear-era legacy sites stay dose vectors in the Phase 2
ionization ledger for generations, history's long tail as engine
fact. Infrastructure-induced harm, no pollution required: deferred
maintenance debt compounds in artifact health until a routine load
event **collapses the weakest link and the failure cascades along the
network graph** — the identical storm-analog landing on the intact
network is a non-event (disaster = hazard × exposure × vulnerability,
computed, reported, nobody's fault and everybody's ledger), and
occupational damage-analog concentrates in the exposure ledger of the
crew that skipped inspection. In orbit, launch-analog traffic leaves a
debris shell that Kessler-cascades if the shell histogram lets it,
reentry-analog sinks the losers, and launch insurance-analog prices
climb the shell's book — the orbital commons as an unowned ledger
account with liability records opening a counter-entry against no
owner at all, which is precisely the policy problem the ledgers
finally make visible.

---

## Scale contract

- Infrastructure graphs: ~10⁴ owned structures + ~10⁵ edge-miles of
  road/pipe/grid per developed region, all on the Phase 7 surface
  grid; health states are event-accumulated (no per-pixel physics
  below Phase 6/8 granularity — artifacts carry accumulators, not PDEs).
- S20 tracers: bubble-local grid ~10× finer than the climate columns,
  passive advect-diffect-deposit only (no in-tracer chemistry —
  speciation stays Phase 4 at column or settlement resolution).
- Traffic: flow as agent-path events on the graph, capacity/degradation
  from edge material + gradient; no fluid-dynamic traffic modeling
  below jam-analog event resolution.
- Debris shells: S7 discipline — shell histogram + objects-of-interest;
  full tracks only inside instantiated conjunction windows.
- Acceptance rigs: the terrain-line rail strip, the convention-border
  pair-cities, the aquifer settlement, the full-stack policy basin,
  the cascade network, the orbit shell.

## Architecture

One new package, everything else borrowed:

```
sim/
  infra/
    build/      structures - houses-analog through civic works - as
                owned artifacts (Phase 12 relation);
                siting against Phase 7 heightfield (cut/fill volume
                = computed cost event), foundations on Phase 5 soils;
                districts = urban-fabric cell clusters (Phase 11
                polis overlays them for free)
    health/     degradation accumulators: threshold-crossing load/
                stress/traffic events integrate into artifact health
                (S2 creep supplies the slow term); maintenance
                obligations = liability-shaped records against own
                assets; neglect is a visible ledger slope
    flow/       traffic on the graph; conventions = learned
                expectation attractors (Phase 11 norms machinery on
                routing coordinates), spatially bounded, border cost
                = prediction error = collisions; freight chains =
                transfer-event paths with Phase 4 spoilage kinetics
                at Phase 7 temperatures; cold-chain-analog = Phase 10
                machine class extending the thermal radius
    metabolism/ the region as flux machine: food/water/energy in,
                waste out, all on Phase 7 reservoir ledgers; aquifer
                drawdown = withdrawal vs recharge series; recycling
                re-entry events compete with mine-analog streams on
                the energy ledger (EROEI-analog computed across
                mine→smelt→build joules, depletion order emergent
                from Phase 7 ore-grade distributions)
    harm/       S19 consumers: exposure ledgers (agent body × time ×
                local concentration from S20 plumes), dose-response
                into Phase 11 health axis; occupational = exposure
                conditioned on work-cell membership; radiation from
                Phase 2 fields, particle/polymer ledgers from Phase 5
                persistence; EXPOSURE-EFFECT HONESTY RULE: effects
                exist only where a dose-response curve exists in the
                Phase 11 calibration spectrum, else exposure logs
                without harm claims
    hazard/     Phase 7 extremes over Phase 13 exposure maps:
                floodplain build-events shift computed risk the way
                insurance shifts nothing; network cascade failure at
                weak links (graph propagation of load-onto-failed-
                neighbors); orbit debris shells (Phase 10 astro
                ledger + S7 histograms, Kessler as shell kinetics)
    liability/  Phase 12 record class pointed at commons accounts:
                citations resolve across Phase 2 isotope sigs →
                Phase 4 speciation → Phase 7 transport → Phase 8/11
                harm; unowned accounts (air shell, aquifer, orbit)
                get liability counter-entries — the ledger admits it
                has no owner to sue, visibly
```

Data rules:

- **Producers tag their output.** Industry-scale flux events carry S19
  attribution; natural fluxes stay untagged — the tag's absence is
  load-bearing data (background vs anthropogenic is a ledger
  computation, isotope-analog signatures included).
- **Health is an accumulator, not a field.** Structures carry scalar
  health + event provenance; the physics stays where it was (Phase
  6/8), accumulators cross thresholds. Grep gate: no stress PDEs in
  `sim/infra/`.
- **Exposure is never effect.** Harm requires a Phase 11 curve. New
  agents (polymer fragments) without curves log exposure forever —
  the honesty rule is CI-enforceable: a harm claim citing no curve
  fails the ledger lint.
- **Conventions have no rule table.** No driving side exists anywhere
  until two agents' predictions collide; the engine holds
  expectations, never traffic law.

## Work packages

W1 builds; W2 flows over W1; W3 scales W2's metabolism; W4 needs S19+S20
landed + W2 flows (sources to plume); W5 overlays W1+W3; W6 chains
W4+W5; W7 last.

### W1 — Build, sit, degrade, maintain

- [ ] Owned-structure record + cut/fill cost events from heightfield;
      gradients selecting haulage; foundation classes on Phase 5
      soils.
- [ ] Health accumulators (traffic/stress thresholds, S2 slow term);
      maintenance obligation records; neglect-slope statistic.
- [ ] **Tests:** line-choice is terrain-determined (two runs, same
      seed, same pass; different orography, different line — reported
      volumes); deferred-maintenance debt predicts failure sequence
      of a bridge-analog panel (rank correlation, ordering test);
      collapse cascades only past the debt threshold, sub-threshold
      loads are silent.

### W2 — Flow: conventions, food, water, waste

- [ ] Convention equilibria on routing coordinates; border prediction-
      error spikes; freight chains with spoilage kinetics.
- [ ] Aquifer drawdown series; sanitation and water recycling loop
      closure (the pipe class that failed as drawdown reopens as
      supply); waste-stream ownership events.
- [ ] **Tests:** two seeds same geography → opposite convention sides
      (arbitrariness asserted, no scripted winner); border collision-
      spike decays with re-fit half-life (reported); food-shed radius
      tracks a temperature-analog shift monotonically (sign asserted,
      magnitude reported); recycling-rate crossover follows the
      energy-price comparison within lag (the EROEI handshake, W3
      closes it).

### W3 — Metabolism: fleets, grids, net energy, depletion

- [ ] Generation fleet from Phase 10 machine ledgers; energy
      distribution networks as owned edge class (last-mile deliverance
      priced in the same flux ledger); inter-city grid ties;
      load-frequency heartbeat series.
- [ ] EROEI-analog computed net-energetics per chain; depletion-order
      realism from ore-grade distributions.
- [ ] **Tests:** net-energy series stays positive for the fleet mix
      that survives and **goes non-positive for the one that doesn't**
      (the accounting discriminates, bands not targets); depletion
      order matches grade distribution (richest-first is emergent,
      asserted by rank test); load-frequency statistics show demand
      structure without a dispatch oracle.

### W4 — Damage vectors (needs S19 + S20 upstream first)

- [ ] Producer tags on flux events (S19 upstream tests red-first);
      S20 plume channel wired to harm/ exposure integration;
      occupational ledger as work-cell-conditioned exposure.
- [ ] Metal/gas/dust/particle dose-response wiring to Phase 11 axis;
      polymer-analog fragmentation ledger (exposure-only, honesty
      rule); radiation legacy sites from Phase 2 fields.
- [ ] **Tests:** full-stack citation chain executes (one liability
      record resolves across isotope → speciation → transport lag →
      harm curve — the phase's keystone test); belt-town health
      distribution shifts while leisure quarter holds (spatial
      gradient is the assertion); background-vs-anthropogenic
      separation recovers the tagged fraction from the ledger alone;
      exposure-only agents produce zero harm claims (lint test).

### W5 — Hazards, cascades, orbital commons

- [ ] Extreme-event overlays; floodplain build-event risk shift;
      network cascade propagation; debris shell kinetics.
- [ ] **Tests:** identical storm, two networks (intact vs debt-ripe):
      event vs disaster from the same hazard (the exposure ×
      vulnerability arithmetic); cascade size bands under seeded
      determinism; Kessler-analog threshold exists on shell density
      (above: cascade, below: decay — both sides run); insurance-
      analog price tracks shell book (correlation reported).

### W6 — Full-stack policy + recovery

- [ ] Liability citations against commons accounts; court-analog
      enforcement as ledger computation; curbs propagating back
      through emission ledgers.
- [ ] **Tests:** deposition recovers with **transport lag preserved**
      after the curb (late arrival is the assertion — the atmosphere
      does not obey legislative calendars); enforcement against an
      unowned account (orbit shell) visibly fails-then-legislates:
      the world invents an owner-actor or an injunction, both allowed,
      whatever happens is reported.

### W7 — Acceptance rigs + freeze

- [ ] Six rigs wired; attribution compression (D13) into
      `spec/decisions.md`; honesty tax extended to exposure and
      liability ledgers.
- [ ] Freeze `infra::` contract (below).

## Performance budget (fill from W1–W4)

| Path                                          | Budget              | Measured |
|-----------------------------------------------|---------------------|----------|
| structure build/degrade event                 | < 2 µs              | ___      |
| health accumulator step (10⁴ structures)      | < 15 ms / tick      | ___      |
| traffic step (10⁵ edge paths, jam events)     | < 30 ms / tick      | ___      |
| S20 tracer step (bubble 64²×4, passive)       | < 25 ms / tick      | ___      |
| exposure integration (10⁴ agents)             | < 10 ms / tick      | ---      |
| cascade recompute (failed link)               | < 5 ms / event      | ___      |
| liability citation resolve (full stack)       | < 200 ms / case     | ___      |
| phase acceptance suite (offline)              | < 2.5 h wall        | ___      |
| CI-fast full-stack policy basin               | < 20 min wall       | ___      |

## Interface exposed to Phase 14 (perception, LOD, existence)

> Phase 14 may read everything this phase built and everything before
> it: the infrastructure graph with health + maintenance debt,
> exposure and liability ledgers, convention atlas, depletion and
> net-energy series, commons accounts with their counter-entries.
> Phase 14 may write **perception and existence events only**: who
> knows what about which cell, at what resolution, and what gets
> computed when nobody looks. Phase 14 renders and prunes the world;
> it never moves it — every LOD shortcut must preserve Phases 7–13's
> ledgers within published error budgets (S7's discipline generalized
> to existence itself). This phase's dense, attributed,
> liability-carrying graph is precisely the thing that must become
> cheap to perceive: the first Phase 14 acceptance test is that its
> pruning changes no ledger beyond tolerance, and the second is that
> *someone notices when the lights-analog go out unobserved*.

## Verification strategy

1. Oracle: `tests/oracle/infra/` — cut/fill volumes vs heightfield
   geometry, spoilage monotone in temperature (Arrhenius-analog
   sign test), EROEI bookkeeping closes (joules out ≥ ledger
   assertion), attribution recovers tagged fraction, dose-response
   monotonicity, cascade determinism under seed pinning.
2. **Full-stack citation keystone:** one policy case must resolve
   across Phases 2/3 → 4 → 7 → 8/11 → 12 ledgers or the phase is
   not done; the citation chain is data, replayable and diffable.
3. Honesty lints in CI: harm claims require curves (W4 rule);
   exposure-only agents never appear as harm claimants;
   exposure-vs-effect report published per run.
4. Conservation supertest reused: Phase 7/8 abiotic books balance
   with industry ON (attribution tags must not create flux —
   bookkeeping heresy test, Phase 12 pattern extended upstream).
5. Surprises ledger: which side of the road each seed chose, city
   migration routes, recycling crossover dates, Kessler yes/no,
   belt-town health half-lives, whether any polity sues the sky
   (unowned-account testaments), policy-recovery lag values.

## Sequencing

```
Wk 1-2          Wk 2-4                 Wk 4-6               Wk 5-7          Wk 7-9
─────           ─────                  ──────               ─────           ─────────
W1 build/       W2 flow + aquifer      W3 metabolism        W5 hazards      W7 rigs
health          (convention pair       +EROEI/depletion     +cascades       +freeze
                early)                                     W4 damage       gate Phase 14
                 (S19/S20 upstream     (handshake with      vectors         (W6 keystone
                  land here, wk 2)      W2 recycling)        (needs S20      before W7)
                                                            plumes)
```

## Risks

| Risk | Mitigation |
|---|---|
| Externality suite reads as advocacy with numbers | mechanisms + ledgers only; enforcement cost reported beside harm cost; policy outcomes emergent, none scripted; honesty rule CI-linted (exposure ≠ effect) |
| S19 attribution cost explodes on fine flux events | sparse tags above production threshold only; cohort-level tags under compression with error budgets (D13); honesty tax nightly catches tag drift |
| S20 plumes blow the tick budget | passive transport only (no reaction chemistry in-plume), bubble gating inherited from Phase 7 lazy machinery, perf table row is a gate not a wish |
| Cascade and Kessler tests go flaky | seeded determinism + banded cascade sizes, instantiated conjunction windows only; both thresholds demonstrated from both sides |
| Convention test accidentally scripts the side | seeds fix only geography + early flows; arbitrariness asserted via two-seed divergence; no side-named constant may exist (grep gate) |
| Depletion realism collapses into Malthus-scripted doom | no scripted substitutions: replacement technologies emerge only via Phase 10 claims channel, and their appearance rate is reported, not tuned; runs may end in boom or bust, the ledger keeps whichever score is true |

**Gate:** Phase 14 starts when: the phase acceptance suite is green
offline-nightly (terrain-line determinism, convention arbitrariness
pair, aquifer migration ordering, food-shed temperature monotonicity,
EROEI discriminant, full-stack citation keystone, two-network storm
pair, Kessler both-sides, recovery-lag preservation), S19/S20 upstream
tests merged, honesty lints pass in CI, D13 is in
`spec/decisions.md`, and the `infra::` line is frozen in
`spec/interfaces.md`.
