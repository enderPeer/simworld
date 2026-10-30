# D0-02 — Run manifests and compatibility preflight

**Owner role:** Reproducibility maintainer · **Depends on:** D0-01 (verified) · **Ticket:** [DEVELOPMENT_SPEC.md §D0-02](../DEVELOPMENT_SPEC.md) · **State:** verified (2026-10-30)

## What was built

- `spec/run-manifest.schema.json` — authoritative field list for `run-manifest/0.1`; separates semantic fields (`schema_version, physics_build, schemas, config, identity`) from informational ones (`created_utc, platform`).
- `sim/manifest.py` — builds the execution identity (constants digest of `sim/constants.py`, git source block, Python/NumPy/numeric policy), validates manifests against the schema document, computes the semantic digest, and runs `preflight()` comparing every replay-relevant dimension against the current build.
- `sim/log.py` — log schema 0.2: header optionally carries `log_schema` and `manifest_digest`; verify mode rejects mismatches. 0.1-legacy headers (toy/test logs) are untouched because both fields are optional parameters.
- `sim/demo.py` — `run_recorded` writes `manifest.json` before the tick loop and binds the log header to its semantic digest.
- `sim/replay.py` — reads and preflights the manifest before any world allocation; rejects legacy manifest-less runs with archived-source instructions (checkout `2a74160…` or the source zip on Python 3.11.9/NumPy 2.4.6); verifies the log↔manifest binding and that header meta matches the manifest configuration.
- `spec/baselines/candidate.json` — registers the candidate `sim/` tree per ADR-D0-01: metadata-only change, physics label stays 0.1, characterization suites still pass on the candidate.

## Acceptance

- [x] Manifest round trips preserve semantic fields; missing required fields, unsupported schemas and contradictory settings are rejected (validate/preflight tests).
- [x] Changed constants, runtime fingerprint or physics label under the old label fail preflight **before** the tick loop runs (tests patch `sim.replay.run` to explode if simulation starts).
- [x] Paths and timestamps never enter RNG coordinates or canonical state hashes: two runs in different directories at different times share `final_hash` and semantic digest; editing `informational` leaves the digest unchanged.
- [x] Legacy 0.1 input is rejected with archived-source reproduction instructions; no guessed migration.
- [x] `python -m pytest -q tests/test_run_manifest.py` — 13 passed; full suite 85 passed (no old test altered; characterization suite green on the metadata-only candidate).

## Evidence

- 2026-10-30: `python -m pytest -q -p no:cacheprovider` → **85 passed** (72 baseline + 13 candidate controls).
- 2026-10-30: smoke: `python -m sim.demo … --ticks 200` + `python -m sim.replay` → REPLAY PASS with manifest binding active.
- 2026-10-30: checker green; D0-02 flipped to `verified`; ready queue updated; `P00-D3` work package marked verified with evidence.

## Reviewer decision needed

- Confirm the log↔manifest binding design (digest in header) and that rejecting legacy runs at replay time (instead of embedding a 0.1 reader) matches intent.
