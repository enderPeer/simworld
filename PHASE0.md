# Phase 0 — World Rules

**Goal:** produce the binding first-principles specification that every other
phase emerges from, and prove the core representation is computationally
survivable with a runnable micro-seed demo.

**Definition of done:** a hot dense seed expands, cools, quanta bind into
nuclei, nuclei capture electrons into atoms, and roughly the right H/He/Li
ratios come out — from the rules alone, no element tables, no scripted
nucleosynthesis. Plus: replay from `seed + observation log` reproduces
run 1 bit-for-bit.

**Deliverables:**

1. `spec/decisions.md` — five decisions D1–D5, each with rationale and
   rejected alternatives.
2. `spec/constants.md` — the irreducible constants table + validation targets.
3. Three throwaway spikes (`spikes/`) proving cost and correctness.
4. `sim/` — the micro-seed demo (keeps growing into Phase 1+).

---

## The five decisions (task list)

Work these in order. Each task has an acceptance test — the decision is only
made when the test passes.

### D1 — What is a quant?

Decide the primitive unit of existence.

**Recommended position:** continuous fields, sampled on demand (sparse).
A quant is a discrete excitation packet of one field.

Proposed record (data-oriented, fits in ~48–64 bytes for the common case):

```
species      : field id (u8)      -- which field is excited
energy       : f32 (log-encoded)  -- headroom without f64
momentum     : 3x f16 packed      -- coarse until observed
charge/spin  : packed bits
phase        : f16                -- for interference while unobserved
state        : enum { superposed, entangled, collapsed }
born         : u64 tick           -- timeline anchor
entangles    : smallvec<QuantId>  -- nonlocal correlation edges
pos          : coarse cell + refinement tier (tier = observation depth)
```

Superposed quanta carry probability + phase only — no exact position until
collapse. Collapsed quanta get real coordinates and refinement tiers.

**Acceptance test:** the record round-trips to disk and a billion of them
fit in RAM budget (see Spike A numbers).

- [ ] Write the quant record spec + invariants (what must never be true).
- [ ] Confirm the entanglement edge representation stays cheap (< 2 hops avg).

### D2 — What is the field substrate?

Decide which fields exist at the start and how particles emerge.

**Recommended position:** an *effective* field set, not the full Standard
Model. Start with ~8–12 fields (a small gauge set + a couple of scalar
fields) whose symmetry breaking yields: electron-ish, quark-ish, photon-ish,
gluon-ish, graviton-ish-as-effective. Coupling strengths are the tuning
knobs, calibrated so nucleosynthesis lands near reality.

Rationale: the real Standard Model has ~20 free parameters and costs
precision we don't need; what matters is that the *emergent* periodic table
and binding curves come out right, not that the substrate is publishable
particle physics.

**Acceptance test:** from the field set + couplings alone, a 1D toy run
produces at least two stable "nucleon" bound species and one massless
carrier species.

- [ ] Choose field list + symmetry rules (one page).
- [ ] List which real phenomena each field must reproduce downstream.
- [ ] Document the cheat: where effective-theory shortcuts replace exact
      QCD/QED, and prove the shortcut's error is below the next layer's
      tolerance (chemistry cares about eV, nuclei about MeV).

### D3 — What was in the Big Bang?

Decide the seed format and initial condition.

**Recommended position:** the seed is
`(u64 prng_seed, constants_version, T0, expansion_rate)`. The initial state
is **not** a particle list — it is a coarse distribution (temperature and
expansion rate over a small lattice) held in superposed form. Particles
condense out as it cools. Nothing is materialized until observed or until
it collapses by decoherence (D4).

**Acceptance test:** two runs from the same seed diverge only at points a
logged observation explains (Spike C harness proves it).

- [ ] Define constants versioning (changing a constant = a new universe
      "physics build", old saves must replay).
- [ ] Define the condensation rule: distribution + cooling → quanta appear.

### D4 — What is observation?

Decide what collapses a superposed quant into classical fact.

**Recommended position:** collapse on **decoherence threshold**, not on
conscious observers. Criterion: a superposed quant collapses when its
interaction count with already-collapsed quanta within its cell exceeds a
threshold θ during one tick, or when an agent's perception region (Phase 14
contract) includes its cell. Entangled partners collapse together.

This keeps "agent perception is special" for later (it controls *rendering
detail*, not *existence*) while giving the quantum layer a mechanical,
testable collapse rule today.

**Acceptance test:** with θ set so ~99% of an unobserved volume stays
superposed, the volume still behaves correctly when a probe interaction
enters it (Spike B micro-cosmology).

- [ ] Write the collapse rule as pseudocode; find its failure cases
      (freezing watched-pot edge cases, entanglement chains).
- [ ] Define the **observation log** entry: `(tick, quant batch, collapsed
      state, cause)` — append-only, compressed; this plus the seed is the
      whole save format eventually.
- [ ] Set θ default + sensitivity analysis (how wrong does the world get
      per % of θ error).

### D5 — What is change/time?

Decide the tick model.

**Recommended position:** discrete ticks at the quantum layer; higher layers
get emergent continuous time through tick-rate tiers. A cell's tick rate =
its observation tier: observed cells tick every tick; near-observed tick
every N; distant regions don't tick at all — they **jump-state** via
analytical/probability propagation (closed-form cooling, decay chains,
orbital decay summaries). Jump-state results are still probabilistic; when
a region gets observed, it collapses from its own distribution, and the log
records the jump so replay is exact.

**Acceptance test:** a 1000x time-skip over an unobserved region costs O(1)
per cell and replays identically when re-observed from the log.

- [ ] Define tick tiers and the promotion/demotion rule (what makes a cell
      change tier; must be hysteresis-free or cheaply reversible).
- [ ] Define the jump-state API: what summaries a region must carry to be
      resumable (T, composition distribution, free energy, entropy debt).
- [ ] Nail the power/thermodynamics framing: power = travel per tick; this
      is where time↔velocity↔power gets its one-line equation, then stop —
      Phase 6 does the rest.

---

## How to implement (sequencing)

```
Week 0        Week 1          Week 2-3         Week 3-4        Week 5-6
─────         ──────          ─────────        ──────────      ──────────
D1,D2 docs → Spike A      →  D3,D4 rules   →  micro-seed     →  D5 jump-
D3 seed      (quant cost,     + Spike C         demo              state +
format       GPU/CPU)         replay test       (big bang →       acceptance
                                                H/He/Li)          run
```

**Spikes (throwaway, Python/NumPy first — port nothing yet):**

- **Spike A — quant cost.** 1M superposed quanta, 10k collapsed, random
  interactions. Measure ns/quant/tick on CPU vs GPU. Budget target: the
  quantum layer must sustain ≥ 10⁷ quanta/s; if not, thicken the superposed
  encoding (pack more quanta per cache line) before deciding D1's record
  layout is final.
- **Spike B — electron shells.** Hydrogen-like orbitals + fitted
  many-electron corrections (not full Hartree-Fock). Validate emergent
  ionization energies against the *real* table — the table is allowed only
  as a test oracle, never as a runtime lookup. This is the cheapest proof
  that "compute, don't table" is feasible and it de-risks Phase 3.
- **Spike C — replay harness.** Tiny universe, seed + observation log →
  deterministic replay, bit-for-bit. Everything downstream depends on this;
  build the harness once, use it in every later phase's CI.

**Implementation notes:**

- Language: prototype in Python/NumPy, engine in Rust or C++ with
  data-oriented ECS; GPU via wgpu/compute shaders. No OOP-per-particle —
  quanta are struct-of-arrays rows, never objects.
- Store quanta in SoA blocks per cell per tick-tier; collapse is a tier
  promotion, not an allocation.
- The observation log is the spine of the save system from day one — do not
  let any spike mutate world state without writing log entries.
- Keep a `physics-build` version on every constant table; replaying old
  universes with new constants is a bug, not a feature.
- One coupling contract file (`spec/interfaces.md`): the *only* data each
  phase may read from the layer below (e.g. Phase 3 reads quant records +
  collapse stats, nothing else). Write each interface line when the phase
  beneath it is done.

**Folder layout to create now:**

```
simworld/
  ROADMAP.md
  PHASE0.md          ← this file
  spec/
    decisions.md     ← D1–D5 with rationale (fill in as decided)
    constants.md     ← constants + physics-build versions
    interfaces.md    ← coupling contracts
  spikes/
    a_quant_cost/
    b_shells/
    c_replay/
  sim/               ← micro-seed demo, becomes the real engine
```

## Risks

| Risk | Mitigation |
|---|---|
| Quantum layer too expensive even superposed | θ + tiers already bought; worst case: quantum detail exists only inside the observed bubble, everything else is jump-state chemistry — spec it as an honest degradation |
| Emergent elements drift from real physics | Spike B oracle harness; constants are tunable within a published physics-build |
| Observation rule too dumb (pot-watch freezes, entanglement chains) | D4 pseudocode failure-case hunt before any engine code |
| Phase 0 becomes an infinity of philosophy | Every decision has an acceptance test; no decision closes without a running check |

## Carry-over open questions (from ROADMAP)

- [ ] Discrete lattice vs sampled continuous — Spike A gives numbers; D1 closes it.
- [ ] Cheat-vs-exact threshold for electron shells — Spike B gives the error curve; feeds D2.
- [ ] Evolve life vs seed it (fast-forward offline evolution) — Phase 8's problem; record the Phase 0 constraint now: whatever we seed must be expressible as a jump-state + log entry, or it breaks the coherent timeline.
