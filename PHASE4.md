# Phase 4 — Chemistry Layer

**Goal:** put atoms together so that molecules, bonds, reactions,
acids/bases, solvents, polymers and fuels are **outputs of electron
energetics** — no reaction tables, no named compounds in `sim/`, every
combination of everything is computable by construction.

**Prerequisites (hard gate, from Phase 3):**

- `atomic::species(Z, ion)` frozen; periodic table regenerates from solver
  output in nightly CI.
- Spectra + plasma contracts written; ladder-fallback counter green.
- Cache-off replay discipline proven for two layers (nuclei, atoms).

**Definition of done:** put any set of species in a closed cell at any
`(T, ρ)` and the engine either finds no channel or computes a rate —
equilibrium inside the box always lands on the state predicted from the
engine's own formation energies (detailed balance, an internal-consistency
test, not an oracle). Water is **bent and sticks to itself** (ice floats),
methane is tetrahedral, carbon burns, ethylene-analog polymerizes, and an
aspirin-analog appears in a test reactor that never had the word aspirin
in it. A brand-new molecule nobody declared gets discovered by the engine,
gets a registry row, and behaves consistently from then on.

---

## Architecture

```
sim/
  chemistry/
    bonds/      diatomic potential curves: LCAO over Phase 3 radial
                densities + correlation ladder; ionic fraction from
                IP−EA difference (electronegativity = derived, never input)
    molecule/   polyatomic geometry: pair curves + angular terms whose
                directionality comes from valence-orbital shape per atom
    registry/   species store keyed by canonical bond graph — an emergent
                cache, delete-and-recompute must hold (third layer now)
    channels/   reaction channels: candidate product graphs by valence-
                satisfying rearrangement of what is nearby; barrier from
                bond-energy sums (Evans–Polanyi form), memoized by
                (reactants → products) signature
    events/     reaction sampler: proximity + orientation + energy from
                Phase 1 stats; Arrhenius rate from computed barrier
    thermo/     formation enthalpy from bond sums; phase state from
                intermolecular terms (dipole, dispersion from polarizability)
    surface/    surfaces as reaction environments — catalysts emerge, they
                are not flagged
```

Data rules:

- A species is a canonical bond graph + computed scalars (formation
  enthalpy, dipole, polarizability, intermolecular params, phase at
  reference). Nothing stores "reaction X gives Y"; a channel is a
  **memoization of a computation over species records**.
- Reaction discovery is local: candidate products come from rearranging
  bonds among atoms already in collision distance, filtered by valence
  satisfaction (Phase 3 valence counts) and energy. This is why "all
  combinations must work" holds — there is no list to be incomplete.
- Detailed balance is a law the sampler must satisfy by construction
  (forward and reverse rates from the same barrier and ΔH), so equilibrium
  is exact by architecture, and CI checks it anyway.
- No organic/inorganic split anywhere in the code. Carbon chains are just
  a bond-strength accident we get to exploit.

## Work packages

W1 is the root. W2 needs W1; W3 needs W1+W2; W4, W5 parallel after W3; W6 last.

### W1 — Bonds

- [ ] LCAO diatomic curves from `atomic::species` densities; homonuclear
      first, then heteronuclear with the ionic-fraction term.
- [ ] Metallic limit: delocalized-electron term for low-IP atoms in
      condensed neighborhoods (feeds Phase 5 conductors without a new layer).
- [ ] **Tests:** H₂ energy/length in band; N₂ unusually strong+short
      (triple bond, unscripted); NaCl ionic with right lattice-ish
      cohesion; Cs–F more ionic than C–F (electronegativity gradient
      comes out monotone without naming it).

### W2 — Geometry

- [ ] Angular terms from per-atom valence-orbital directionality, computed
      once per atom kind (hybridization as output).
- [ ] **Tests:** methane-analog tetrahedral; water-analog **bent**, dipole
      nonzero; ammonia-analog pyramidal; H-bond network gives water-analog
      density anomaly — solid less dense than liquid, or the test fails
      and ice sinks, which we must not ship.

### W3 — Reaction engine

- [ ] Channel discovery via local valence-rearrangement search, bounded by
      collision neighbors; barrier from bond sums + Evans–Polanyi slope.
- [ ] Event sampling through Phase 1 RNG; memoized channels; electron-
      transfer reactions as first-class (electrochemistry comes free).
- [ ] Surfaces: reactions allowed to route through surface-adsorbed
      intermediates — that is the entire catalyst mechanism.
- [ ] **Tests:** carbon + O₂ exothermic to CO₂-analog; H₂+½O₂→water
      explodes at the right ignition band; an alcohol-analog oxidizes to
      an acid-analog; Haber-analog (N₂ + H₃ → ammonia-analog) reaches
      nonzero yield at hot high-pressure conditions with an iron surface,
      near-zero without it.

### W4 — Thermo & phase state

- [ ] Formation enthalpies, heat capacities (vibrational sums), entropy
      proxies → boiling/melting from intermolecular terms.
- [ ] Autodissociation of the water-analog → pH as an emergent axis;
      acid/base and precipitation fall out as reactions + solubility from
      intermolecular energies (no solubility tables).
- [ ] **Tests:** equilibrium constants inside a closed box match the
      engine's own ΔG (detailed-balance CI); salt dissolves in water-
      analog, sand does not, gold does not (aqua-regia exception is
      allowed to surprise us — record it either way).

### W5 — The organic stress test (plastics, fuels, drugs)

- [ ] Carbon catenation: C–C vs C–O vs Si–O bond strengths come out such
      that long carbon chains are possible and long silicon chains are
      not — this one test decides whether biology later gets polymers.
- [ ] Ethylene-analog polymerizes under pressure+surface; chain lengths
      have a distribution, not a constant.
- [ ] Test reactor: salicylic-analog + acetyl-analog → ester product
      within band of aspirin's formation enthalpy — the engine produced a
      drug **from a world that has no drug concept**.
- [ ] Fuel ladder: methane → propane-analog → diesel-analog trends
      (energy density, boiling point) monotone with chain length.

### W6 — Acceptance harness + interface freeze

- [ ] Fuzz: random species pairs, random `(T, ρ)`, 10⁶ reaction events —
      no panics, energy/atom-conservation audits per event, every product
      graph valence-valid.
- [ ] Discovery test: seed an exotic-but-valenced molecule, confirm the
      engine reacts it correctly with zero registry pre-knowledge.
- [ ] Cache-off replay: delete `registry/` + `channels/`, replay the
      organic stress test, hashes identical.
- [ ] Freeze `chem::species(graph)` + `chem::react(cell)` contracts.

## Performance budget (fill from W1–W3)

| Path                                   | Budget            | Measured |
|----------------------------------------|-------------------|----------|
| new bond curve compute                 | < 100 ms          | ___      |
| channel discovery per collision pair   | < 20 µs           | ___      |
| reaction event apply                   | < 1 µs            | ___      |
| species/phase read (cache hit)         | < 10 ns           | ___      |
| closed-box 10⁷-event equilibrium run   | < 10 s wall       | ___      |
| organic stress test full rerun         | < 5 min           | ___      |

## Interface exposed to Phase 5 (materials)

> Phase 5 may read: species records (bond graph, formation enthalpy,
> dipole, polarizability, intermolecular params, phase at (T,P)), reaction
> events, surface state. Phase 5 may write: environmental boundary
> conditions (confinement, stress, ambient) back to cells — never species.

Materials are what species do when there are 10²³ of them under
conditions; if Phase 5 ever needs a property chemistry didn't compute,
that is a Phase 4 bug, not a Phase 5 table.

## Verification strategy

1. Oracle: ~50 real molecules (bond lengths, ΔHf, geometries) in
   `tests/oracle/`, band-checked nightly; aspirin/ammonia/etc. named only
   there — `sim/chemistry/` passes a grep gate for compound names.
2. Internal-consistency (no oracle possible): detailed balance holds in
   closed boxes across random conditions — this is the strongest
   correctness test we have for a world with uncountably many compounds.
3. Surprise ledger: every emergent result that differs from reality gets
   a dated line in `spec/surprises.md` with the measured gap — drift
   becomes visible instead of being patched with a table.

## Sequencing

```
Wk 1-2         Wk 2-3          Wk 3-4            Wk 4-5          Wk 5-7
─────          ──────          ─────────        ──────────      ──────────
W1 bonds    →  W2 geometry  →  W3 reactions  →   W4 thermo     W6 fuzz +
(H₂, N₂)       (water bends)   (carbon burns)    + pH/phase     discovery +
                                                  W5 organic    freeze gate
                                                  stress test   Phase 5
```

## Risks

| Risk | Mitigation |
|---|---|
| LCAO pair+angle model misses medium molecules (it will, ~kJ/mol error) | bands set to what **thermo** needs, not spectroscopy; surprises logged; per-family refinement ladder mirrors Phase 3's, fires on detected strain — never on a species list |
| Reaction-candidate combinatorics blow up for heavy species | search bounded by collision shell + valence budget; heavy-molecule channels memoize aggressively; fuzz includes a polymer melt cell |
| Evans–Polanyi misses barrierless/rearrangement classes | barrier floor at 0 allowed (no fake activation); pericyclic-analog class gets its own geometry-only channel rule with a test, not a list |
| Catalysts emerge too weak or too strong | surface term has one global coupling knob calibrated on **one** anchor (ammonia yield); everything else, including catalytic converters, is prediction |

**Gate:** Phase 5 starts when the organic stress test passes, detailed-
balance CI is green across fuzz conditions, the catenation test decides
the carbon/silicon question correctly, and both contract lines are frozen.
