# Phase 5 — Materials & Substances

**Goal:** aggregate 10²³ species into **materials**: phase + microstructure
+ processing history per cell, with hardness, ductility, melting point,
conductivity and viscosity all **derived from composition and what was
done to the sample** — no per-material constants, no material names in
`sim/`, clay→ceramic and quench→hard-steel fall out as consequences.

**Prerequisites (hard gate, from Phase 4):**

- `chem::species(graph)` + `chem::react(cell)` frozen; organic stress
  test and detailed-balance CI green.
- Catenation test decided carbon-vs-silicon correctly (wood and oil later
  depend on that verdict).
- Surprise ledger open — this phase inherits all chemistry error bands.

**Definition of done:** a scripted test forge and a scripted test kiln,
containing no material names, produce: a ductile metal-analog that work-
hardens and anneals soft; a harder, quench-brittier variant of the same
metal with more of a small-species addition (steel's whole trick,
unscripted); a glass because it cooled faster than nucleation; a fired-
climb ceramic from wet plastic clay; and a wood-analog that is strong
along its fibers and weak across them. Every material record is a
computed summary keyed by `(composition, history)` and deleting the cache
replays it.

---

## Architecture

Materials are **cell-scale summaries over Phase 4 species** — aggregation,
not a new ontology. Chemistry keeps running inside every material.

```
sim/
  materials/
    aggstore/   material record per cell: species composition (Phase 4
                graphs), phase, microstructure summary, history digest
    phases/     multicomponent phase equilibrium from Phase 4 thermo:
                solid/liquid/gas fractions, segregation, eutectics
    kinetics/   nucleation + growth rates vs (T, undercooling, composition)
                — quench/anneal/glass all live here
    mech/       bonding-type fractions (Phase 2 ionicity, Phase 4 curves)
                + grain size + porosity → E, hardness, ductility, fracture
                toughness, as tensors when structure is anisotropic
    transport/  thermal + electrical conductivity, viscosity, diffusivity,
                permeability from porosity; mobile ions → electrolytes
    geo/        rock records: igneous (cooling path), metamorphic (P-T
                path), sedimentary (compaction+cement) — a P-T-t history
                per rock cell, resumable via jump-state
    hist/       history digests: bounded feature set (peak T, cooling
                rates, strain path, anneal time) — never raw event logs
```

Data rules:

- A material record = `(composition digest, phase fractions, microstructure
  summary {grain size, porosity, texture, fiber dirs, dislocation density,
  carbon-analog content}, history digest)`. Canonical signature → property
  cache rows. Third layer with delete-and-recompute discipline.
- Microstructure summaries are the **only** permitted lossy step in the
  whole stack, so: every summary carries an error budget, and CI re-derives
  sampled cells from explicit particle runs to keep it honest.
- History digests are bounded (fixed feature count, older history folds
  into statistics). Unbounded history = unbounded cache = silent table.
- Mechanics (Phase 6) writes stress/strain **history events** into records
  via `materials::note_deformation`; that is the one write-back path the
  Phase 4→5 contract amendment allows, and it is logged like everything
  else.

## Work packages

W1 is the root. W2 feeds W3, W4, W5; W5 can overlap W3/W4; W6 last.

### W1 — Aggregation store

- [ ] Material record layout + canonical signatures; per-cell phase
      fractions from `chem` phase state.
- [ ] Observation-tier awareness: inside the bubble, records tick with
      chemistry; outside, they ride jump-state summaries (Phase 1 D5).
- [ ] **Tests:** a cell of pure water-analog reports {phase: liquid,
      composition: one species}; a granite-analog reports {solid,
      multi-species, grain summary}; signature collisions fuzzed at 10⁶
      random compositions.

### W2 — Phase equilibrium + kinetics

- [ ] Multicomponent equilibrium: solid solution limits, segregation on
      freeze, eutectic troughs — from Phase 4 ΔG only.
- [ ] Nucleation/growth rate curves; cooling-rate → microstructure map;
      annealing as recovery of dislocation summary.
- [ ] **Tests:** salt-analog lowers the water-analog freezing point in
      band; a eutectic composition appears as the lowest-melting mix of
      two named-in-oracle metals without either melting lowest alone;
      quench vs furnace-cool of the same melt gives fine vs coarse grain
      and the recorded history digests differ only in the cooling feature.

### W3 — Mechanical properties

- [ ] Bonding-fraction mix (metallic/ionic/covalent from Phase 2/4 data)
      → baseline E/hardness/ductility; grain size → Hall-Petch-style
      strengthening **fit from two anchors only** (calibration constants,
      not species); porosity softens; anisotropy from texture/fibers.
- [ ] Fracture: crack advances when stored elastic energy exceeds the
      bond-energy surface term → toughness is derived, glass vs metal
      behavior is a microstructure statement.
- [ ] **Tests:** carbon-analog ladder in the metal-analog is monotone
      hardening then over-carbiding (the band may be wide, the shape may
      not be wrong); wet clay-analog plastic, fired ceramic-analog brittle;
      wood-analog axial/cross strength ratio > 3 with no fiber constants —
      geometry of polymer-analogs from Phase 4 does it.

### W4 — Geology materials

- [ ] Rock records from P-T-t paths; compaction + cementation for
      sedimentary; metamorphic recrystallization on burial paths.
- [ ] Weathering = Phase 4 surface chemistry + rain (Phase 6 later feeds
      it for real) → soil as a material class, permeability included.
- [ ] Magma: viscosity from composition (silica-rich thick), dissolved-gas
      exsolution pressure — explosive-vs-effusive is an output.
- [ ] **Tests:** slow-cool vs fast-cool test magma gives coarse vs fine
      rock-analogs with matching strength; ice-analog creeps under load on
      a geological timescale via jump-state (10⁵ yr skip, O(1)/cell).

### W5 — Transport properties

- [ ] Thermal: phonon term from bonding stiffness + porosity scattering;
      electrons add conduction in metallic fractions.
- [ ] Electrical: metals / ionic conductors (melts, electrolytes) /
      insulators from the same terms; **doping trend**: a trace species
      from the registry changes carrier behavior in the right direction
      (band wide — Phase 10 only needs the direction, not the value).
- [ ] Viscosity from chain-length distributions (oil-analog ladder
      monotone); diffusion coefficients memoized per (species, medium).
- [ ] **Tests:** metal-analog ≫ doped-semi-analog > insulator-analog at
      room T with the crossover ordering in band; hot glass-analog flows
      on human timescales, cold does not — one curve, no constants.

### W6 — Acceptance harness + interface freeze

- [ ] **Manifest test:** a scripts-only forge/kiln/press/loom produces
      ~100 oracle-named materials (oracle maps signatures → real names);
      every property in band; anything unnamed by the oracle is logged as
      an emergent invention (and celebrated, not deleted).
- [ ] History-fuzz: random thermal/strain cycles, 10⁵ material evolutions
      — digest sizes stay bounded, no crashes, energy audits.
- [ ] Cache-off replay of the whole manifest → identical hashes.
- [ ] Freeze `mat::record(cell)` + `mat::note_deformation` contracts.

## Performance budget (fill from W1–W3)

| Path                                   | Budget            | Measured |
|----------------------------------------|-------------------|----------|
| material read (cache hit)              | < 10 ns           | ___      |
| property recompute on history event    | < 10 µs           | ___      |
| phase equilibrium solve per cell tick  | < 2 µs            | ___      |
| nucleation/kinetics step               | < 5 µs            | ___      |
| new material first compute             | < 1 s             | ___      |
| full manifest rerun                    | < 5 min           | ___      |
| 10⁵-yr geological jump on one rock     | O(1), < 1 ms      | ___      |

## Interface exposed to Phase 6 (physics/mechanics)

> Phase 6 may read: `mat::record(cell)` — phase fractions, property
> tensors (E, hardness, toughness, density, conductivities, heat
> capacity), surface energies, permeability.
> Phase 6 may write: deformation/fracture/thermal exposure **events**
> through `mat::note_deformation` only. Phase 6 never edits a property
> directly — it changes the cell's story, and the record recomputes.

Phase 6's continuum mechanics therefore never disagrees with Phase 5;
it is the customer, with a write-back that is only ever a new event.

## Verification strategy

1. Oracle names the manifest, never the engine: `tests/oracle/materials/`
   maps signatures → real names + bands; `sim/materials/` passes a grep
   gate for material names (mirrors the Phase 3 hydrogen exception rule —
   here the analytic anchors are the pure species from lower layers).
2. Sampling re-derivation: explicit particle-level runs of a few hundred
   atoms recompute summary properties for sampled records nightly — this
   is the honesty tax on the one lossy layer.
3. Surprises ledger continues: emergent alloys/composites that don't match
   reality get dated entries with measured gaps.
4. Cache-off replay + digest-bound checks in CI alongside everything above.

## Sequencing

```
Wk 1-2        Wk 2-3           Wk 3-4            Wk 4-5          Wk 5-7
─────         ──────           ─────────        ──────────      ──────────
W1 aggstore → W2 phases +   →  W3 mech tests    W5 transport    W6 manifest
              kinetics         (steel ladder,   (doping trend,  +fuzz+freeze
                                 clay/glass)      permeability)  gate Phase 6
                               W4 geo in
                               parallel track
```

## Risks

| Risk | Mitigation |
|---|---|
| Microstructure summaries too lossy → wrong steel/wrong wood | error budgets per feature + nightly particle re-derivation; a feature that fails re-derivation twice gets added to the digest (grow the summary, never hardcode the result) |
| History digest explosion (coarse-grained tables by another name) | bounded feature count is a CI assertion; new features require a written justification line |
| Property bands so loose everything passes | band the **shapes** (monotone ladders, crossovers, ratios) tightly and the **values** loosely — shape errors are bugs, value gaps are logged surprises |
| Doping/semiconductor emergence too crude for Phase 10 | direction-only requirement; if direction is wrong for a whole class, that class's carrier term gets a Phase 4-level fix, documented |
| Phase 6 needs a property we can't derive | it is contractually a Phase 4/5 bug — the amendment process is a new derived term, never a Phase 6 constant |

**Gate:** Phase 6 starts when the manifest passes at 100 materials with
zero names in `sim/`, particle re-derivation is within error budgets,
digest bounds hold, and `mat::record` / `mat::note_deformation` are frozen.
