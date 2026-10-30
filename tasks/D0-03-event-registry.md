# D0-03 — Event registry and stable event identities

**Owner role:** Event-contract maintainer · **Depends on:** D0-01 (verified) · **Ticket:** [DEVELOPMENT_SPEC.md §D0-03](../DEVELOPMENT_SPEC.md) · **State:** verified (2026-10-30)

## What was built

- `spec/ontology.json` — versioned registry (`event-ontology/0.1`) of the nine events actually implemented in build 0.1: five draw kinds (`condense`, `react` via four declared lanes weak/bind/network/atoms, `decay`, `annih`) and two log-only kinds (`collapse`, `jump`). Each carries a stable semantic ID, canonical-identity stable hash, schema version, required q/payload fields, producer ownership (`sim/<module>.py:<function>`, checked importable) and role.
- `sim/ontology.py` — loader/validator: duplicate IDs, conflicting name/schema in semantic IDs, unknown roles, unregistered or non-callable producers, missing required fields, kind-id/role conflicts with the engine tables, fabricated kinds and legacy-reserved kinds all fail validation. `identity_map()` is order-independent; `classify_entry_kind()` separates the legacy truncated-hash encoding from registry identity.
- Registry binding: `schemas.events = "0.1"` was already a manifest dimension since D0-02 — preflight now pins registry version at replay (test controls the tamper path).
- `spec/seams.md` S25 row annotated as partial foundation (still OPEN; the S25 closure work package remains P16-W1, planned).

## Acceptance

- [x] Duplicate IDs, conflicting names/schema versions, unregistered producers and missing required fields fail validation (7 negative tests).
- [x] Same semantic event ID survives cache regeneration (`importlib.reload`) and deterministic channel re-enumeration (shuffled events + renumbered sub-lanes: identical `identity_map`, validation still clean).
- [x] Legacy encoding identified separately: `collide` (kind 1, no producer) lives only in `legacy_0_1.reserved_kind_ids_without_producer`; registry declares `registry_identity_present_in_serialized_logs: false`; a recorded 0.2 run's entries classify as `legacy_truncated_hash`, never as stable hashes. No claim that old logs use the new registry.
- [x] Registry contains only implemented kinds (engine cross-check both directions); extension section reserves `next_kind_id: 7` and explicitly enumerates no future kinds; `s25_closure: "partial_foundation"` is the only accepted value in 0.1.

## Evidence

- 2026-10-30: `python -m pytest -q -p no:cacheprovider` → **101 passed** (85 + 16 candidate controls); no engine file changed, all characterization tests green on the candidate.
- 2026-10-30: ticket command `python -m pytest -q tests/test_event_registry.py tests/test_log.py` → green.
- 2026-10-30: checker green after registry sync; manifest binding test proves preflight rejects a foreign `schemas.events` version.

## Reviewer decision needed

- Confirm lane identity (`react` split by declared lane, sub-lane kept informational for D0-04) is the intended process-identity granularity before D0-04 builds draw addresses on it.
