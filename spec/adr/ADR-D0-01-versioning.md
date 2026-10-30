# ADR-D0-01: Version and compatibility boundaries

**Status:** Accepted · **Date:** 2026-10-30 · **Ticket:** [D0-01](../../tasks/D0-01-baseline-freeze.md) · **Deciders:** Reference-model maintainer

## Context

`physics_build 0.1` is a manually maintained string. Historical documents treat
D1-D5 as closed while the audit (`ROADMAP_DIFF.md`) and code comments identify
weaker guarantees (RNG prefix reuse, absent reverse channels, quiet-jump
heuristic, incomplete causal fingerprint). The 0.1 artifacts lack a complete
execution identity, so changes could silently inherit an incompatible label.

## Decision

1. **Frozen baseline.** `physics_build 0.1` is frozen at commit
   `2a74160e5934fe76b8e14726d78ba6e2c3c7d40f` and fingerprinted in
   [`../baselines/physics-0.1.json`](../baselines/physics-0.1.json) (engine git
   trees for `sim/`, `tests/`, `spikes/`, environment, artifact hashes). Frozen
   means immutable: original audits, acceptance runs and this manifest are never
   overwritten or silently replaced.
2. **Independent identity dimensions.** A run is identified by five separate
   identities, each versioned independently: **model** (`physics_build`),
   **runtime/numerical environment**, **log schema**, **RNG scheme**, **state
   schema** — plus **source revision**. A single version string may never imply
   compatibility across a change it does not identify.
3. **Candidate states.** The next model identifier is the **0.2 candidate**.
   `candidate` → `accepted` requires the D0-12 release dossier. Behavior-changing
   edits to engine trees invalidate the baseline manifest's identity check and
   must produce new artifacts (new goldens, new fingerprints) under the new
   identity; metadata-only changes (docs, manifests, task records) do not.
4. **Legacy execution.** 0.1 execution history is preserved by its exact source
   revision (git checkout of the frozen commit), not by duplicate legacy kernels
   inside a newer engine. Replay of 0.1 records runs in that archived source
   environment; log content must never auto-fetch or execute historical code.
5. **Reproducibility classes are named separately:** record-and-verify (same
   build, same environment), fresh repeat (independent run, same environment),
   cross-build comparison (named observables under a preregistered equivalence
   budget — never automatic bit identity), checkpoint restoration (separate
   feature, later acceptance), independent replication (separate implementation).
   Every test and report names exactly one class.
6. **Test-scope policy.** Every existing test is classified in
   [`../test-scope.json`](../test-scope.json) as `shared_invariant`,
   `characterization_0_1`, or `model_validation` with a declared domain.
   Characterization and band suites run against the archived 0.1 source once the
   candidate changes behavior. No blanket xfail, no weakened assertions, and the
   new model is never tuned until old bands happen to pass. Candidate controls
   are added under new test names.

## Consequences

- `tests/test_baseline_manifest.py` fails if engine trees drift from the frozen
  baseline, forcing an explicit identity decision on every behavior change.
- D0-02 run manifests, D0-03 event registry and D0-05 state schema build on the
  identity dimensions defined here (S9, S23 partial-contract progress only).
- Old fitted bands, capture timings, jump counts and golden histories become
  0.1 characterization the moment their assumptions change; green candidate runs
  do not retroactively validate them.

## Trace

ROADMAP_DIFF.md (status ambiguity, recommended revisions); BUILD0.md (physics
build 0.1, milestones); DEVELOPMENT_SPEC.md §3.1, §5, §8 (ADR-D0-01 row);
spec/seams.md S9, S23.
