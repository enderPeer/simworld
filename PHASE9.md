# Phase 9 — First Humans & Epochs of Civilization

**Goal:** agents and the first epochs, from the same layers as
everything else. A forager lineage of Phase 8 acquires **agency** —
budget-gated policies over sense transductions, writing only momentum,
contact and flux events — and civilization's first acts **fall out of
physics, chemistry and geography**: lightning ignites the savanna,
cooking raises the brain's share of the energy budget, fracture
geometry gives edges that butcher better, ore where it lies decides who
gets bronze, and foraging pressure alone drifts plants into crops. No
epoch is a tech tree; an epoch is what the ledgers look like after ten
thousand years of agents maximizing budgets. The acceptance run must
end *before* industry and must contain **nothing that would block it** —
"future: whatever emerges next, unplanned" is a testable property.
Scope line (like Phase 8's "humans are Phase 9's problem"): the
roadmap's era list is satisfied through **professions**; "modern times:
industry, car industry, medical industry" are Phase 10 (the technology
that makes them possible) and Phase 13 (their externalities) deliverables —
Phase 9 ends at the plateau plus the openness assertion.

**Prerequisites (hard gate, from Phase 8 + seam round three):**

- `life::contract` frozen and the Phase 8 gate green: moving bodies
  with budgets, sense transductions (`flux_band`, pressure history,
  species concentrations), genome/lineage ledgers, era run bending the
  O₂ curve. The acceptance world file must carry a savanna-analog
  biome, lightning (Phase 7 W5), and at least two metal-analog ore
  outcrops (Phase 7 W3 geology) — world-file facts, not engine changes.
- Seam round three: **S13** landed upstream — an articulated multi-body
  layer reading `mat::record` properties (running, carrying, knapping
  need skeleton-scale mechanics; grid elasticity can't afford or resolve
  them). **S14** (the "own clock" wording slip) closed: agents tick on
  the global tick — Phase 0's one-timeline principle stands.
- Phase 6 contact/fracture events + Phase 5 toughness records green —
  every tool is a fracture-mechanics argument, won or lost honestly.
- Phase 8's era-compression machinery (D8 validity limits) — epochs
  span ~10⁴ yr ≈ 10⁵ generations; individual instantiation cannot
  carry that and won't be asked to.

**Definition of done:** on the first-people world file, dry-season
lightning ignites the grass strip; a lineage that has learned to
*tend* fire shows up in the budget ledger within generations —
heat-processed food-analog yields more net joules per foraging-joule,
and the brain-tissue fraction of that lineage's budget **rises across
generations** (the cooking–brain loop is a slope in the ledger, banded
by shape, never a constant). At a chert-analog outcrop, knapped cores
produce edge geometries whose butchering contact tests beat unworked
stone by a real margin, and the skill that makes good edges — not any
edge — spreads through the population at the speed of voice-analog:
skill histograms diffuse within earshot radius and **variants improve
across carriers once transmission fidelity crosses the cumulative
threshold** (below it, skills decay to founder noise; both directions
are tests, not knobs). Agents experimenting near hot rock over
ore-bearing ground find smelt-analog; where the ore lies, bronze-analog
tools shift clearing and digging budgets and settlements follow the
budgets, not a map. Foraging pressure alone — agent choice events, no
scenario — drifts two plant-analog lineages into the domestication
syndrome (retain, big-seed, quick-seed trait complex) with selection
coefficients the Phase 8 correlation ledger can name the agent events
behind, and the same pressure on a tolerated animal-analog lineage
drifts tameness. Villages appear as persistent material structures with
waste ledgers Phase 8 decomposition closes. Professions are attractors:
the role histogram (forager/fighter/potter-analog/…) is stable under
population perturbation and its exchange-network flows match the
histogram; a baker-analog who cannot feed themselves does not persist.
Every tool user traces in the lineage ledger to a Phase 8 forager
lineage — **no ontological discontinuity** — and the run ends in an
agricultural plateau with no furnace-scale industry, no test skipped,
and no engine rule that would stop one if the agents found it.

---

## Scale contract (the social LOD ladder)

- **Individual (in bubble):** agent = body (Phase 8 `corpo/` + S13
  rigid layer) + weights (individual state, deterministic instantiation
  from RNG lane `sub=5`) + skill memory; ticks on the global tick.
- **Population (default, jumpable):** skill/role histograms +
  lineage-culture correlation ledger (Phase 8 pattern re-used);
  demography compressed over generations with honesty tax against
  instantiated runs.
- **Epoch:** ~10⁴ yr acceptance span; compressed selection + culture
  diffusion in stable windows, ticked through shocks (climate events,
  crop failures) — D8 discipline extended to culture (decision D9).
- Bubble scale: ≤10³ agents ticking at once; one village ≈ 10²
  individuals is the resolved unit of the epoch tests.

## Architecture

```
sim/
  mind/
    agent/     individual instantiation (Phase 8 LOD pattern, lane
               sub=5), drives = budget deficits (hunger, thermal,
               safety-from-dose) resolved by a learned policy; behavior
               = Phase 6 momentum/contact events + Phase 5 material
               interactions + Phase 7 flux events, nothing else
    learn/     value learning from budget outcomes: predict budget
               deltas, act to raise them, planning horizon = how far
               predictions stay calibrated (emergent, never preset);
               small generative nets - cognition is expensive tissue
    cultu/     skill memory as individual state; transmission ONLY via
               sense channels (pressure-wave strings, gesture/visual
               patterns, surface marks for persistence); culture ledger
               tracks variant frequency vs fidelity threshold - the
               cumulative-culture phase boundary is computed here
    rig/       consumer of S13: articulated bodies with joint torques
               whose strengths come from mat records (tendon-analog
               properties); strikes, throws, carries are fracture/
               contact tests against real toughness
    fire/      NOT a fire system: the detection + bookkeeping layer for
               combustion channels (Phase 4 oxidation kinetics) in fuel
               geometries (Phase 5) with buoyancy flow (Phase 6) -
               cooking = temperature-time chemistry on food species,
               the brain-budget feedback is read, not written
    demog/     generation-compressed demography + culture diffusion;
               honesty tax vs instantiated village runs
    socia/     minimal: recognition, coalition pressure, mate-choice
               as budget games - Phase 11's sociology plugs into these
               ledgers, nothing more lives here yet
```

Data rules:

- **One clock.** Agents tick on the global tick (S14); "decision rate"
  is policy resolution, not a second timeline.
- **No scripted discoveries.** No fire recipe, no smelting trigger, no
  agriculture key in `sim/` — grep gate extended: zero occurrences of
  the strings `fire`, `bronze`, `farm`, `village` as state machines in
  engine code (`fire/` is a detector/ledger name only, and its tests
  assert ignition from lightning + fuel + heat, never from a call).
- **Culture is physical.** A skill exists only as (a) weights, (b) a
  transducible signal, or (c) a material trace. Skills that never
  crossed a sense channel never spread — fuzz test for telepathy.
- **Budgets still close.** Agents inherit Phase 8's ledger discipline:
  brain-analog tissue is a budget line whose waste heat Phase 6 must
  carry; an agent that "thinks" its way to negative net energy is
  selected out by the same books as a starving cell.

## Work packages

W1–W3 are the enabling cognition stack (sequential); W4–W6 are the
epoch acts, parallel once W3's culture ledger exists; W7 last.

### W1 — Agency: bodies that choose

- [ ] S13 lands upstream (`rigid/` in Phase 6 reading `mat::record`);
      joint torques, strikes, carries as logged contact events.
- [ ] Agent instantiation + drives + policy skeleton; birth from Phase 8
      lineage ledger, death at budget floor, deterministic replay.
- [ ] **Tests:** a foraging agent closes its budget on a real gradient
      and dies on a depleted one — no respawn, no pity energy;
      corrupted-value fixture wastes budget and self-extinguishes
      against the CI budget checker; instantiation determinism: same
      seed, same life, cache-off.

### W2 — Learning & planning that pays for itself

- [ ] Value learning from budget outcomes; planning-horizon emergence:
      keep extending cached trajectory prediction while calibration
      holds, collapse it when the world outruns it.
- [ ] **Tests:** novel barrier between agent and resource solved
      untaught (barrier is CI-generated, never in training world);
      horizon lengthens in predictable environments and shrinks in
      noisy ones, both without new constants; expensive-tissue check:
      brain budget share tracks task difficulty across lineages.

### W3 — Voice-analog & the cumulative threshold

- [ ] Transmission via pressure-wave/visual channels only (Phase 6
      waves + Phase 8 transductions); teaching = one agent's policy
      bias imprinted through a sense channel onto another's learning.
- [ ] Culture ledger: variant frequency, fidelity, founder-drift;
      surface-mark persistence (Phase 5 traces) as long memory.
- [ ] **Tests:** a learned variant diffuses at the speed of its channel
      (radius/time in band), teleports zero distance; below fidelity
      threshold skills decay, above them **variants improve across
      carriers** — the threshold is found by the test, not set by it;
      isolated groups diverge (drift), connected ones converge.

### W4 — Fire & the brain loop

- [ ] Ignition: lightning strike (Phase 7 W5) into fuel geometry at
      pyrolysis-analog thresholds — closure detector style: fire exists
      when a fuel cell runs sustained oxidation flow; agents *tend*
      (add fuel = momentum event) never *cast*.
- [ ] Cooking: temperature-time chemistry channels on food species;
      net-yield and brain-budget-share readouts.
- [ ] Fire–ecosystem coupling: burn regimes against Phase 7 climate +
      Phase 8 litter/decomposition; biomass-burning ledger edge closes.
- [ ] **Tests:** no sustained fire without lightning + fuel + wind
      (controls fail); tending lineage's food-net-energy slope rises in
      band; brain-fraction slope follows with a generational lag —
      the cooking–brain feedback as two ledger slopes, the phase's
      signature chart; a burn the world recovers from (Phase 8
      succession) proves no permanent scarring by construction.

### W5 — Stone, edge, metal: the tool chain

- [ ] Knapping: fracture-path geometry from Phase 6 fracture + Phase 5
      toughness; edge sharpness a computed geometric property scored by
      contact-work efficiency in butchering-analog tests.
- [ ] Hafts and composites (Phase 5 assemblies); wear ledgers on tools.
- [ ] Smelt-analog: agent experimentation (W2) over ore outcrops;
      reduction chemistry is Phase 4 channels at fire temperatures —
      discovery rate depends on ore geography, and the acceptance world
      deliberately puts one outcrop near the savanna strip and one far.
- [ ] **Tests:** knapped edge beats unworked stone by a measured
      contact-work margin; edge quality correlates with knapper skill
      histogram (skill is a real physical variable); bronze-analog
      adoption spreads along budget-gradient paths, reaching the
      far-outcrop region later or never — geography decides, tests
      assert the ordering exists, not that it completes.

### W6 — Farms, villages, professions

- [ ] Domestication by choice pressure: foraging/harvest preferences
      ARE selection events into the Phase 8 correlation ledger; crop-
      and tameness-analog syndromes drift; no "domesticate" action.
- [ ] Settlements: persistent material structures (Phase 5), waste
      fluxes closed by Phase 8 decomposition, carrying-capacity
      feedback to demography.
- [ ] Roles: policy specialization as budget-game attractors; exchange
      as direct flux transfer between agents (money is Phase 12's
      compression of exactly this).
- [ ] **Tests:** domestication syndrome traits rise with named agent
      choice events as selection coefficients; tameness drifts under
      tolerance pressure alone; role histogram stable under ±20 %
      population perturbation with exchange flows matching it; a
      village whose waste ledger doesn't close fails CI (Phase 8's
      supertest, now with latrines).

### W7 — Epoch harness + interface freeze

- [ ] First-people acceptance run: lightning → cooking loop → knapping
      band → bronze-analog at the near outcrop → farming + roles;
      ends on the agricultural plateau, asserts **openness** (no rule
      blocks industry: an industry-seed fixture injected at end-state
      is not rejected by any engine rule, only priced by budgets).
- [ ] Demography honesty tax: 10⁴-yr compressed epoch vs instantiated
      10²-yr village runs in band; culture diffusion transparency
      across compression boundaries.
- [ ] Freeze `mind::agent` + culture-ledger contract (below); D9
      (epoch-compression validity) into `spec/decisions.md`.

## Performance budget (fill from W1–W3)

| Path                                        | Budget           | Measured |
|---------------------------------------------|------------------|----------|
| policy eval per agent·tick (10³ agents)     | < 0.5 ms         | ___      |
| rigid-body agent step (S13 layer)           | < 1 ms           | ___      |
| culture-ledger update per transmission      | < 10 µs          | ___      |
| demography compression step (1 generation)  | < 5 ms / 10² agents | ___   |
| fire cell sustained-oxidation check         | < 20 µs          | ___      |
| first-people acceptance run (offline)       | < 90 min wall    | ___      |
| honesty tax (epoch vs instantiated)         | < 30 min wall    | ___      |
| CI-fast culture-diffusion lane              | < 10 min wall    | ___      |

## Interface exposed to Phase 10 (technology tree)

> Phase 10 may read: agent policies/skill memories and the culture
> ledger (who knows what variant), `mind::agent` budget readouts, and
> everything Phases 4–9 already expose (agents *are* world-processes).
> Phase 10 may write: **experiment events** — an agent's policy
> choosing to vary a parameter of the world it manipulates (the
> research move is just learning W2 applied with exploration bias) —
> and knowledge artifacts as culture-ledger variants plus surface-mark
> records. Research is not a new layer: it is W2 learning pointed at
> the world-model agents already carry, and Phase 10's job is making
> knowledge *social* (Phase 10 W2) and *cumulative-laboratory-scale*.

## Verification strategy

1. Oracle: `tests/oracle/mind/` — fidelity threshold band for
   cumulative culture, diffusion speed of a channel, butchering
   contact-work margin, domestication-syndrome trait rise rates.
   Directions tight, values loose.
2. No-buttons gate: grep for state-machine strings (`fire`, `bronze`,
   `farm`, `village`, `teach`) in `sim/` engine paths; plus the
   positive control that lightning-only ignition runs exist — the gate
   must not accidentally accept a scripted discovery while rejecting a
   real one.
3. Ancestry continuity: every agent in the acceptance run links,
   through Phase 8 lineage ledgers, to a pre-agent forager lineage;
   the test walks the chain and fails on any unlogged birth.
4. Honesty taxes ×2: demography vs instantiated villages (nightly);
   culture compression transparency at shock windows (climate events
   tick, plateau windows compress).
5. Surprises ledger: does the acceptance world ever independently
   discover agriculture twice; role-histogram shapes; any epoch that
   *doesn't* happen in-run (a skipped epoch is a finding about
   geography, logged as dated surprise, not a test failure to patch
   around by moving the ore).

## Sequencing

```
Wk 1-2        Wk 2-4           Wk 4-6            Wk 5-8            Wk 8-10
─────         ──────           ──────            ──────            ──────────
W1 agency     W2 learning      W3 voice+culture  W4 fire/brain ─┐  W7 epoch
(needs S13     (horizon,        (threshold found  W5 tools/geo  ├─ harness
upstream)     tissue budget)    by test)         W6 farms/roles ┘  +freeze
```

## Risks

| Risk | Mitigation |
|---|---|
| Epoch never ignites in feasible time (discovery is rare-event statistics) | acceptance world concentrates lightning + fuel + ore in the foraging range (geography, allowed); if discovery still misses, log surprise and widen the *world*, never the engine — a scripted first-discovery requires a decision entry admitting the button (Phase 8's rule inherited) |
| Cumulative culture never crosses fidelity threshold (Tantalus: variants always decay) | threshold is a computed band with both directions tested; if the acceptance world sits below it, the channel (not the culture layer) is the suspect — voice SNR vs distance is Phase 6 physics, fix there |
| Agents too expensive to run civilizations | histogram LOD outside bubble is the default, individuals are the exception; brain nets stay small by construction (expensive tissue is enforced by ledger, not by comment) |
| Tests silently measure anthropomorphism ("looked smart") | every mind test reads a ledger: budget slope, diffusion radius, contact work, trait frequency; nothing asserts behavior adjectives |
| Domestication drift lost in Phase 8 noise floor | agent choice events are explicit selection coefficients in the correlation ledger — signal injected by physics, measured at W1 sensitivity (Phase 8 machinery already resolves it) |
| Epoch compression invalid across shocks (famine, migration) | shocks tick, plateaus compress (D8 pattern → D9); transparency test at the hottest shock window |
| Phase 9 creep into Phase 10 (research/science emerges by accident of optimism) | hard line: agents may discover things, but *knowledge as social practice* — institutions, publication, labs — is Phase 10; culture-ledger freeze line says Phase 10 may not add agent internals |

**Gate:** Phase 10 starts when: the first-people acceptance run is
green offline-nightly (cooking slope, knapping margin, cumulative
threshold crossed, bronze-analog at near outcrop, farming + role
histogram stable), ancestry continuity and both honesty taxes pass,
S13's upstream tests are merged, D9 is in `spec/decisions.md`, and
`mind::agent` + the culture-ledger line are frozen in
`spec/interfaces.md`.
