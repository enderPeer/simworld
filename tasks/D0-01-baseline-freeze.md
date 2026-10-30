# D0-01 — Freeze the historical baseline and define change control

**Owner role:** Reference-model maintainer · **Depends on:** none · **Ticket:** [DEVELOPMENT_SPEC.md §D0-01](../DEVELOPMENT_SPEC.md) · **State:** verified (backlog state flipped 2026-10-30; unlocks D0-02/03/06)

Freeze the accepted `physics_build 0.1` micro-slice with an exact, machine-checkable
execution identity and a version/test-scope policy, without touching simulation
behavior. No opportunistic physics repairs.

## Deliverables

| File | Purpose | Done |
| --- | --- | --- |
| `spec/adr/ADR-D0-01-versioning.md` | Version and compatibility boundary policy | [x] |
| `spec/baselines/physics-0.1.json` | Baseline manifest: source trees, environment, schemas, artifact hashes | [x] |
| `spec/test-scope.json` | Classification of all 65 existing tests + execution contexts | [x] |
| `tests/test_baseline_manifest.py` | Deterministic manifest checks incl. negative tamper cases | [x] |

## Key facts established

- Baseline commit `2a74160e5934fe76b8e14726d78ba6e2c3c7d40f` (2026-10-29).
- `sim/`, `tests/`, `spikes/` git trees are identical between the baseline commit
  and current HEAD: the engine in the working tree *is* the 0.1 source.
- Local verification environment: Python 3.11.9, NumPy 2.4.6, Windows-10;
  `python -m pytest -q -p no:cacheprovider` → 65 passed.
- Public 0.1 evidence (verified run, audit diagnostics, test report, source zip)
  is tracked under `website/dist/downloads/`; hashes recorded in the manifest.

## Acceptance checklist (from ticket)

- [x] Manifest resolves to exact source and preserved 0.1 fingerprints; hashes validate without rerunning the universe.
- [x] Current-status record distinguishes accepted micro-slice, known defects, proposed contracts, unvalidated changes (existing `spec/status.json`; referenced, not overwritten).
- [x] Version policy names model, runtime, log, RNG and state schemas; behavior changes require new artifacts.
- [x] No original audit or acceptance files overwritten.
- [x] Every existing test classified shared-invariant / 0.1-characterization / domain model-validation, with execution contexts documented.
- [x] `python -m pytest -q tests/test_baseline_manifest.py` passes.

## Evidence

- 2026-10-30: `python -m pytest -q tests/test_baseline_manifest.py` → **7 passed** (identity fields, artifact hashes, frozen engine-tree check, 4 negative tamper cases, defect→ticket/evidence trace, scope-vs-collection, status agreement).
- 2026-10-30: full suite `python -m pytest -q -p no:cacheprovider` → **72 passed** (65 baseline + 7 new; no old test altered).
- 2026-10-30: `python scripts/check_development_spec.py` → OK, 17 phases / 12 tickets / 112 work packages / 25 seams.
- Scope classification: 27 shared_invariant, 34 characterization_0_1, 4 model_validation = 65.
- Behavior change: none. Engine trees (`sim/` etc.) untouched and verified against the frozen baseline commit.

- 2026-10-30: registry updated — D0-01 `state: verified` with evidence paths in `spec/development_backlog.json`; `ready_now` now D0-02 / D0-03 / D0-06 in both backlog and `spec/status.json`; phase 0 evidence records the baseline manifest. Checker green after sync.

## Reviewer decision needed

- Accept classification (esp. probe-equivalence as characterization, `test_jumps_happened` demoted from band). Objections mean editing `spec/test-scope.json` — the manifest and checker do not depend on the split beyond coverage.
