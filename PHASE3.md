# Phase 3 — Atomic Layer

**Goal:** put electrons on nuclei so that shells, the periodic table,
ionization energies, valences, spectra and plasma ionization fractions are
all **outputs of solving the electron problem** — the periodic table exists
only in `tests/oracle/`, never in `sim/`.

**Prerequisites (hard gate, from Phase 2):**

- Nuclear acceptance run + fuzz green in CI; binding curve in band on the
  prediction set.
- `nuclear::nuclide(Z,N)` contract line written and frozen.
- Phase 0 Spike B (hydrogen-like + corrections) numbers on disk; this phase
  decides how much further past Spike B the real solver must go.

**Definition of done:** for any `Z` the sim asks, including ones never seen
in a book, the engine returns a stable atom record: orbital energies,
radial density, ionization potential, electron affinity (or "unbound"),
valence count, and spectral lines — computed, cached, and recomputable
with the cache deleted. The periodic table falls out of an
ionization-energy-vs-Z plot with the right periods (2, 8, 8, 18…), noble
gas peaks and alkali troughs, and the hydrogen Balmer series plus the
sodium-analog bright line land in band. A hot dense region's ionization
fractions follow from the atoms themselves, not a look-up.

---

## Architecture

```
sim/
  atomic/
    solver/     radial self-consistent-field (SCF) eigenstate solver on a
                logarithmic grid — the one hard numerical object in the sim
    species/    atom record per (Z, ion_state): orbital energies, radial
                densities, occupancy; the emergent cache (Phase 2 rule)
    derive/     IP, affinity, radius, polarizability, valence — finite
                differences / integrals over solver output only
    spectra/    line list from orbital energy differences; oscillator
                strengths from density overlaps
    plasma/     Saha-style occupation balance from IP + (T, ρ) — derived,
                wired to jump-state thermal summaries
    table/      TESTS ONLY: oracle CSVs + the plotting script that makes
                the periodic table as a verification artifact
```

Data rules:

- The SCF solver is the only place many-electron physics is approximated.
  Everything above Phase 3 reads `species/` records; nobody re-derives
  electron structure downstream.
- Species records are cache rows keyed by `(physics_build, Z, ion_state)`,
  versioned like Phase 2's. Cache-off replay must reproduce hashes (weekly
  CI, same rule as nuclei).
- A species is computed lazily on first ask, but CI precomputes Z = 1–118
  all ion states nightly so no player-facing moment ever blocks on SCF —
  and so the oracle comparison runs on the full table.
- Unresolved cases are data, not crashes: if affinity is unbound (HF-level
  failure cases like some anions), the record says `affinity: unbound` and
  a correlation-correction ladder is attempted before falling back; the
  fallback choice is logged and counted (see Risks).

## Work packages

W1 is everything; W2–W4 hang off its output. W5 needs W2+W3.

### W1 — The solver

- [ ] Hydrogenic analytic start (exact) as grid initializer.
- [ ] Radial HF-SCF on logarithmic grid, spherical approximation, frozen
  nucleus (nuclear radius/mass from Phase 2 records).
- [ ] Correlation-correction ladder: HF → +local-density-style correlation
  term → +configuration mixing for the handful of near-degenerate
  light-atom ground states that need it (the ladder is generic — it fires
  on degeneracy detected in solver output, never on a species list).
- [ ] Convergence + basis-set-free error control: solution must be stable
  under grid refinement; refinement convergence test in CI.
- [ ] **Tests:** H 1s binding = 13.6 eV within band (analytic anchor);
  He, Li, C, Fe first IP within band; every level-2 ladder case converges
  within its declared tolerance or the run fails loudly.

### W2 — Shells, periodicity, valence (the table as output)

- [ ] Compute neutral + low-ion records for Z = 1–118.
- [ ] Derive: IP₁..ₙ, affinity, radius (density fallback percentile),
  polarizability, valence count from partially-filled outer shells.
- [ ] **Tests (the money shots):**
  - [ ] Period lengths from IP jumps: 2, 8, 8, 18, … within tolerance.
  - [ ] Li shows the huge IP₁→IP₂ gap (shell structure, unscripted).
  - [ ] Noble-gas local maxima at every period end; alkali minima after.
  - [ ] Carbon says 4 valence electrons, oxygen 2, sodium 1 — with no hint
        of those numbers in code.
  - [ ] The table **ends**: above some Z, neutral atoms stop being bound;
      record where it ends and whether it matches reality within band.

### W3 — Spectra

- [ ] Line list per species from orbital differences; intensity proxy from
  overlap integrals.
- [ ] **Tests:** H Balmer series wavelengths in band; the Na-analog
  strongest visible line lands in the visible (the physics behind sodium
  streetlamps, needed later for city lights in Phase 13); H-like Fe line in
  the X-ray band — needed later for radiation astronomy (Phase 7).
- [ ] Emit a `spectra::` read contract: Phase 6 light and Phase 7
  observation read line lists; nothing else.

### W4 — Plasma & ionization balance

- [ ] Saha-style equilibrium from IP + `(T, ρ)` from jump-state summaries;
  pressure ionization when neighbor distance < summed radii.
- [ ] **Tests:** solar-photosphere conditions → ~all H neutral, Na mostly
  ionized (that's the real-world check that made Saha useful); solar-core
  → fully ionized; a cool dense region → no plasma anywhere.
- [ ] Ionization must feed back: recombination emits the W3 line list
  (absorption/emission symmetry check per species).

### W5 — Acceptance harness + interface freeze

- [ ] Acceptance run: extend the Phase 2 stellar cell — cooled composition
  now captures electrons; verify the H/He/Li output is neutral atoms with
  matching line spectrum, replay bit-for-bit.
- [ ] Oracle CI job: ionization-energy-vs-Z plot diffed against
  `tests/oracle/`, band-pass; runs nightly on the 1–118 set.
- [ ] Fuzz: random `(Z, ion_state, T, ρ)` — no panics, no record where
  `charge ≠ Z − electrons`, energy audits on every recombination event.
- [ ] Freeze `atomic::species(Z, ion)` (below), write the line.

## Performance budget (fill from W1)

| Path                              | Budget            | Measured |
|-----------------------------------|-------------------|----------|
| SCF first solve (light atom)      | < 50 ms           | ___      |
| SCF first solve (Z ≈ 100)         | < 1 s             | ___      |
| species record read (cache hit)   | < 10 ns           | ___      |
| line-list lookup                  | < 50 ns           | ___      |
| ionization balance per cell tick  | < 1 µs            | ___      |
| nightly Z=1–118 sweep             | < 30 min          | ___      |
| cache-off replay slowdown         | < 3×              | ___      |

## Interface exposed to Phase 4 (chemistry)

> Phase 4 may read: `atomic::species(Z, ion)` — orbital energies, radial
> densities, occupancy, IP/affinity/valence/polarizability, radius, line
> lists — plus nuclei charge/radius from the Phase 2 contract.
> Phase 4 may write: nothing into atomic records; ionization changes go
> through the W4 balance (which consults Phase 2 for transmutation only).

Chemistry gets density clouds and energies, never a name for the element.
Any "what is carbon" question must be answerable only by asking Z=6.

## Verification strategy

1. Oracle discipline extends: real periodic table lives in `tests/oracle/`
   as data + the plotting script; a CI grep keeps `sim/atomic/` free of any
   element name above Z ≤ 1 (hydrogen is the analytic anchor and may be
   named; that is the whole exception).
2. Periodicity plot is a first-class test artifact, regenerated nightly —
   a regression in shell structure shows up as a wrong-looking table, not
   a passed numeric band.
3. Ladder-fallback counter: if a species needs the correlation ladder more
   than budgeted, fail the build — silent ladder sprawl is the slow way to
   re-introduce a table.
4. Replay CI unchanged: atomic acceptance in every merge, cache-off weekly.

## Sequencing

```
Wk 1-2            Wk 2-3          Wk 3-4           Wk 4-5         Wk 5-6
─────             ──────          ─────────        ──────────     ──────────
W1 solver core →  W2 periodicity  W3 spectra       W5 acceptance  interface
H-anchor tests    + valence tests W4 plasma        run + oracle   freeze +
                  (nightly sweep  + feedback       CI             budget CI
                   starts here)                                   gate Phase 4
```

## Risks

| Risk | Mitigation |
|---|---|
| HF misses electron affinities badly (it does, famously) | correlation ladder is mandatory before affinity is publishable; anions that still fail report `unbound` honestly and salt is... not possible — so ladder must clear halogens; that's an explicit W1 test |
| Spherical approximation breaks degenerate d/f shells (Cr, Cu anomalies) | degeneracy detector fires configuration mixing automatically; the anomaly test is "Cr and Cu configs come out weird like reality" |
| SCF cost × 118 × ion states too slow | nightly precompute + lazy path only for exotica; if sweep > budget, coarsen grid for high ion states and show the error stays below chemistry's tolerance |
| Grid artifacts fake shell gaps | refinement-convergence CI test on the exact Zs that define period boundaries (3, 10, 11, 18, 19, 36…) |

**Gate:** Phase 4 starts when the periodic table regenerates correctly from
solver output, the spectra and plasma tests are in CI, the ladder-fallback
counter is green, and the `atomic::species(Z, ion)` line is frozen.
