# Phase 6 — Physics Layer

**Goal:** make the cell grid *move*: gravity, collisions, fluids, heat,
light, sound and electromagnetism as **operators on the Phase 5 material
records** — every wave speed, heat flux, efficiency ceiling and field
strength an output of what the cell is made of. No new ontology: Phase 6
is the first *customer* of the whole stack below it, and the one layer
that writes nothing directly — only logged events.

**Prerequisites (hard gate, from Phase 5):**

- `mat::record(cell)` + `mat::note_deformation` frozen; the 100-material
  manifest passes with zero names in `sim/`; particle re-derivation green.
- Phase 4 detailed-balance CI green (thermo inherits its error bands) and
  Phase 5 history-digest bounds proven.
- `spectra::` line-list read contract (Phase 3 W3) live — light and
  radiation read it and nothing else.
- Surprises ledger open; entropy debt bookkeeping from Phase 1 W3 jump
  states is green in CI (Phase 6 thermodynamics must reconcile with it).

**Definition of done:** a cold fluid cell with a hot floor self-organizes
into convection rolls that carry the right heat flux (Nusselt-scaling
shape in band, value a logged surprise at worst); the same cell with a
cold lid rains back what evaporated from the floor. A piston-analog over
a heated cylinder lifts a weight — work, heat and entropy close per
tick, the ceiling is Carnot-like, and a steeper temperature difference
always lifts more. A dropped hammer leaves a dent and a work-hardened
history in metal-analog plate; glass-analog shatters instead, with new
fracture surface area paid for out of toughness. A cavity with a pinhole
emits the Phase 1 blackbody shape, and a cool gas cell between source
and probe casts absorption lines **at the Phase 3 line positions** —
Kirchhoff falls out, nobody wrote it. A convecting molten-metal-analog
cell amplifies a seed field into a dipole above threshold and lets it
decay below; sound from a scripted explosion arrives at a probe at the
time derived from `mat::record`, and bends upward across a temperature
gradient. All of it replays bit-for-bit; jump-state cells close their
ledgers on resume with hash-transparency.

---

## Architecture

```
sim/
  physics/
    continuum/  cell conserved fields (ρ, momentum, energy, species-mix
                fractions); advect → diffuse → couple operator split;
                viscosity/conductivity/permeability read from mat
                records, never re-derived here
    gravity/    pairwise below N ≤ 10⁴ cells, one dimensionless coupling
                in the constants table (amendment, see Risks); free fall
                is a flux, orbits are emergent; reused wholesale by
                Phase 7 for orbits/tides
    solid/      stress tensor evolution per cell, contact between cells,
                fracture when stored elastic energy > mat toughness term;
                all permanent change leaves as note_deformation events
    heat/       conduction (mat thermal conductivity), advection coupling,
                phase change consumed from Phase 4/5 equilibrium — latent
                heat comes from their ΔG, no transition constants here;
                per-cell entropy ledger reconciling Phase 1 jump debt
    radiation/  photon energy groups (~8) transported per cell; opacity =
                line lists (Phase 3, Doppler+pressure broadened) +
                continuum terms from mat records, memoized by
                (composition, ρ, T) signature — cache discipline, not a
                table; emission detailed-balance against absorption
    wave/       no separate solver: pressure waves read off the continuum
                operator's own characteristic speeds; hearing (Phase 14)
                and sonar (Phase 10) will sample the pressure history
    em/         charge conservation over Phase 3 ionization balance,
                currents from mat electrical conductivity, induction +
                magnetostatics; dynamos are an outcome, not a module
```

Data rules:

- Phase 6 owns **no state below the cell**: it advances conserved fields
  and writes events. A cell's material identity changes only through
  `mat::note_deformation` / Phase 4-5 chemistry — physics changes the
  story, the record recomputes.
- One entropy ledger per cell: every diffusive, radiative and phase term
  books its `đS`; the ledger may only shrink via logged export. The
  engine is a *test*, never a module — any "engine code" in `sim/` is a
  spec violation.
- Wave phenomena are not a subsystem: sound speed, refraction and shock
  heating are consequences of the continuum operator reading `mat::record`
  (E, ρ, phase fractions). One operator, two acceptance stories.
- Jump-state: a cell whose net flux magnitudes sit under a published
  per-tick budget propagates by the closed-form linear decay of its own
  terms; on resume the ledger must close and the hash match the
  ticked reference (the M2/M4 transparency discipline, extended).

## Work packages

W1 is the root. W2 starts parallel in week 2; W3 needs W1; W4 needs
W1+W2; W5 needs W1 (sound) and W2 (dynamo convection); W6 last.

### W1 — Continuum + gravity

- [ ] Conserved-field layout + advect/diffuse split; CFL substepping
      from mat-derived sound speed; hydrostatic and free-fall limits.
- [ ] Gravity pass + orbit integration; potential feeds back as flux.
- [ ] **Tests:** two-body orbit closes with energy/angular momentum in
      band over 100 periods; Kepler's third-law exponent in band (shape
      test, oracle data in `tests/oracle/physics/`); a water-analog slab
      sloshes without damping artifacts; mass/momentum/energy audits
      exact per tick to float tolerance.

### W2 — Heat, phase change, entropy ledger

- [ ] Conduction + advection coupling; latent heat and transition points
      consumed from Phase 4/5 equilibrium calls only.
- [ ] Entropy ledger per cell + reconciliation report in every summary;
      jump-state entropy-debt reconciliation against Phase 1 bookkeeping.
- [ ] **Tests:** a hot slab cools to the analytic conduction curve
      (shape); boiling + rain-in-a-box: evaporate, convect, condense at
      the cold lid, precipitate, with the heat flux carried matching the
      latent bookkeeping; the piston acceptance (def-of-done) closes its
      ledger and beats no Carnot-like ceiling across a ΔT sweep.

### W3 — Solid mechanics, contact, fracture

- [ ] Stress evolution under W1 deformation; contact between cells with
      friction from mat surface terms; fracture criterion from the Phase
      5 toughness derivation; fragments are just new cell boundaries.
- [ ] **Tests:** hammer-drop leaves a dent and a work-hardening event in
      the record (re-hit is harder — Phase 5 loop proven from the physics
      side); glass-analog shatters with new surface area paid against
      toughness; wood-analog splits along fibers, not across (Phase 5
      anisotropy showing up in fracture paths).

### W4 — Radiation and light

- [ ] Group transport with emission/absorption paired by detailed
      balance; line opacities from `spectra::` with Doppler + pressure
      broadening; shadowing = attenuation inside the observation bubble.
- [ ] Spectral-band flux contract `physics::light::flux_band(cell, band)`
      — band edges defined by later phases, line positions from Phase 3;
      vision (Phase 14) will be one more reader of this contract, so it
      must carry per-band flux and direction, nothing else.
- [ ] **Tests:** pinhole cavity reproduces the Phase 1 W6 blackbody shape;
      cool gas in front of a source absorbs **at its own line positions**
      and emits the same lines when hot (Kirchhoff, both directions);
      a visible-band flux over a vegetation-analog cell stays inside the
      band Phase 8 will call photosynthetic — with zero biology in sight.

### W5 — Waves and electromagnetism

- [ ] Pressure-history tap on the continuum for wave acceptance (no new
      solver); shock heating across a jump validated against the W2
      ledger.
- [ ] Charge/current continuity over Phase 3 ionization; circuits from
      mat conductivity (metal-analog wire, melt electrolyte); induction;
      magnetic field advection + diffusion in moving conductors.
- [ ] **Tests:** explosion pulse reaches a probe at the `mat::record`
      derived time within band, and refracts away from the cold side of
      a T gradient; a loop-analog with a battery-analog (chemistry!)
      carries current and heats its wire monotonically in resistance;
      dynamo threshold test: faster convection amplifies the seed field,
      slower decays it — threshold behavior banded, field value is a
      surprise entry if it misses.

### W6 — Acceptance harness + interface freeze

- [ ] Manifest acceptance: rain-in-a-box, piston lift, hammer/glass,
      pinhole+gas cell, dynamo cell, wave probe — one scripted world
      file, no physics names in the scripts.
- [ ] Fuzz: random field initializations, 10⁷ cell-ticks — CFL never
      violated, ledgers close every tick, no NaN, energy audit green.
- [ ] Jump-state transparency: full manifest with half the cells
      jump-state ⇒ final hash equals the all-ticked reference (the
      strongest determinism test in the project so far).
- [ ] Freeze `physics::state(cell)` + the Phase 7 line (below); budget CI.

## Performance budget (fill from W1–W3)

| Path                                   | Budget            | Measured |
|----------------------------------------|-------------------|----------|
| continuum step per cell-tick           | < 1 µs            | ___      |
| gravity pass, 10⁴ cells                | < 1 s             | ___      |
| heat + ledger update per cell-tick     | < 1 µs            | ___      |
| radiation transport per group-cell     | < 2 µs            | ___      |
| opacity first-compute (memoized after) | < 100 ms          | ___      |
| fracture/contact event apply           | < 10 µs           | ___      |
| full acceptance manifest               | < 15 min wall     | ___      |
| jump resume of one cell                | O(1), < 1 ms      | ___      |

## Interface exposed to Phase 7 (planet & space)

> Phase 7 may read: `physics::state(cell)` — conserved fields, entropy
> ledger, EM field summary — plus the radiation flux/spectral-band
> contracts and the pressure-history tap. Phase 7 may write: boundary
> conditions and initial fields only — insolation curves, geothermal
> floor flux, tectonic velocity/stress boundary driving — and it drives
> orbits and tides **through the W1 gravity module**, never its own.
> Nothing else crosses the boundary; weather, oceans and mantle
> convection are things Phase 6 *does* when Phase 7 sets the stage.

Phase 7 is the first customer that consumes jump-state at planetary
scale; every budget in the table above is what that scale buys.

## Verification strategy

1. Oracle discipline extended: `tests/oracle/physics/` holds the real
   numbers (free-fall g, sound speeds, a lunar-orbit analog, Stefan–
   Boltzmann, Carnot for named ΔT, Earth dipole moment). A grep gate on
   `sim/physics/` bans derived-constant names (`sound`, `c_sb`, `mu_0`,
   any material word); the only permitted physics numbers are the Phase 0
   irreducible set plus the one declared gravity coupling.
2. Shape-over-value rule (Phase 5, adopted): scaling exponents,
   monotonicities and thresholds banded **tightly**, absolute values
   loosely with surprises logged — wrong shape is a bug, wrong value is
   a ledger line.
3. Ledger CI: entropy + energy audits every tick of every acceptance
   run, plus jump-resume reconciliation; a ledger that closes on the
   ticked path but not the jumped path is a hard fail.
4. Cache-off replay of the whole manifest (opacity memoization deleted)
   ⇒ identical hashes; nightly CI inherits the Phase 0 task.
5. Surprises ledger continues — convection flux constants and dynamo
   values are expected first residents.

## Sequencing

```
Wk 1-2          Wk 2-3          Wk 3-4            Wk 4-5          Wk 5-7
─────           ──────          ─────────        ──────────      ──────────
W1 continuum +  W3 solids +     W4 radiation     W5 waves + em   W6 manifest
gravity         W2 heat         (blackbody,      (dynamo needs   +fuzz+jump
(orbits,        (rain-in-a-box   lines,           convection)    transparency
 hydrostatics)   ledger)         shadows)                         +freeze gate
                                                                Phase 7
```

## Risks

| Risk | Mitigation |
|---|---|
| G is absent from the Phase 0 irreducible constant set | one dimensionless gravity coupling added as a *documented amendment* to `spec/constants.md` with a written justification, anchored once by the orbit test — the only new constant this phase may own |
| Coarse cells can't do turbulence → convection/rain flux wrong | band the scaling **shape**; one global sub-grid flux term calibrated on a single anchor (the rain-box flux), everything else prediction; sampled DNS re-derivation nightly, same honesty tax as Phase 5 summaries |
| Dynamo is threshold-sensitive and may not start | test is threshold *behavior* (amplify-vs-decay crossover), never a field value; if it never amplifies, the induction term gets a Phase-3-level fix, documented — no scripted seed field |
| Group transport too slow or opacity memoization drifts toward a table | groups fixed at ~8; memo rows are signature-keyed and cache-off replay must reproduce them; a memo hit-rate test keeps the lazy path honest |
| Waves and heat silently diverge on who owns compressional heating | one operator owns it (W2 ledger books what W1's characteristic speeds produce); a shock test asserts the ledger pays for the temperature jump |
| Engines, weapons or vehicles get prototyped "to help" | the engine is a *test*; a grep gate on `sim/physics/` plus review checklist item at every milestone — Phase 10 builds machines out of W1–W5 interactions only |

**Gate:** Phase 7 starts when the acceptance manifest passes as one
scripted world, jump-state transparency holds at manifest scale, energy
and entropy ledgers close every tick, the gravity-coupling amendment is
written into `spec/constants.md`, and `physics::state` + the Phase 7
contract line are frozen in `spec/interfaces.md`.
