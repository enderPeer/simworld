# Phase 7 — Planet & Space

**Goal:** point the Phase 6 physics layer at planetary scale and geologic
time and let a world happen: a debris disk accretes into differentiated
planets, mantles drag plates, surfaces cycle water and carbon for
billions of years under a sun that is just another Phase 2 star cell —
accretion, tectonics, weather, climate and the CMB clock all **fall out
of the layers below**, scripted by no scenario. Phase 7 is the first
phase that runs mostly in jump-state: the acceptance story spans 4 Gyr
and must still replay bit-for-bit.

**Prerequisites (hard gate, from Phase 6 + the seam round):**

- `physics::state` + the Phase 7 BC-only contract frozen; manifest
  jump-state transparency green; energy/entropy ledgers close every tick.
- Seam round **S1–S5** (see `spec/seams.md`) landed upstream with
  red-first tests: rotating-frame term in the continuum (S1), general
  viscoelastic relaxation in `solid/` (S2), vapor→droplet heterogeneous
  nucleation kinetics (S3), the gravity-coupling amendment written into
  `spec/constants.md` with its version decision (S4/S9), and the
  expansion-law anchor decision recorded (S5).
- Phase 5 geo (P-T-t rock records, compaction, 10⁵-yr creep jump) and
  Phase 2 stellar-cell acceptance green in CI.
- Seam **S12** (photochemistry channel class in Phase 4, surfaced later
  by Phase 8 planning) landed before W5: the photolysis terms here are
  its first consumer.
- `tests/oracle/physics/` bands green — Phase 7 inherits every lower
  error band and is where several of them finally get spent.

**Definition of done:** from a gas-and-dust ring with a seeded
composition (the documented initial condition, decision **D6** below)
the engine accretes 2–3 planets in ~10 Myr of sim time; the inner one
**differentiates by falling** — metal core, silicate mantle, crust,
density order unscripted — and a giant impact, if geometry offers one,
throws off a Moon-analog (record the outcome, never force it). Its
mantle convects on geological timesteps, drags a mobile lid into moving
plates, subducts sediment, and builds mountains that rain then wears
down; the weathering–CO₂ loop holds the surface habitable on a
**plateau shape over 4 Gyr** while the simulated sun's luminosity ramps
up (a steeper ramp burns more CO₂ — the negative feedback is visible in
the flux ledger). The water cycle closes at planetary scale — evaporated
mass equals precipitated mass per sim-year in the ledger — currents turn
with the planet's rotation, clouds nucleate on dust and sea-salt aerosol,
deserts sit under the descending branch, and ice ages come and go with
the orbital cycles integrated from the gravity module (Milankovitch
**presence**, not dates). Lightning fixes nitrogen at a measurable rate,
carbonate weathering buffers the ocean, and abiotic sinks balance the
photochemical O₂ source — an anoxic baseline that Phase 8 can then blow
up. The sun is the Phase 2 star cell run 4.6 Gyr by jump with the right
luminosity-rise shape; surface UV dose under the simulated column lands
in band, and the W2 geodynamo field shields the surface unevenly — more
dose under the anomaly (shape). The engine's own expansion clock matches
the CMB anchor (2.7 K today) within the band S5 sets. And a second star
system costs nothing until a probe asks for its spectrum — summaries
until then, identical hashes after.

---

## Scale contract (what "planetary" means here, numerically)

- **Bodies layer:** disk ringlets ~10², resolved bodies ≤ 5·10³, then
  ringlet-averaged accretion after the first Gyr of clumping.
- **Planet summary layer:** 1 record per planet (mass, spin, orbital
  elements, reservoir totals) — this is what jump-state rides on.
- **Resolved strip:** acceptance planet = 48×24 surface columns × 8 air
  levels ≈ 10⁴ columns ticking; everything else on the planet rides
  summaries with error budgets.
- **Time:** accretion 10 Myr, tectonics/climate plateau 4 Gyr
  (nightly-offline), sun 4.6 Gyr by jump. LOD discipline (S7) is a
  first-class deliverable, not a Phase 15 surprise.

## Architecture

```
sim/
  planet/
    accrete/    orbiting-bodies layer (ring-averaged N-body on the W1
                gravity module), Hill-scale merge events, giant impacts;
                Moon-analog is an outcome the ledger records
    interior/   differentiation (gravity + melt + density from mat
                records), mantle convection via S2 viscoelasticity on
                geological timesteps, core: liquid metal + W5-P6
                geodynamo at planetary scale → field summary
    tecton/     mobile lid: mantle traction breaks the lithosphere into
                plates; plate motion = the Phase 6 tectonic BC driving,
                authored here; subduction recycles mat rock records,
                orogeny = uplift bookkeeping, volcanism = melt reaching
                the surface
    surface/    the resolved strip: ocean, regolith, air boundary layer;
                rain/runoff/erosion (Phase 5 weathering + Phase 6 fluid
                transport), sediment → compaction → rock on burial paths
    climate/    insolation from the sun cell + orbital elements; albedo
                from surface optics (Phase 5); greenhouse from Phase 4
                species opacities + Phase 6 transport; ice–albedo and
                weathering–CO₂ thermostats as ledger feedbacks;
                S20 (owed upstream, Phase 13 planning): a bubble-scale
                near-surface tracer channel — passive advect-diffect-
                deposit ~10× finer than the columns — so env(cell) can
                answer local concentration questions at settlement
                resolution
    cycles/     reservoir graph (air / ocean / rock / sediment) with the
                flux ledger: C via carbonate–silicate loop, N via
                lightning NOx + hydrothermal, O sources/sinks; abiotic
                baseline — Phase 8 plugs biology into these same edges;
                S19 (owed upstream, Phase 13 planning): flux ledger
                edges grow a sparse downstream producer-attribution
                tag (industrial emitters only; natural flux stays
                untagged — the tag's absence is background data)
    env/        radiation environment: column shielding from line
                opacities (Phase 3/6), surface spectral bands on the
                Phase 6 light contract, particle dose from the sun +
                field geometry (W2 dynamo) — the Phase 8 hard gate lives
                in this file
    astro/      solar-system integration (Phase 6 gravity, symplectic),
                star cells on demand for other systems (Phase 2 kernel,
                memoized), expansion-law/CMB timeline anchor reads
    lazy/       LOD authority: promotion/demotion rules between strip,
                summary and bodies layers; every demotion reconciles the
                ledgers inside a published error budget
```

Data rules:

- **Ledgers everywhere.** Reservoir sums (C, N, O, water, mass, charge)
  are exact per tick inside the strip and bounded across LOD boundaries:
  strip sums must match the planet summary within the budget the `lazy/`
  table publishes. A demotion that loses mass is a hard fail, same
  discipline as the Phase 6 entropy ledger.
- Phase 7 writes **boundary conditions and events only**, exactly as its
  own Phase 6 contract demands: plate velocities, geothermal floor flux,
  insolation curves. It never edits cell state or material records
  directly; volcanism deposits via Phase 4 species events, erosion is
  carried by Phase 6 advection.
- Disk composition is the project's first **seeded initial condition**
  (D6): volatile and metal budgets read from an offline Phase 2 stellar
  yield run (one prior-generation star, cached as a build constant with
  its run seed and log). No new physics numbers, and the roadmap's
  "seed vs emerge" open question is formally answered: seeded once,
  documented, versioned.
- Long jumps re-anchor: every 10⁶-yr jump segment ends with an orbital +
  ledger consistency check against the summary layer; drift beyond
  budget fails the run, not the band.

## Work packages

W1 is the root; W2 needs W1 (a planet must exist to layer); W3 needs
W2's field of plates; W4 needs W1+W3 (orbits) and the S1–S3 seam fixes;
W5 needs W3 (weathering) + W4 (rain, lightning); W6 is parallel from
week 3; W7 last.

### W1 — Accretion, orbits, the lazy sky

- [ ] Ringlet + bodies layer on the Phase 6 gravity module; symplectic
      integrator (4 Gyr matters more than one tick being fancy);
      Hill-capture and merge as logged events with mass/momentum books.
- [ ] Ringlet-averaging after clumping, validated against a full-body
      window (shape test: same end-states, ±one body).
- [ ] `astro/`: second star systems compute lazily on probe ask; CMB
      anchor + expansion-law decision (S5) wired as the timeline read.
- [ ] **Tests:** ring with one dominant mass clears its feeding zone on
      the analytic timescale shape; two-planet resonance appears when
      geometry allows it, unforced; lazy star: zero cost until probed,
      probe twice ⇒ identical memoized spectrum, replay hash unchanged.

### W2 — Interior: layers, mantle, field

- [ ] Differentiation: melt + percolation of metal-analog to the center;
      final density profile monotone, core/mantle/crust boundaries are
      phase-transition surfaces from Phase 4/5, not radii set in code.
- [ ] Mantle convection on S2 viscoelasticity with 10⁵-yr jump steps
      (extends the Phase 5 ice-creep discipline to a whole mantle).
- [ ] Liquid core + Phase 6 dynamo at scale → dipole summary; field
      strength and reversal *attempts* are outputs.
- [ ] **Tests:** undifferentiated seed → density order in band (shape,
      iron-analog below silicate-analog, crust floats); mantle Rayleigh
      crossing → convection cells appear; stagnant lid forms when the
      crust is cold enough (the failure mode is the test); dynamo on
      above the threshold set by core size, off below.

### W3 — Plates, volcanism, mountains, weathering loop

- [ ] Lithosphere breaks into plates under mantle traction (fracture
      criterion from Phase 5 toughness — the same equation as the
      hammer-drop test, at 6000 km); plate kinematics authored as the
      Phase 6 tectonic BC.
- [ ] Subduction recycles rock records (their P-T-t paths continue),
      arc volcanism emits Phase 4 species, orogeny uplifts, and the
      weathering term (Phase 5 W4, rain-fed since Phase 6) closes the
      CO₂ drawdown edge of the carbon cycle.
- [ ] **Tests:** spreading center + subduction pair emerge from the
      traction field, not a preset; a volcanic pulse raises atmospheric
      CO₂-analog and the plateau recovers on weathering timescales
      (recovery ratio banded, the mass ledger closes to the bubble);
      mountain range grows where convergence focuses, erodes downstream
      in the sediment ledger.

### W4 — Oceans, air, weather, climate, ice ages

- [ ] Rotation term (S1) live: geostrophic balance appears in currents
      and jets; Coriolis deflection sign follows spin direction.
- [ ] Water cycle at scale with S3 nucleation: aerosols (dust from
      deserts, sea-salt from foam-analog cells) seed condensation;
      cloud albedo feeds back on insolation absorption.
- [ ] Climate feedbacks on the ledger: ice–albedo, water vapor,
      weathering–CO₂; orbital forcing (eccentricity/obliquity from W1
      integration) drives glaciation cycles.
- [ ] **Tests:** rain-out latitudes: wet equator / dry subtropics band;
      gyre circulation turns with the planet (sign test, value loose);
      Milankovitch: glaciation cycles appear at the orbital periods'
      **presence and rough ratio**, dates are a surprise entry if off;
      no permanent ice-covered planet at 1× insolation (runaway test) —
      if it happens, the albedo term is the bug, log it loudly.

### W5 — Cycles and aerosols (abiotic baseline)

- [ ] Reservoir graph + flux ledger: air/ocean/rock/sediment edges for
      C, N, O, P-analog (from rock weathering), water.
- [ ] Lightning NOx from the radiation environment + discharge events in
      moist air; hydrothermal N at the crust; photolysis escape terms.
- [ ] Dust and sea-salt aerosol transport (the machinery later carries
      Phase 13's microplastics with no new code); waste breakdown as
      oxidation/photolysis baselines.
- [ ] **Tests:** fixed-N rate lands in the order-of-magnitude band
      (oracle); ocean carbonate buffering keeps pH-analog in a stable
      band under a 2× volcanic CO₂ pulse; abiotic O₂ stays below the
      visible-photochemistry ceiling (no accidental oxygenation before
      Phase 8 earns it).

### W6 — The sun and the radiation environment

- [ ] Sun = Phase 2 stellar cell, jump-run 4.6 Gyr; luminosity curve +
      spectrum evolution as the insolation input; flare/CME summary term
      for the particle environment (banded shape, ledgered).
- [ ] Surface dose: column attenuation from line opacities (Phase 3/6),
      band fluxes on `physics::light::flux_band`, particle cutoff from
      the W2 field — uneven shielding under the anomaly is the test.
- [ ] **Tests:** 4.6-Gyr luminosity rise matches the ramp **shape**
      (oracle) within band; UV-B-analog surface flux in band for the
      simulated column; the anomaly patch measures more particle dose
      than the dipole patch — direction, not value.

### W7 — Acceptance harness + interface freeze

- [ ] Primordial-system acceptance: seeded disk → planets → differentiation
      → plateau run → environment report, one scripted world file, zero
      scenario code; nightly-offline for the 4-Gyr segment, CI-fast for
      the 10-Myr segment.
- [ ] LOD fuzz: random promotion/demotion storms — strip sums match
      summaries within published budgets every tick; jump transparency
      across all three time layers (accretion, mantle, climate).
- [ ] Cache-off replay: delete accrete/astro memos + lazy tables ⇒
      identical hashes.
- [ ] Freeze `planet::env(cell)` + the reservoir-ledger contract (below);
      budget CI; write the D6 seed-IC decision into `spec/decisions.md`.

## Performance budget (fill from W1–W4)

| Path                                   | Budget            | Measured |
|----------------------------------------|-------------------|----------|
| ringlet force + merge pass (10³ bodies)| < 5 min / 10 Myr  | ___      |
| mantle jump segment (1 cell, 10⁵ yr)   | O(1), < 1 ms      | ___      |
| resolved strip tick (10⁴ columns)      | < 50 ms           | ___      |
| climate feedback update per column     | < 5 µs            | ___      |
| cycle flux ledger per edge             | < 1 µs            | ___      |
| sun jump-run 4.6 Gyr                   | < 1 s             | ___      |
| lazy star spectrum on demand           | < 1 s first, ns   | ___      |
| 4-Gyr plateau acceptance (offline)     | < 45 min wall     | ___      |
| full CI-fast acceptance segment        | < 15 min wall     | ___      |

## Interface exposed to Phase 8 (life)

> Phase 8 may read: `planet::env(cell)` — T, pressure, species partial
> pressures, irradiance spectral bands, liquid-water fraction, nutrient
> fluxes (fixed N, P-analog weathering), particle dose rate, substrate
> (Phase 5 material records) — plus the reservoir graph and its flux
> ledger. Phase 8 may write: **flux events only** — uptake and release
> into reservoirs and species (Phase 4 chemistry); biomass is chemical
> species, a reef is a material, a forest is just very slow weathering
> going backwards. No "organism" state enters the planet layer until
> Phase 9's agents, and Phase 8 owns no clock: it perturbs, the same
> tickers tick.

Phase 8's abiogenesis question is then purely environmental: does the
env+chemistry stack spend its nutrient and energy gradients fast enough
to make replication inevitable? If it doesn't, that is a Phase 7 gap,
not a Phase 8 hack.

## Verification strategy

1. Oracle: `tests/oracle/planet/` — density-order profile, feeding-zone
   clearing timescale, Milankovitch period ratios, lightning-N order of
   magnitude, luminosity ramp, CMB anchor numbers. Shapes banded tight,
   values loose (adopted Phase 5 rule), grep gate extended: no planet/
   moon/continent names, no "Coriolis" constants in `sim/planet/`.
2. Ledger CI: reservoir sums exact per tick in-strip, LOD-bounded across
   layers; the plateau acceptance must close its C and water books
   across 4 Gyr of jump segments (re-anchor checks).
3. Jump transparency at every layer: accretion coarsening, mantle
   segments, climate plateau — final hash equals the ticked reference
   on sampled windows.
4. D6 honesty: the seeded disk composition ships with its generating
   run's seed + log pointer in `spec/constants.md`; cache-off replay
   regenerates it from that run, so "seeded" never means "unverifiable".
5. Surprises ledger: ice-age timing, dynamo reversals, CMB anchor gap,
   desert latitudes — dated lines with measured gaps.

## Sequencing

```
Wk 1-2          Wk 2-4              Wk 4-6              Wk 6-8        Wk 8-10
─────           ──────              ─────────          ──────────    ──────────
W1 accrete +    W2 interior          W3 plates +        W4 climate    W7 acceptance
astro (lazy     (differentiation,    weathering loop    + cycles      +fuzz+freeze
sky, anchor)    mantle, dynamo)      ── feeds W4/W5 ──  (rotation,    gate Phase 8
W6 sun in       (parallel from       (needs S2 seam     thermostats,
parallel        week 3, needs S4)    green)             needs S1/S3)
```

## Risks

| Risk | Mitigation |
|---|---|
| 4-Gyr integrations drift silently | symplectic orbits, jump segments end with mandatory re-anchor checks, ledgers exact-to-budget per segment; drift beyond budget fails the run, never widens a band |
| Mantle convection numerically over-diffusive at 10⁵-yr steps | refinement-convergence CI test on the mantle (Phase 3 grid lesson): convection survives coarsening or the timestep scheme changes |
| Thermostat overshoots to snowball/runaway and the plateau never appears | feedback terms have no free knobs; if the plateau needs tuning, that is a seam discovery — log it, fix the upstream term (albedo, weathering rate law), don't tune the loop |
| Ringlet averaging changes outcomes vs full N-body | overlap-window validation test (same end states) before averaging is allowed to ship |
| Seeded disk composition (D6) read as cheating | it is one IC, generated by the engine's own stellar physics, reproducible from its logged seed; the alternative — simulating galactic chemical enrichment — is out of scope and stays written down that way |
| Biogeochemistry scope creep (life appears in Phase 7 by accident of optimism) | hard line: cycles close abiotically or the open edge is a documented Phase 8 prerequisite; a test asserts abiotic O₂ stays below the photochemical ceiling |
| CMB anchor fails the single-component expansion law badly | S5 decision is made before W1 turns green; if a radiation+matter correction is needed, it is a Phase 0 D5 amendment with a written justification, not a fudge factor |

**Gate:** Phase 8 starts when the primordial-system acceptance (disk →
planets → differentiation → 4-Gyr plateau → env report) passes offline
nightly with ledgers closed, the LOD fuzz is green, seam round S1–S5
(+ S12, retrofitted) tests are upstream and merged, D6 + the anchor
decision are in
`spec/decisions.md`, and `planet::env` + the reservoir-ledger line are
frozen in `spec/interfaces.md`.
