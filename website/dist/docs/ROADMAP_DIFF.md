# ROADMAP_DIFF

Roadmap versus implemented reality for SimWorld.

This document is the requested roadmap audit. It compares:

- the 17-phase research roadmap in `ROADMAP.md` and `PHASE0.md`–`PHASE16.md`;
- the frozen first-build contract in `BUILD0.md`;
- the seam ledger and frozen decisions in `spec/seams.md` and `spec/decisions.md`;
- the current Python micro-seed implementation in `sim/`;
- the current test status in `tests/`.

Date of audit: 29 October 2026.  
Physics build: `0.1`.  
Verification command used during this pass: `python -m pytest -q -p no:cacheprovider`.  
Result: `65 passed`.

## Executive verdict

`ROADMAP.md` is not a current status report. It is a long-range research and product thesis: an emergent, replayable, perception-centric world from Big Bang to playable civilization. The implemented repository is much smaller and more honest about its limits than the roadmap: a calibrated Python micro-seed with event logging and replay checks.

The core diff is:

- The roadmap promises a full 17-phase emergent simulation. The current build implements only a reduced Phase 0 micro-seed plus fragments of early physics mechanisms.
- `ROADMAP.md` claims “no seams,” but `spec/seams.md` is a cross-phase defect ledger recording `S1`–`S25`, with `22` seams marked `OPEN` and only `S14`, `S17`, and `S21` marked as wording or contract fixes.
- `ROADMAP.md` promises reproducibility from `seed + observation log`. Current replay is same-machine, same-build validation by re-running and comparing event/hash traces, not checkpoint restoration or cross-build bit-identity.
- `ROADMAP.md` says “Compute, don’t table.” The current model is useful precisely because it is an effective/calibrated model: fitted constants, oracle bands, imposed stability rules, effective fields, and aggregate ledgers.
- Late phases depend on mechanisms that are not merely incomplete but absent: chemistry, materials, planets, life, agents, machines, institutions, perception, nested simulation, compiled runtime, and global event ontology.

The roadmap should be read as a research program with an implemented micro-slice. It should not be used as a completion tracker unless a status layer is added.

## Roadmap principles versus current evidence

| Roadmap principle | Roadmap claim | Current evidence | Diff verdict |
|---|---|---|---|
| Compute, don’t table | Elements should be derived from electron physics, not looked up in a periodic table. `ROADMAP.md:10-12`. | Current atoms are an aggregate electron-capture ledger, not dynamical electron physics or a solved periodic table. `sim/atoms.py` describes itself as a charge ledger rather than dynamical transport. | Violated at the level of current code, but acceptable as an explicitly reduced micro-seed if labeled as calibration. |
| Emergence over scripting | Higher layers should emerge from lower layers. `ROADMAP.md:13-15`. | Current model uses calibrated anchors and acceptance bands; late phases are specified by detailed phase contracts rather than emergent discovery. Phase 7 already has decision `D6` for seeded disk composition. | The roadmap is still mostly a designed ladder. This is not fatal, but it must not be described as full emergence. |
| One coherent timeline, no resets, no seams | One world-state, no resets, no seams. `ROADMAP.md:16-17`. | `spec/seams.md:12-36` is an explicit seam ledger for cross-phase logic errors. It records `22 OPEN` seams. | Direct contradiction between roadmap wording and project reality. |
| Deterministic reproducibility | True quantum randomness is allowed, but the world must be reproducible from its seed and observation log. `ROADMAP.md:21-23`, `ROADMAP.md:53`. | `BUILD0.md:37` says replay determinism is guaranteed `same-machine, same-build`. `docs/architecture.md:9` says the log is an experiment record, not a complete resumable checkpoint or cryptographic chain. | Overstated as stated in the roadmap. Current behavior supports environment-scoped replay only. |
| Perception-centric existence | Observation/collapse is hooked into perception and field of view becomes the center of existence. `ROADMAP.md:52`, `ROADMAP.md:191`. | Current probe/observation bubble is an external stand-in. Seam `S21` records that the observation map was an external input and that mechanics land only in Phase 14 `W1/W5`. | Not implemented. Late-phase promise only has a fixed wording/contract, not working perception. |
| Whole world reproducible later | Whole world reproducible from seed plus observation log. `ROADMAP.md:206`. | `S22`, `S23`, and `S24` are open seams around frame budgets, compiled-runtime bit identity, and slow-layer jump certificates. | The full-world reproducibility promise is currently aspirational and contractally unresolved. |

## Phase-ladder diff

| Phase | Roadmap promise | Implemented/spec evidence | Audit verdict |
|---|---|---|---|
| Phase 0 | Big bang, expansion, cooling, quanta, fields, nucleosynthesis, replay from seed and log. `ROADMAP.md:27-45`. | `spec/decisions.md:1` says `D1-D5` are closed at `physics_build 0.1`; `BUILD0.md:17` freezes spec/interfaces; `BUILD0.md:248` marks M0 replay spine done; `docs/research-status.md:19` reports `65 passed`; `docs/research-status.md:21` reports `34` replay hashes matched. | Partially done as a micro-seed. Not done as the full ROADMAP Phase 0. Roadmap checkboxes remain unchecked and `ROADMAP.md:221-229` still contains unresolved open questions. |
| Phase 1 | Quanta, fields, entanglement, perception hook, production replay CI, large performance targets. `PHASE1.md` prerequisites and gates. | Current build has sampled quant rows, effective fields, collapse, probe stand-in, jump-state, log/replay. It does not have full entanglement, the performance architecture, or real perception integration. Seam `S21` records the probe bubble problem. | Partial micro-slice. Should be marked “early mechanisms present,” not “Phase 1 complete.” |
| Phase 2 | Nuclear physics, nuclides, stellar nucleosynthesis, decays, cache-off replay, emergence of isotope identity. | Current model has effective weak conversion, nucleon formation, bounded nuclear network, liquid-drop binding, and BBN-like outputs. `docs/research-status.md:7` explicitly calls it calibrated, not first-principles. | Partial effective nucleosynthesis. Full Phase 2 is not implemented. |
| Phase 3 | Atoms, spectra, periodic table as output. | Current atoms are aggregate electron capture, not solved atomic structure or dynamical spectra. | Not implemented as the roadmap means it. |
| Phase 4 | Chemistry, molecules, materials from interaction rules. | No chemistry layer is implemented. `spec/seams.md:21-23` says Phase 4 mechanisms are missing templated channels, self-assembly kinetics, and photochemistry classes. | Not implemented. |
| Phase 5 | Materials with internal structure and history. | No materials layer is implemented. | Not implemented. |
| Phase 6 | Continuum physics, fluids, solids, gravity, EM. | No continuum/solid/gravity/EM layer is implemented. `spec/seams.md:26` shows Phase 6 EM magnetostatics is a future seam for Phase 10. | Not implemented. |
| Phase 7 | Planet, climate, cycles, geochemistry, stellar context. | Depends on `S1`–`S9` and `S12`, all open or unresolved in prior audit; `ROADMAP.md:221-229` open questions remain. | Not implemented. Hard-blocked by upstream seams and unresolved composition/source questions. |
| Phase 8 | Life, heredity, compartments, ecology. | Depends on `S10` templated polymerization, `S11` vesicle self-assembly kinetics, and `S12` photochemistry. `spec/seams.md:21-23`. | Not implemented. Cannot be credibly attempted before upstream channel mechanisms land. |
| Phase 9 | Animals, individuals, rigid bodies, cognition, tools. | Depends on `S13` articulated multi-body dynamics, absent from current mechanics. `PHASE9.md:21-29`, `spec/seams.md:24`. | Not implemented. |
| Phase 10 | Civilization, cities, machines, circuits, science, nested simulation. | Depends on `S15` EM circuit/radio regimes and `S16` nested-simulation determinism. `PHASE10.md:18-28`, `spec/seams.md:26-27`. | Not implemented. |
| Phase 11 | Society, norms, institutions. | `S17` is a wording/contract fix: norms must enter agents as environment, not policy edits. `spec/seams.md:28`. The actual society layer is absent. | Contract fixed, implementation absent. |
| Phase 12 | Economics, ownership, money, institutions. | `S18` ownership is still open: owning is not an engine relation in earlier phases. `PHASE12.md:24-33`, `spec/seams.md:29`. | Not implemented. |
| Phase 13 | Infrastructure, externality, liability, climate damage. | Depends on `S19` producer attribution and `S20` street-scale concentration channels. `PHASE13.md:32-40`, `spec/seams.md:30-31`. | Not implemented. |
| Phase 14 | Perception, memory, existence, LOD. | `S21` is fixed only as wording/equivalence contract; mechanics land in Phase 14. `S22` frame-budget determinism remains open. `PHASE14.md:35-42`, `spec/seams.md:32-33`. | Not implemented. |
| Phase 15 | Hyperoptimized compiled runtime. | Depends on `S23` runtime build fingerprint and `S24` cross-layer jump certificates. `PHASE15.md:34-51`, `spec/seams.md:34-35`. | Not implemented. |
| Phase 16 | Full playable emergent world and definition-of-done. | Depends on all earlier phases plus `S25` machine-readable cross-phase event ontology. `PHASE16.md:40-46`, `spec/seams.md:36`. | Not implemented. |

## Seam ledger: the strongest roadmap contradiction

The roadmap’s “no seams” principle is contradicted by the project’s own defect ledger.

Current seam ledger status from `spec/seams.md:12-36`:

- Total seams recorded: `25`.
- Open seams: `22`.
- Fixed wording/contract seams: `S14`, `S17`, `S21` only.
- Important open seam clusters:
  - Phase 7 and upstream physics/cosmology: `S1`–`S9`.
  - Phase 8 biology prerequisites: `S10` templated polymerization, `S11` vesicle self-assembly, `S12` photochemistry.
  - Phase 9 agent/rigid-body prerequisites: `S13`.
  - Phase 10 machines/circuits/nested-sim prerequisites: `S15`, `S16`.
  - Phase 12 ownership: `S18`.
  - Phase 13 liability/attribution and local exposure: `S19`, `S20`.
  - Phase 14 perception/frame-budget determinism: `S22`.
  - Phase 15 compiled runtime and slow-layer certificates: `S23`, `S24`.
  - Phase 16 global event ontology: `S25`.

The fixed seams are not equivalent to implemented mechanisms:

- `S14`: fixed the wording that implied a second timeline. `spec/seams.md:25`.
- `S17`: fixed the wording that would have allowed policy edits by norms. `spec/seams.md:28`.
- `S21`: fixed the observation-map contract but explicitly says mechanics land later in Phase 14. `spec/seams.md:32`.

So the roadmap should say: the project has discovered seams, logged them, and uses them as upstream gates. Saying “no seams” is only true as an aspiration, not as a description of the project’s current planning state.

## Replay and reproducibility diff

The roadmap’s reproducibility language is the second-largest contradiction.

Roadmap and phase language:

- `ROADMAP.md:21-23` reproducibility promise.
- `ROADMAP.md:53`: seeded RNG plus observation log for reproducibility.
- `ROADMAP.md:206`: whole world reproducible from seed and observation log.
- `PHASE1.md:5-6`: Phase 1 promises bit-for-bit replay from seed plus observation log.

Current implemented reality:

- `BUILD0.md:7` says the micro-seed replays bit-for-bit from seed plus observation log.
- `BUILD0.md:37` narrows determinism to `same-machine, same-build`.
- `docs/architecture.md:9` says the log is an experiment record, not a complete resumable checkpoint or cryptographically linked chain of every state.
- `CONTRIBUTING.md:20` says exact replay is an environment-scoped guarantee unless cross-environment tests establish more.
- `spec/seams.md:34` says bit-identity had no compiler/build fingerprint contract and calls for `S23` at Phase 15.

Audit verdict:

- Current replay is valuable but should be described as “same-build regression replay,” not “universal world reproducibility.”
- The phrase “observation log” currently means experiment/event log, not a full save/load spine or resumable checkpoint system.
- Cross-build, cross-platform, GPU, compiler, and runtime-fingerprint claims should remain blocked until `S23` is merged.
- Frame-budget allocation determinism should remain blocked until `S22` is merged.

## Implementation semantics versus roadmap semantics

The current implementation is a useful scientific toy, but its vocabulary must not be mistaken for the full research target.

| Current concept | What it is now | What it does not mean |
|---|---|---|
| Fields | Five effective fields in a table, `sim/fields.py`. | Not the Standard Model field substrate. |
| Quanta / superposed / collapsed | Storage states plus threshold/probe collapse mechanics. | Not a full many-body quantum wavefunction or quantum field solver. |
| Weak layer | Effective `u`/`d` conversion and freeze-out, `sim/weak.py`. | Not full weak-interaction theory. |
| Nuclear layer | Bounded reaction network plus fitted binding and imposed baryon/stability rules. | Not full nuclear physics or stellar nucleosynthesis. |
| Atoms | Aggregate electron-capture ledger. | Not solved atomic structure, spectra, chemistry, or photon/electron transport. |
| Probe | External observer bubble used by collapse mechanics. | Not Phase 14 perception or agent existence. |
| Hash chain / replay | Event/hash comparison after re-run. | Not cryptographic ledger semantics, checkpoint restoration, or complete state-chain verification. |

`docs/architecture.md:3` and `docs/research-status.md:7` already make this distinction. The roadmap itself is less careful, so `ROADMAP_DIFF.md` should be treated as the authoritative warning label.

## Status ambiguity

There are currently three incompatible notions of “Phase 0 done”:

1. `ROADMAP.md:27-45` leaves Phase 0 unchecked.
2. `ROADMAP.md:221-229` still labels important questions open, including observation/decoherence and seed-versus-emerge composition issues.
3. `spec/decisions.md:1` and `BUILD0.md:17` treat `D1-D5` as closed and `physics_build 0.1` as frozen.
4. `docs/research-status.md:9-21` explicitly separates the micro-seed from full roadmap phases.

This is not a fatal problem, but it is a documentation hazard. A reader can reasonably conclude either:

- the project has nothing implemented; or
- the project has completed a lot because many docs exist and specs are frozen.

Both are wrong.

The accurate status is:

> Phase 0 exists as an accepted BUILD0 micro-seed slice at `physics_build 0.1`, with replay/log/nuclear/atomic reduced mechanics. The ROADMAP Phase 0 and all later phases are not complete. The late phase documents are design contracts, not implemented systems.

## Highest-risk roadmap choices

1. Saying “no seams” while maintaining a seam backlog.
   - Risk: the roadmap sounds more certain than the system is.
   - Fix: state that seams are expected and that a phase cannot pass until its listed upstream seams merge.

2. Using phase documents as pseudo-progress.
   - Risk: detailed `PHASE*.md` files can look like implementation reports.
   - Fix: add explicit status headers: `NOT IMPLEMENTED`, `CONTRACT FROZEN`, `MICROSLICE PRESENT`, `UPSTREAM BLOCKED`.

3. Treating replay as a solved foundation.
   - Risk: later phases inherit unresolved cross-build and determinism assumptions.
   - Fix: separate `same-build regression replay`, `same-machine reproducibility`, and `cross-build equivalence`.

4. Treating effective calibration as failed emergence.
   - Risk: either overclaims “computed from first principles” or condemns every useful reduced model.
   - Fix: define an explicit calibration ladder: anchor, reduced model, held-out validation, emergent derivation.

5. Leaving open questions in the roadmap after `D1-D5` closure.
   - Risk: readers do not know whether questions are genuinely open or only ROADMAP prose is stale.
   - Fix: move resolved questions into `spec/decisions.md`, keep unresolved questions in a visible blocker list.

6. Building late phases before upstream seams.
   - Risk: Phase 8 life without templating/photochemistry/self-assembly, Phase 10 circuits/nesting without EM/nested contracts, Phase 13 liability without producer attribution, Phase 16 without global ontology.
   - Fix: make `spec/seams.md` a hard gate table, not a reference note.

7. Mixing product ambition and research ambition.
   - Risk: playable world expectations distort physics claims.
   - Fix: maintain separate tracks:
     - micro-seed physics paper;
     - replay/determinism infrastructure;
     - emergent phase ladder;
     - playable-world product demo.

## Recommended roadmap revisions

1. Add a status legend to `ROADMAP.md`.
   - Suggested labels: `NOT IMPLEMENTED`, `MICROSLICE`, `CONTRACT FROZEN`, `UPSTREAM BLOCKED`, `ACCEPTED`.

2. Add a Phase 0 status note.
   - Suggested wording:
     - “Phase 0 is accepted as `BUILD0` micro-seed `physics_build 0.1`. ROADMAP Phase 0 open questions and full roadmap acceptance remain unresolved.”

3. Replace “no seams” with a seam policy.
   - Suggested wording:
     - “History should have no runtime seams. Planning seams are allowed only if they are recorded in `spec/seams.md`, owned upstream, and closed before dependent phases merge.”

4. Promote `spec/seams.md` to a release gate.
   - Every phase should list required seam IDs and status in its own gate.
   - A phase cannot be called ready when an upstream `OPEN` seam blocks its core mechanism.

5. Split `ROADMAP.md` into three layers.
   - Vision/principles.
   - Current implementation status.
   - Future phase contracts.

6. Create a machine-readable status file.
   - Example: `spec/status.json` with phase, status, blockers, tests, evidence path, last verified date.

7. Add explicit reproducibility labels.
   - Use:
     - `same-build regression replay`
     - `same-machine reproducibility`
     - `cross-build equivalence`
     - `checkpoint restoration`
   - Do not call any of them “world reproducibility” until separately proven.

8. Reframe “Compute, don’t table” as a direction, not a current fact.
   - Suggested wording:
     - “The long-term goal is derived computation. Current accepted work may use calibrated effective models when they are labeled as anchors and tested against held-out targets.”

9. Mark late phases as contracts only.
   - `PHASE7.md` through `PHASE16.md` are design specs until their first upstream seam and first executable gate exist.

10. Prioritize upstream seams over new phase docs.
   - Before Phase 7: resolve `S1`–`S9`.
   - Before Phase 8: land `S10`–`S12` upstream.
   - Before Phase 9: land `S13`.
   - Before Phase 10: land `S15` and `S16`.
   - Before Phase 13: land `S19` and `S20`.
   - Before Phase 14: define `S22`.
   - Before Phase 15: land `S23` and `S24`.
   - Before Phase 16: land `S25`.

## Evidence baseline

The audit was based on the following concrete evidence:

- `ROADMAP.md:10-23` roadmap principles.
- `ROADMAP.md:27-45` Phase 0 progress markers.
- `ROADMAP.md:52-53` observation/reproducibility promises.
- `ROADMAP.md:206` full-world reproducibility promise.
- `ROADMAP.md:221-229` unresolved open questions.
- `BUILD0.md:7` and `BUILD0.md:17`: micro-seed replay promise and frozen spec/interfaces.
- `BUILD0.md:37`: replay determinism is same-machine, same-build.
- `BUILD0.md:248`: M0 replay spine done.
- `BUILD0.md:273`: full suite green at freeze with `65 passed`.
- `docs/research-status.md:3`, `:7`, `:9`, `:19`, `:21`: dated status, calibrated model warning, 17 phases, `65 passed`, `34` replay hashes.
- `docs/architecture.md:3`: current engine is reduced stochastic micro-seed.
- `docs/architecture.md:9`: log is experiment record, not complete checkpoint or cryptographic chain.
- `CONTRIBUTING.md:20`: exact replay is environment-scoped unless more is proven.
- `spec/decisions.md:1`: `D1-D5` closed at `physics_build 0.1`.
- `spec/seams.md:12-36`: seam ledger statuses.
- `spec/seams.md:16-36`: open seam examples and late-phase contracts.
- `PHASE1.md:5-6`: Phase 1 bit-for-bit replay promise.
- `PHASE7.md:12`, `PHASE8.md:15`, `PHASE9.md:21`, `PHASE10.md:18`, `PHASE11.md:19`, `PHASE12.md:24`, `PHASE13.md:28`, `PHASE14.md:29`, `PHASE15.md:34`, `PHASE16.md:35`: prerequisite hard gates.
- `tests/` full suite result: `65 passed` on this pass.

## Bottom line

The roadmap is ambitious and largely coherent as a research thesis. The implementation is not yet a roadmap-compliant world; it is a reduced micro-seed with a solid replay/log foundation. The most useful correction is not to rewrite the vision, but to make the gap explicit:

> Current reality: one calibrated Python micro-seed at `physics_build 0.1`, with `65` tests passing and same-build replay validation.  
> Roadmap target: a 17-phase emergent, perception-centric, replayable world.  
> Present bridge: `spec/seams.md` records `22` open upstream defects that must become hard gates before later phases can be credibly attempted.
