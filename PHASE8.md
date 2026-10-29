# Phase 8 — Life: Abiogenesis → Ecosystems

**Goal:** chemistry that persists. From Phase 4's reaction networks under
Phase 7's environmental gradients, template molecules arise that copy
themselves with errors, cells enclose them, and ecology — food webs,
nutrient cycles, arms races — closes the planet's reservoir ledgers with
biological edges the ledger never had. There is no "create life" button
anywhere in the tree: **living is a computed property** of a species
graph (a set whose members catalyze their own production), and every
organism above it is bookkeeping over chemistry, mechanics and energy
budgets that Phases 4–7 already own. Phase 8 writes flux events and
nothing else; if the life layer ever needs to edit a planet or material
record directly, that is a seam, not a feature.

**Prerequisites (hard gate, from Phase 7 + seam round two):**

- `planet::env(cell)` + the reservoir/flux-ledger contract frozen; the
  Phase 7 primordial-system acceptance green (offline) — life needs the
  4-Gyr stage standing before it walks on.
- Seam round two **S10–S12** (`spec/seams.md`) landed upstream with
  red-first tests: templated polymerization/catalysis channel class in
  Phase 4 W3 (S10), amphiphile self-assembly kinetics — vesicles form
  by nucleation+growth like every other phase transition (S11), and the
  photoexcitation channel class (S12; also retrofits Phase 7 W5's
  photolysis term, which silently needed it).
- Phase 2's frozen `radiation/ionization fields per cell` read path —
  that field × bond energies is the mutation source; no mutation-rate
  constant exists anywhere in `sim/`.
- Phase 5 `mat::record` + Phase 6 contact/momentum events green — bodies
  are materials and motion before they are organisms.

**Definition of done:** in a tidal-strip of the Phase 7 acceptance
planet — wet-dry cycling rock over a hot-rock gradient — the closure
detector fires: a set of species appears whose members catalyze their
own production, and it *keeps* firing as its members' sequence-analog
templates vary under the env dose and the best-copying variant wins the
local energy budget. Amphiphiles self-assemble into vesicles that
enclose such sets; enclosed chemistry runs measurably longer than free
solution in the same cell, so **cells are an outcome, not an axiom**.
Populations ride real gradients: logistic growth on a redox source that
starves when the source stops, extinction when the env dose rate times
genome length crosses what replication fidelity can outrun. A parasite
template class appears that copies using a host's own channels — the
virus of the roadmap, same ontology, no new machinery — and the
host×parasite match ledger shows a Red Queen chase (both sides' match
statistics drift, neither wins). A mould-analog metabolite inhibits one
competitor lineage and not another (selectivity falls out of binding
chemistry), and the inhibited lineage evolves resistance on the same
run — all four roadmap arms-race beats in one test file. Food webs form
from who-eats-whose-product plus Phase 6 contact predation, biomass
falls with trophic depth in band, and decomposition closes the Phase 7
reservoir graph: **every abiotic flux edge of Phase 7 gains a biological
counterpart in the ledger, and the books still balance.** Then the era
test: the same world runs 500 Myr compressed; photoautotrophs harvest
the UV-B band and bend the atmospheric O₂-analog curve upward (Phase 7's
anoxic baseline is the thing life breaks, visibly); a drying climate
event pushes symbiotic consortia onto land where desiccation tolerance
(cuticle-analog wax, Phase 4 organic chemistry) decides the winners;
body plans move by Phase 6 momentum events with energy budgets that
close per individual while observed and per population while not. No
speciation script exists: "epoch" is what the climate curve does to the
fitness ledger. Humans are Phase 9's problem.

---

## Scale contract (the biological LOD ladder)

- **Genome:** template species over a Phase 4 monomer alphabet; sequence
  space is sampled, never enumerated — the registry stays emergent.
- **Population state (default, jumpable):** genotype-frequency ledger +
  a host×parasite **correlation ledger** (match matrix, compressed) —
  frequency-only dynamics miss variance-driven escape, so correlations
  are first-class, not an afterthought.
- **Individual state (on observation, Phase 0 D4 discipline):** sampled
  deterministically from RNG lane `sub=4`; a sampled individual must
  reproduce population statistics within binomial band (nightly honesty
  test), and inside the bubble it ticks as a cell of Phase 4 chemistry +
  Phase 6 mechanics, no special biology.
- **Time:** abiogenesis acceptance runs in an *accelerated-but-real*
  prebiotic strip (concentration physics, not time compression); the
  500-Myr era run is compressed selection over stable-climate windows
  with jump transparency, like the mantle.

## Architecture

```
sim/
  life/
    heredy/     template species: Phase 4 species whose channel set
                includes S10 templated polymerization; copying fidelity
                is computed (bond energies vs env ionization dose), so
                mutation rate is an output, never an input; lineage and
                hostxparasite correlation ledgers
    abiox/      the closure detector: finds species-sets closed under
                catalysis that consume env fluxes - a graph property of
                Phase 4 channels, memoized. Detects and measures only:
                the file that helps abiogenesis originat
                is the file this one must never be
    cellu/      vesicle compartments (S11), enclosed metabolism,
                osmotic/thermal stress from Phase 4/5 thermo;
                population<->individual LOD (sub=4 lane)
    metabo/     energy budgets: redox donor/acceptor pairs harvested
                from env:: chemistry, uptake = f(concentration,
                surface, gradient); growth/motion/heat/waste ledger
                closes per tick or the run dies
    eco/        niches = actual energy-source gradients from env::,
                never a niche table; food-web graph = chemical edges
                (whose product is whose food) + mechanical edges
                (Phase 6 contact fracture = eating); decomposition
                returns flux to the Phase 7 reservoir graph
    viro/       parasitic templates: same ontology as heredy/, channels
                consume host machinery; arms race lives entirely in the
                correlation ledger - this file is ~all tests
    corpo/      multicellularity: S10 regulatory extension (templates
                catalyzing template-expression) yields soma/germ
                division as a stable attractor under within-lineage
                relatedness; bodies = growing Phase 5 materials with
                emerged boundaries (cuticle, shell via mat nucleation),
                motion = Phase 6 momentum + deformation events,
                senses = transduction only: flux_band (vision's
                physical half), pressure-history tap (hearing), species
                concentrations (smell). Rendering is Phase 14's job
```

Data rules:

- **No life flag, no organism type.** `living?` is the closure detector
 's cached bit over channel graphs; anything else that smells like an
  ontology (species tree, named clade, "individual" below observation)
  fails the grep gate: `sim/life/` contains zero literal genome strings,
  zero named taxa, zero mutation-rate constants.
- **Budgets close or runs die.** Every individual while observed, every
  population always, carries an energy ledger closed against env::
  sources + Phase 6 work + heat + waste flux. A population that grows
  with an unclosed budget is a hard fail, not a surprise entry.
- Phase 8's only write path stays Phase 7's freeze line: flux events
  into reservoirs and species (uptake, excretion, necromass). Lichens
  etching rock is a proton-analog flux event, not a rock edit.
- Era compression is jump-state discipline: selection flows linearized
  inside stable-climate windows, closed-form where valid, ticked where
  not, final hash equals ticked reference on sampled windows.

## Work packages

W1 needs only Phase 4/2 (seam-fixed) and runs parallel to Phase 7's
second half — it is the phase most worth starting early, because W1's
uncertainty dominates the phase. W2 needs W1 + S11; W3 needs W2 +
`planet::env`; W4–W6 need W3; W7 last.

### W1 — Templating, heredity, the closure detector

- [ ] S10 lands upstream: templated polymerization channel class +
      red-first test (a template accelerates production of its own
      complement from monomer flux; nothing else does).
- [ ] Closure detector: incremental graph-closure over catalysis edges,
      memoized, fired-once semantics logged.
- [ ] Mutation = ionization field × genome length × computed fidelity
      (fidelity itself evolvable in W6+ runs); RNG lane `sub=4`.
- [ ] **Tests:** prebiotic strip (wet-dry + gradient) reaches closure in
      bounded wall-time, ladder of fallbacks recorded like Phase 3's;
      a non-catalytic control set never fires the detector; copying
      variants compete and the ledger names the winner by energy budget,
      not by draw order.

### W2 — Cells: vesicles, compartments, populations

- [ ] S11 lands upstream: amphiphile aggregate nucleation+growth;
      vesicle yield in band for concentration ramp shapes.
- [ ] Enclosed sets: metabolism inside vesicle vs free solution in the
      same cell — persistence is the metric, osmotic rupture real.
- [ ] Population LOD: frequency ledger + correlation ledger, individuals
      materialized on ask from `sub=4`, deterministic.
- [ ] **Tests:** enclosed chemistry outlives free chemistry on leaked
      substrate (direction test); logistic growth then starvation decay
      on a switched redox source; sampled individuals match population
      stats in binomial band across a nightly sweep; dose-rate ×
      genome-length crosses extinction threshold in band shape.

### W3 — Metabolism & energy budgets

- [ ] Redox harvest from env:: species pairs; uptake with surface/
      diffusion limits (no infinite feeding); fermentation/analog
      excretion closes budgets under anoxia vs oxic.
- [ ] **Tests:** growth yield tracks substrate energy in band; anoxia
      switches excretion chemistry and the ledger follows; a cell in
      thermodynamic impossibility (budget claims more than env offers)
      is caught by the CI budget checker, not silently fed — the checker
      goes red on a deliberately-impossible fixture.

### W4 — Ecology: niches, food webs, decomposition

- [ ] Niche graph rebuilt lazily from env:: gradients only; chemical +
      contact-predation edges; trophic depth computed, not assigned.
- [ ] Decomposition: necromass → Phase 5 detrital material → mineral
      flux back into the Phase 7 reservoir graph; soil-analog horizon
      emerges through Phase 5 W4 weathering under litter flux.
- [ ] Mutualism edges: cross-lineage flux exchange where **both sides
      gain budget** — pollination/dispersal-analog and mycorrhizal-
      analog exchange emerge as stable two-node cycles in the web graph
      (fungi-analog = decomposer lineage partnering with a
      producer-analog over mineral access; no symbiosis code, just
      edges that pay).
- [ ] **Tests (mutualism):** a forager lineage harvesting a
      producer-analog's reward flux co-distributes with it along the
      climate gradient; removing one partner cascades range loss
      without scripted extinction; a "cheating" edge that takes flux
      and returns none is rejected by the budget ledger — mutualisms
      that don't pay both books don't persist.
- [ ] **Tests:** web connectance and chain length land in loose band
      (shape); biomass declines with trophic depth; the Phase 7 abiotic
      ledger test still passes with the biology layer ON and books
      balance with biological edges included (the phase's money shot);
      an invasive species introduced across a barrier spikes then
      settles or crashes — no scripted equilibrium either way.

### W5 — Viruses & arms races

- [ ] Parasitic templates via host-channel-hijacking channels (S10
      class, parasitic instances); match-statistics ledger.
- [ ] Mould-analog inhibitor: selectivity emerges from binding-chemistry
      differences between lineages; resistance = mutation + selection,
      the W1 machinery re-used.
- [ ] **Tests:** host and parasite match stats both drift (Red Queen,
      direction over value); inhibitor halts lineage A and not lineage
      B, and A evolves resistance in-run — all four roadmap beats, one
      test file, zero named organisms; an immune-analog: a cellular
      repair/ejection set that raises survival against parasites whose
      matches it has *encountered* (memory from chemistry, not design).

### W6 — Multicellularity, body plans, land, light

- [ ] Regulatory closure (S10 extension): templates expressing
      templates; soma/germ split emerges under relatedness pressure;
      cheating lines that break cooperation are a tracked failure mode.
- [ ] Photoautotrophs: S12 photoexcitation channels harvest flux_band
      (UV-B-analog band first, in band) and bend the O₂-analog curve —
      the anoxic Phase 7 baseline visibly ends.
- [ ] Land: desiccation tolerance (cuticle-analog) decides which
      consortia survive a climate drying event; vegetation layers as
      Phase 5 porous materials competing for `flux_band` at the top.
- [ ] Body plans: constrained generative search (bounded body graphs —
      segmentation from the same math as fracture patterns), energy
      budget gates size and speed; locomotion through Phase 6 momentum.
- [ ] Senses' physical half: photoreceptor chemistry on `flux_band`,
      pressure-history tap, chemoreception — transduce only.
- [ ] **Tests:** O₂-analog curve bends after photoautotroph emergence
      (shape vs Phase 7 baseline run); drying event: cuticle carriers
      advance, bare ones retreat, ledger shows who ate what; a body plan
      that violates its energy budget is rejected by the generator —
      speed/mass curve in band; **no test asserts a named era outcome**
      (dinosaurs are allowed to be a surprise, logged either way).

### W7 — Era harness + interface freeze

- [ ] 500-Myr compressed era run on the Phase 7 acceptance world:
      marine → chemical land-granting → vegetation layers, driven only
      by the climate curve; jump transparency on sampled windows.
- [ ] Budget CI: energy-ledger closure per population per tick, whole
      era run; cache-off replay regenerates registry + detector memos.
- [ ] Freeze `life::contract` (below); write the era-compression
      validity limits into `spec/decisions.md` (D8 candidate).

## Performance budget (fill from W1–W4)

| Path                                        | Budget          | Measured |
|---------------------------------------------|-----------------|----------|
| closure detector, incremental per new edge  | < 1 ms, memoized| ___      |
| population step per cell (compressed)       | < 5 µs          | ___      |
| correlation-ledger update (host×parasite)   | < 2 µs per pair | ___      |
| individual tick while observed              | < 1 ms          | ___      |
| food-web rebuild per cell (lazy)            | < 1 ms / 10⁴ ticks | ___   |
| prebiotic-strip CI acceptance               | < 10 min wall   | ---      |
| 500-Myr era run (offline nightly)           | < 60 min wall   | ___      |
| honesty sweep (population vs individuals)   | < 20 min wall   | ___      |

## Interface exposed to Phase 9 (intelligence)

> Phase 9 may read: bodies as `mat::record` + energy budget + sense
> transductions (`flux_band`, pressure history, species concentrations),
> the genome/lineage ledger for heredity of learned-and-inherited
> lineages, and `planet::env`. Phase 9 may write: behavior as events at
> individual scale only — momentum and contact (Phase 6), material
> interaction (Phase 5 events), fluxes (Phase 7 ledgers). A choice is
> computed by Phase 9 from sense data and is never stored below it; the
> life layer stays agent-free until Phase 9's agents exist — and they
> tick on the same global clock (Phase 0's one-timeline, seam S14).

Phase 9's intelligence question is then environmental again: do sense
transductions plus energy budgets make predicting the environment worth
more joules than they cost? If not on the acceptance world, that is a
Phase 7/8 environment gap, not a Phase 9 hack.

## Verification strategy

1. Oracle: `tests/oracle/life/` — logistic-growth curve, binomial
   sampling band, trophic-pyramid exponent, Red Queen drift-direction
   test, O₂-bend shape. Values loose, directions/shapes tight.
2. The ledger supertest: Phase 7's abiotic ledger acceptance re-run with
   biology ON; balance holds with biological edges in the graph. This
   single test kills every "life runs on hidden energy" bug class.
3. Honesty tax: nightly population-vs-individual comparison across
   random strips; a compressed population that individuals would not
   reproduce is a hard fail (same spirit as jump transparency).
4. Grep gate extended: no genome strings, taxa names, mutation-rate
   constants, niche tables, or "fitness" scalars in `sim/life/` —
   fitness is what the budget ledger says it was.
5. Surprises ledger: abiogenesis wall-time to closure, whether complex
   multicellularity ever fires, era ordering, any mass-extinction event
   the climate curve causes — dated lines, measured gaps, no retro-fix
   of the world to make the story tidier.

## Sequencing

```
Wk 1-3            Wk 3-5              Wk 5-7              Wk 7-9       Wk 9-11
─────             ─────               ─────────           ─────────    ──────────
W1 templating +   W2 cells + LOD      W3 metabolism ─┐    W5 viruses   W7 era run
closure detector  (needs S11 green)   W4 ecology      ├─── W6 bodies +  +freeze
(needs S10,S12     runs parallel to    (needs env::)  │    land + light gate Phase 9
upstream)         Phase 7 finish ─────┘──────────────┘
```

## Risks

| Risk | Mitigation |
|---|---|
| Abiogenesis never fires in feasible wall-time | the prebiotic strip uses real concentration physics (wet-dry, thermo-focus) and gets the phase's whole slack budget; fallback ladder (Phase 3 style) records every rung; a scripted seed replicator is the **last** resort and requires a decision entry admitting the button exists |
| Compressed populations miss the variance that drives escape | correlation ledger is first-class from W2; honesty tax nightly; worst case the era run ticks individuals in hot windows only (documented, band-tested) |
| Food-web combinatorics explode (chemical niche space) | niches only from env:: gradients that actually exist in the strip; lazy rebuild; fuzz cell = eutrophic hot-spot |
| Arms race runs to boring fixed points (no chase) | match matrix keeps rare-type variance; if chase never emerges, log it as a surprise and revisit the S10 class granularity upstream, don't tune chase in |
| Era compression invalid across climate shocks | closed-form only in stable windows, shocks tick; transparency test across the hottest window in CI |
| Life makes Phase 7's climate story untidy (O₂ bend reads as scripted) | the bend test is run against the biology-OFF baseline as control in the same CI job; both curves ship |
| Scope: "humans" appears in Phase 8 | hard line — Phase 8 ends at moving bodies with budgets and senses; cognition, culture, tools are Phases 9–11, and the roadmap's epoch list is satisfied up to "vegetation layers + fauna" |

**Gate:** Phase 9 starts when: prebiotic-strip closure + heredity is
green in the CI-fast lane; the ledger supertest passes with biology ON;
the arms-race file is green (four beats); the 500-Myr era run bends the
O₂ curve and lands life on land under climate events alone with budgets
closed; the honesty tax passes; S10–S12 upstream tests are merged; D8
(era-compression validity) is in `spec/decisions.md`; and
`life::contract` is frozen in `spec/interfaces.md`.
