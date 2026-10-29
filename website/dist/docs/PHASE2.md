# Phase 2 — Nuclear Layer

**Goal:** on top of the running quantum layer, produce nuclei: bound
nucleon states whose binding curve, stability islands, decay chains,
half-lives and radiation come out as **outputs** of the coupling rules —
no nuclide table anywhere in the runtime.

**Prerequisites (hard gate, from Phase 1):**

- Acceptance run green in CI (big bang → H/He/Li, replay bit-for-bit).
- Perf budgets measured-filled, held one week.
- The Phase 1 → Phase 2 interface line written in `spec/interfaces.md`
  (read: collapsed quanta, collapse events, jump-state composition;
  write: binding outcomes into the W2 coupling table).

**Definition of done:** given arbitrary `(T, ρ, composition)` conditions —
supplied as a jump-state summary or a probe cell — the engine fuses,
fissions, decays and radiates at rates that land in the theory band, the
binding-energy curve emerges with the iron-peak maximum and the helium-4
spike, decay chains terminate at stability, and the whole nuclear history
replays bit-for-bit. A nuclide nobody pre-declared appears in a test run
and the sim handles it as correctly as one we have seen in a book.

---

## Architecture

Extends `sim/`; the nuclear layer is a composite tier above quanta, not a
new world:

```
sim/
  nuclear/
    nucleon/     nucleon = bound 3-valence-quant state; p/n as species variants
    nucleus/     nucleus store: Z, N refs into nucleon blocks; excitation energy
    force/       effective residual-strong kernel (Yukawa-style, from D2 table)
    coulomb/     proton-proton barrier from Phase-1 EM coupling (no new constant)
    tunnel/      Gamow-window sampling via counter RNG (rare-event path)
    decay/       alpha / beta / gamma outcomes from stability gradients
    rad/         radiation bookkeeping: species, penetration, ionization deposit
    cache/       emergent nuclide registry (computed-once disk cache, see rules)
```

Data rules:

- A nucleus is an id + constituent lists + cached scalars (mass, binding,
  dominant decay mode). It is a row, not an object graph; constituents are
  indices into nucleon blocks.
- The **nuclide cache is a memoization, never a source of truth**: every
  cached value must be recomputable from the force kernel, and CI runs a
  cache-off replay to prove it. Deleting `cache/` must never change results.
- Fusion/fission/decay are **events**, not per-tick scans: nuclei tick
  cheaply (stability check only when composition or T changed); transitions
  are sampled from rate tables the tunnel/decay kernels compute on demand.
- Radiation is not a new substance — alphas are He nuclei, betas are
  electron quanta, gammas are photon quanta. Radiation damage = ionization
  energy deposited into cells, a field the biology phase can read later.

## Work packages

W1 and W2 parallel; W3 needs both; W4 parallel after W2; W5/W6 last.

### W1 — Nucleons and the effective force

- [ ] Nucleon as bound valence state from the D2 field table (no new fields).
- [ ] Residual-strong kernel: short-range attraction, hard core, saturation.
- [ ] Coulomb barrier wired to the existing EM coupling — check the proton
      charge Phase 1 emits is the one the barrier expects.
- [ ] **Test:** deuteron exists and is bound but loose; helium-4 is far more
      bound than its neighbours; nothing heavier than ~A=120 is stable
      against fission without neutron excess.

### W2 — Binding curve as output

- [ ] Scan Z, N up to ~110 on and off lattice; record mass-per-nucleon.
- [ ] **Test:** curve matches the real binding curve within band (oracle
      only), iron-peak maximum within ±2 elements of iron, He-4/Li-6 spikes
      present. Bands go in `tests/physics_bands.toml` next to Phase 1's.
- [ ] Publish `nuclear::binding(Z,N)` as Phase 3's workhorse call.

### W3 — Fusion

- [ ] Gamow-window rates: tunnel/ samples `σ(v)` from W1 kernels + counter RNG.
- [ ] Chain handling: pp → D → He-3 → He-4 with whatever intermediates exist.
- [ ] **Test:** at solar-core `(T, ρ)` the H→He rate and energy yield land
      in band; at ~10× T the triple-alpha path (or its emergent equivalent)
      makes carbon appear — and carbon appears **without** us naming the
      process.
- [ ] Jump-state fusion: a 1000× skip of a hot dense region produces the
      same final composition as ticking (extends Phase 1 W3 test to reacting
      matter).

### W4 — Fission, decay, half-lives

- [ ] Fission when Coulomb term overwhelms strong term; fragment split from
      both daughters' binding, neutrons ejected as free nucleons.
- [ ] Alpha: emit when it lowers total mass; beta: move toward the stability
      gradient; gamma: de-excitation of W2 excitation energy.
- [ ] Half-lives fall out of barrier-penetration rates — **measured, never
      assigned**.
- [ ] **Tests:** a uranium-ish emergent nuclide fissions with ~2–3 neutron
      excess (chain-reaction capable — note it, Phase 11 weapons); a
      C-14-analog beta half-life lands within 2 orders of magnitude (bands
      are loose here on purpose, first-pass kernel); decay chains from any
      heavy nuclide terminate at a stable one in every fuzz run.

### W5 — Radiation bookkeeping

- [ ] Per-species penetration/absorption in matter (alpha stops in air,
      gamma doesn't) derived from ionization cross-sections, not lists.
- [ ] Ionization deposit per cell: running field, cheap, read-only above.
- [ ] **Test:** a sealed hot source inside 10 cm of matter registers near
      zero outside; unsealed registers high. Radioactive decay products
      carry away correct energy (energy conservation audit per event).

### W6 — Acceptance harness + interface freeze

- [ ] Acceptance run: cool the Phase 1 demo output to nucleosynthesis, run
      a mini "star" cell (fixed T, ρ jump-state) for a simulated 10⁷ years,
      verify composition drift: H falls, He rises, traces of C/O appear,
      radionuclides decay on schedule, replay bit-for-bit.
- [ ] Fuzz: random `(Z, N, T, ρ)` for 10⁶ events — no panics, no
      non-terminating chains, energy conserved in every logged event.
- [ ] Freeze the Phase 2 → Phase 3 interface (below) and write the line.

## Performance budget (fill from W1–W3 measurements)

| Path                                   | Budget            | Measured |
|----------------------------------------|-------------------|----------|
| stability check / nucleus / tick       | < 20 ns           | ___      |
| fusion/decay event (rate + apply)      | < 2 µs            | ___      |
| binding(Z,N) cache hit                 | < 50 ns           | ___      |
| binding(Z,N) first compute             | < 1 ms            | ___      |
| cache-off replay slowdown              | < 5×              | ___      |
| 10⁷-yr stellar cell (jump path)        | < 1 s wall        | ___      |

## Interface exposed to Phase 3 (atomic)

> Phase 3 may read: nuclide records `(Z, N, mass, charge, half-life, decay
> modes, binding)` via `nuclear::nuclide(Z,N)` — computed or cache-served,
> never enumerated — plus radiation/ionization fields per cell.
> Phase 3 may write: nothing into nuclei (electron capture is the one
> exception: it asks Phase 2 to transmute, and Phase 2 decides).

This keeps the periodic-table-from-chemistry (Phase 3) honest: it can ask
"what is Z=6" but cannot know how many carbons exist.

## Verification strategy

1. Replay CI extended: nuclear acceptance run + fuzz in every merge.
2. Oracle discipline: the real nuclide table lives **only** in
   `tests/oracle/`, never linked into `sim/`; a CI grep enforces it.
3. Conservation audits: baryon number, charge, energy per event, logged and
   checked on 100% of events in debug builds.
4. Cache-off replay weekly, not per-merge (cheap insurance against the
   cache becoming load-bearing).

## Sequencing

```
Wk 1-2         Wk 2-3          Wk 3-4           Wk 4-5          Wk 5-6
─────          ──────          ─────────        ──────────      ──────────
W1 nucleons    W2 binding   →  W3 fusion    →   W5 radiation    W6 accept
W2 scan infra  curve+tests    W4 decay/fiss    + conservation   run+fuzz+CI
                                                    gates        gate Phase 3
```

## Risks

| Risk | Mitigation |
|---|---|
| Effective force gets He-4 right but misses medium nuclei | fit the kernel on 5 anchor nuclides only (oracle-legal: they calibrate constants, not runtime), check the other ~200 as pure prediction |
| Half-lives off by orders of magnitude (they always are, first pass) | loose bands + log the curve vs reality as a published artifact; Phase 9+ doesn't need C-14 precision, weapons logic needs U-235-ish fissionability, which is a binding-curve statement, not a half-life statement |
| Rare-event sampling starves or floods | rate tables computed once per (species, T) bucket, reused; bucket resolution is a knob with a convergence test |
| Cache silently becomes truth | cache-off replay + grep gate + "delete cache, same hashes" as an explicit acceptance test |

**Gate:** Phase 3 starts when the acceptance run and fuzz are in CI, the
binding curve is in band on the 200-nuclide prediction set, and the
`nuclear::nuclide(Z,N)` contract line is written.
