# Phase 10 — Technology Tree (emergent, research-driven)

**Goal:** the world learns to read itself and starts rewiring its own
subsystems. Research is Phase 9's learning pointed at the world with
exploration bias; instruments are transducers calibrated against real
fields; science is the replication ledger that emerges when claims get
material traces and enemies. The "technology tree" **does not exist in
the engine**: there is no device ontology, no recipe, no unlock —
machines are agent artifacts (Phase 5 records + S13 rigid bodies +
Phase 6 field interactions), and "technology" is a test-side name for
stable device-class clusters in the artifact ledger. Phase 6's standing
rule applies in full: machines are built out of W1–W5 interactions
only, and the engine stays a test. The acceptance arc runs from an
agent boiling water to a machine running a nested world to a telescope
reading the engine's own CMB — **the world recovering its own genesis
parameters, in band, in a paper filed in its own claims ledger.**

**Prerequisites (hard gate, from Phase 9 + seam round four):**

- Phase 9 gate green: `mind::agent` + culture-ledger frozen; the
  first-people plateau world is the substrate — the acceptance run
  *starts* at the agricultural plateau, it does not rewind.
- Seam round four upstream with red-first tests: **S15** — Phase 6 EM
  is magnetostatics-only; capacitors, inductors, transmission and radio
  propagation need the EM operator extended to the regimes they name
  (or the regimes explicitly declared, owned upstream — no lumped-element
  fudge inside this phase). **S16** — a nested-simulation determinism
  contract (child seeds drawn from parent RNG lanes, replay-hash rules,
  recursion depth) written into `spec/` as decision **D10**.
- Phase 5's doping-trend test green *direction-only* (its own risk row
  pre-names this phase — transistors get direction, not values; if a
  whole carrier class behaves wrongly, the fix is Phase 4-level and
  documented).
- S13 rigid layer merged (machines share it with animals); Phase 7's
  lazy-star contract + the S5 expansion-band decision (W4's sky test
  reads exactly those numbers).

**Definition of done:** on the plateau world with coal-analog seams
near the early-industrial settlement, an agent experimenting over a
boiling vessel finds work: a pressure vessel that survives its own
operating pressure (Phase 5 fracture sets the honest boiler-death rate
the run must show, not zero), then an engine that raises mine-drain-
analog water, its efficiency landing **between zero and its Carnot
ceiling with every joule in the Phase 6 entropy ledger** — exhaust heat
booked, no leakage. The grid then does what grids do: dynamo-analog
generation balanced against load as a flux ledger, city lights appearing
as a night-side anomaly in `flux_band`, clocks from Phase 6 oscillators
keeping time agents route traffic against — commute patterns as
budget-minimizing attractors, the same math as Phase 9's professions.
A spark gap and a wire loop put voice-analog over the hill and radar-
analog echoes off it; a longer horn hears the sky: the surface receiver
measures the CMB-analog at the S5-band anchor, and a **claims-ledger
paper recovers the engine's own expansion-law parameters within band**
— the full circle, genesis read back by genesis. Doped crystals
(Phase 5's direction, honestly coarse) switch; switching computes; the
first useful programs are bookkeeping, then games; and one machine runs
a **nested coarse world** — deterministic child, parent-lane draws,
replay bit-identical, depth-guarded — while a machine-tuned player
beats every biological agent at a timing game (brute force is a
ledger-visible win-rate, not a narrative). The transport chain is five
work-budget milestones, not five blueprints: hull displacement, wheels
on rails, wings whose lift/drag the continuum actually computed, a hull
that doesn't buckle at depth, and rotor drones — each adopted along
budget gradients, each spread pattern a Phase 9 replay. Under the
microscope, germ-analog populations explain village disease curves
(medicine becomes dose-response chemistry on Phase 8 populations, and
the demography ledger visibly bends); the biotech ladder walks Phase 8
machinery as tools: breeding → trait optimization → mould-derived
inhibitor-analog drugs → template-splicing edit-analog, and one edited
nitrogen-fixing-analog symbiont lineage measurably **moves the Phase 7
nutrient ledger** — engineered chemistry feeding back into the planet
the engine built. Rockets climb out of the acceptance world's gravity
on computed momentum, satellites observe lazy stars through the Phase 7
contract, and the packet network that ties it together makes memes
measurable: variant diffusion rates on-network versus off, platforms as
coalition statistics (Phase 11's door, unlocked but unopened). And the
tree still isn't there: if the run skips aviation, the surprises ledger
logs why, and no test fails.

---

## Scale contract

- **Devices are artifacts, not entities:** every machine is a `mat`
  record + rigid-body structure + field couplings, built by agent
  events; "device class" is a named cluster in the *test-side* artifact
  classifier — the engine never has a `Device` type.
- Grid/network scale: acceptance region ≈ 10⁴ device nodes ticking on
  the strip clock; energy/time ledgers, not per-device physics
  extravagance.
- **Nested world budget:** child sim is coarse (Phase 15 LODs, child
  seed from parent lane), parent-tick cost ratio ≤ 10⁻², recursion
  depth 1 (a nested-nested world needs its own decision entry).
- Epoch: industrialization acceptance spans ~100 yr ticked in-region,
  rest compressed under D9.

## Architecture

No new sim/ package for technology. Three thin bookkeeping layers, each
strictly a ledger over lower-layer events:

```
sim/
  sci/        claims ledger: a claim = culture-ledger variant with an
              evidence pointer (replay-log region ids); replication =
              independent agents reproducing the logged intervention;
              status transitions (contested/replicated/withdrawn) are
              computed from agent experiments, never authored;
              priority, citation-graph, school formation = statistics
              of this one ledger - "science as social practice" is
              literally this ledger's shape over time
    metro/    instruments as calibration maps: any device whose output
              channel is a Phase field read (deflection, band flux,
              pressure history, species concentrations at a port);
              calibration = deviation-from-truth distribution computed
              against ground truth, feeding W2 learning's world-model
              radius - instruments are how a policy sees further than
              its skin
    net/      communication as physical devices on Phase 6 fields:
              pulse/radio links, packet routes, latency from
              propagation - meme statistics = culture-ledger variant
              diffusion measured with the net ON/OFF (the difference
              is the phase's thesis, quantified)
    nest/     consumer of S16: child engine instances with parent-lane
              seed draws, own log region appended to the parent hash
              chain, depth guard; in-world computers are its substrate
```

Data rules:

- **No tech tree, no devices in the engine.** Grep gate: zero device
  nouns (`engine`, `radio`, `train`, `transistor`, `rocket`, ...) as
  types/state-machines in `sim/`; the artifact classifier lives in
  `tests/` and maps artifact material-records + rigid graphs to names.
  A device "exists" when the classifier finds a cluster and its budget
  ledger closes; it persists when agents keep rebuilding it.
- **Machines are budget agents.** Every operating machine carries a
  throughput/loss ledger (fuel in, work out, losses booked); adoption
  of a device class spreads iff its net budget beats the incumbent at
  agent decision points — Phase 9's W5 mechanism verbatim.
- **Claims are reproducible or they are noise.** The claims ledger
  stores intervention templates (world-file patch + initial state
  hashes), so any agent — or CI — can rerun the experiment from the
  log; unfalsifiable claims can't accumulate status.
- Nested worlds inherit determinism or the run dies: child final hash
  recorded in parent log; replay reproduces it bit-for-bit or the
  honesty tax fails.

## Work packages

W1 enables everything (research loop + instruments); W2→W3→(W4,W5)
follow the historical dependency the roadmap lists, but each can also
be found in any order the agents try; W6 needs W1+W4-grade instruments;
W7 last.

### W1 — Research: exploration, instruments, replication

- [ ] Exploration-bias policies (Phase 9 W2 re-used): agents may spend
      budget varying parameters of situations they manipulate;
      experiments = logged interventions with claim artifacts.
- [ ] `metro/` calibration maps; instruments extend world-model
      calibration radius beyond skin (microscope-analog, telescope-
      analog are later W's applications of this one file).
- [ ] `sci/` claims ledger + replication mechanics; school/paradigm
      statistics as emergent shapes.
- [ ] **Tests:** an unattended world yields no claims (no free science);
      a real effect with instrument sensitivity above its size gets
      replicated within generations, a fake one gets withdrawn; claim
      replay from log reproduces the original result bit-for-bit.

### W2 — Heat engines and the transport chain

- [ ] Boilers (Phase 5 pressure-vessel records, honest fracture deaths),
      engines doing Phase 6 work against loads; metallurgy ladder is
      Phase 5's steel runbook, re-entered as artifacts.
- [ ] Transport milestones as work ledgers: displacement hulls, wheel-
      rail contact (Phase 5 friction), lifting surfaces (continuum
      lift/drag), depth hulls, rotors.
- [ ] **Tests:** boiler failure rate tracks overpressure events (zero
      failures is a fracture-term bug, file upstream); engine efficiency
      strictly < Carnot, entropy ledger closes per stroke; each transport
      class's net-joules-per-trip beats its predecessor where adopted,
      and adoption radius follows budget gradient (Phase 9 replay).

### W3 — Electricity: generation, grids, timing, traffic

- [ ] S15 regimes live: capacitors store, inductors resist change,
      transmission lines carry timing; dynamos/motors both directions
      (Phase 6 W5 induction, time-reversed honestly).
- [ ] Grids: generation-load balance as flux ledger, fault propagation
      (cascade as ledger event, not drama); clocks from Phase 6
      oscillators; traffic as routing attractors on the road network.
- [ ] **Tests:** grid frequency-analog stability vs load steps (shape);
      a storm-analog fault cascades and recovers with losses booked;
      traffic congestion emerges from budget-minimizing agents on a
      fixed network and re-equilibrates after a link closes (Braess-
      style surprises logged as discoveries, not patched).

### W4 — Radio, radar and reading the sky

- [ ] Spark-gap → detection → modulation on S15 propagation; ionosphere-
      analog reflection from Phase 4 ionization + Phase 6 transport;
      radar = echo timing off real topography.
- [ ] Telescope-analog via `metro/`: in-world observers probe lazy star
      cells (Phase 7 `astro/` contract — lazy means lazy *for the
      player*, never for a native astronomer) and the CMB-analog sky.
- [ ] Rockets out of gravity: computed momentum exchange (Phase 6) on
      Phase 4 reaction heats; orbit = Phase 7 gravity's own mechanics,
      satellites observing lazy stars and weather as the first payload
      - the space chain (waves observed -> rocket -> satellite -> ship)
      is this ladder, not a separate one.
- [ ] **Tests:** signal range vs power and ionization state (directions);
      radar returns a hill where the world file has one; a rocket's
      insertion orbit equals what the Phase 7 astro ledger integrates
      from its logged thrust events (navigation from physics, not
      tables); **the claims
      ledger ends the run with a sky paper whose expansion-law estimate
      sits in the S5 band** — engine cosmology recovered by world
      cosmology, the phase's signature artifact.

### W5 — Computing and nested worlds

- [ ] Doped-crystal switches (Phase 5 direction), switching networks
      that compute; programs = agent-authored artifact sequences
      (bookkeeping first — ledgers eat the world, honestly).
- [ ] `nest/`: child instances with parent-lane seeds, appended log
      regions, depth guard; in-world computers are the first hosts.
- [ ] Brute-force test arena: machine-policy vs biological agents at a
      timing game the world contains.
- [ ] **Tests:** a computer reproduces a claims-ledger experiment
      end-to-end from stored artifacts; nested child replays
      bit-identical, depth-2 refused with a logged refusal event;
      machine win-rate rises with hardware generations while its energy
      bill stays in the ledger (brute force has a price).

### W6 — The biotech ladder and medicine

- [ ] Microscope-analog (W1 instrument) reveals Phase 8 population
      dynamics at cell scale → germ-analog theory as a replicated
      claim → medicine as dose-response chemistry (Phase 4 kinetics on
      Phase 8 bodies).
- [ ] Ladder: breeding (Phase 9 W6) → trait optimization → mould-
      derived inhibitor-analog drugs (Phase 8 W5 chemistry as mined
      reality) → template-splicing edit-analog (S10 channels used as
      tools, every edit a logged chemistry event).
- [ ] **Tests:** mortality curves bend after medicine adoption in the
      demography ledger; antibiotic-analog adoption selects resistant
      lineages (Phase 8 arms race, now in hospitals); **one edited
      N-fixing-analog symbiont lineage measurably shifts the Phase 7
      reservoir flux** — the loop back into the planet is the test.

### W7 — Networks, memes and the freeze

- [ ] `net/`: packet routing on physical links; latency from
      propagation, nothing virtual.
- [ ] Meme statistics: variant diffusion with net ON vs OFF — the
      difference is measured and reported, the phase's thesis in one
      number pair; platforms = coalition-statistics seeds (Phase 11
      opens that door, this phase only hangs the hinge).
- [ ] Artifact-classifier CI (test-side), no-tech-tree grep gate,
      freeze `sci::` + artifact-ledger contract (below); D10 in
      `spec/decisions.md`.

## Performance budget (fill from W1–W3)

| Path                                        | Budget           | Measured |
|---------------------------------------------|------------------|----------|
| engine stroke step (10³ cylinders)          | < 2 ms           | ___      |
| grid balance step (10⁴ nodes)               | < 5 ms / tick    | ___      |
| ray/echo pass (radio, 10³ links)            | < 1 ms           | ___      |
| claims-ledger op (file/replicate)           | < 100 µs         | ___      |
| packet route (10⁴ links)                    | < 2 ms / tick    | ___      |
| nested child step vs parent tick ratio      | ≤ 10⁻²           | ___      |
| industrialization acceptance (100 yr in-region, offline) | < 90 min wall | ___ |
| meme on/off diffusion CI lane               | < 10 min wall    | ___      |

## Interface exposed to Phase 11 (people & society)

> Phase 11 may read: agent coalition graph (Phase 9 `socia/`), the
> `sci::` claims ledger, the artifact ledger with per-machine budget
> readouts **and ownership-transfer events + compressed-agent holdings
> (seam S18, owed upstream: owning must be an engine fact before
> Phase 12 can price anything)**, `net/` topology/latency, and
> grid/wallet-grade flux ledgers.
> Phase 11 may write: **collective-choice events only** — norms as
> sanction patterns agents *sense and predict* (environment, never
> policy edits — seam S17), laws as enforcement events executed
> by coalitions through the same Phase 6/8 event channels any agent
> uses. Society prices and steers machines; it never adds machine
> physics — the boundary between economics and engineering is this
> freeze line.

## Verification strategy

1. Oracle: `tests/oracle/tech/` — Carnot ceiling checks, boiler fracture
   Weibull-analog shape, diffusion on/off meme ratio band, CMB recovery
   band (= S5's numbers), lift/drag sanity shapes.
2. Possibility-not-destiny: every milestone test asserts ordering and
   possibility (if X adopted, then Y beats X), never that X happened;
   skipped milestones become dated surprises, per Phase 9's rule.
3. Reproducibility fuzz: CI re-runs random logged experiments from the
   claims ledger; non-reproducible "replicated" claims fail the run —
   science's own fraud check, run mechanically.
4. Honesty tax: nested-child hash equality nightly; artifact classifier
   stability under perturbation (a machine renamed by noise =
   classifier bug, not engine bug).
5. Surprises ledger: paradigm shapes, whether radio precedes flight,
   Braess anomalies, meme-death-rate distributions, any in-world
   scientist reproducing our own constants better than we asked.

## Sequencing

```
Wk 1-2         Wk 2-4           Wk 4-6             Wk 5-7           Wk 7-9
─────          ─────            ─────              ─────            ──────────
W1 research +  W2 heat +        W3 electricity     W5 computing     W7 nets+
metro + claims transport        (needs S15)        +nested (S16)    memes+freeze
W6 ladder starts                                   W6 medicine      gate Phase 11
with instruments (W4 sky in parallel under W1) ────┘
```

## Risks

| Risk | Mitigation |
|---|---|
| Magnetostatic EM can't carry circuits/radio even after S15 | S15 lands regime-by-regime with red-first device tests (capacitor first, radio last); no lumped fudge inside Phase 10 — the inherited Phase 6 rule binds |
| Tech explosion outruns the test harness (100 yr → singularity in one run) | nested depth guard, brute-force price in-ledger, adoption gated by agent budgets (expensive tissue principle, scaled up) |
| Technology too slow: acceptance never industrializes in feasible time | world file concentrates coal-analog + ore + navigable water near the plateau settlement (geography, allowed); missed milestones are surprises, never scripted |
| Claims ledger replays drift (experiment templates reference live state) | claims store intervention template + initial-state hashes from the log, never pointers to mutable world |
| Nested sim becomes a second engine nobody audits | `nest/` is a thin consumer of S16: child = the same engine with different constants; depth 1; child log region is part of the parent hash chain — no shadow physics allowed |
| Biotech tests imply eugenics-shaped selection language | tests stay mechanistic: trait frequencies, selection coefficients, flux ledgers; the social meaning is Phase 11/12's to have |
| Doping direction-only turns out direction-wrong for the switch class | Phase 5's pre-named risk row binds: whole-class carrier fix upstream at Phase 4 level, documented; relay-analog fallback (mechanical/thermal) keeps computing's *logic* testable while hardware waits |

**Gate:** Phase 11 starts when: the industrialization acceptance run is
green offline-nightly (engine-in-entropy-ledger, grid balances, radio
over the hill, CMB paper in band, computer replays a claim, nested child
replays bit-identical, edit-analog moves the planet ledger, memes
diffuse faster on-net), the possibility-not-destiny audit of skipped
milestones is filed as surprises, S15/S16 tests are merged upstream,
D10 is in `spec/decisions.md`, and the `sci::` + artifact-ledger line is
frozen in `spec/interfaces.md`.
