# D0-04 — Distinct random addresses for independent events

**State:** verified · **Ticket:** [D0-04](../spec/development_backlog.json) ·
**ADR:** [ADR-D0-02](../spec/adr/ADR-D0-02-random-addresses.md) · 2026-10-30

## Problem (audit-backed)

`EventContext.draws` addressed batches as
`(cell << 24) + (sub << 48) + offset` per call with no call counter, so
condense/annih calls for different species at the same tick/kind/cell
restarted the same stream; the audit reproduces identical prefixes for
length-10 and length-16 requests with different payloads
(`SimWorld_Audit_Diagnostics.json:rng_reuse_diagnostic`).

## Change

- New addressed stream (RNG schema `0.2`): prefix
  `b"simworld-draw-0.2\n" || LE u64[event_hash, tick, cell, channel, seed]`,
  base = LE u64 head of `sha256(prefix)`, value(offset) =
  `splitmix64(base + offset)` with the unchanged `>>11 / 2**53` float rule
  (`sim/rng.py`: `encode_draw_address`, `address_base64`, `draw_at`,
  `draw_at_float`, `draws_at`, `AddressError`).
- `EventContext.draws(..., event=, channel=, offset=)`: `event` is a D0-03
  registry semantic_id resolved to its stable_hash; `channel` is an explicit
  u32 species id (condense/annih), react lanes are distinct events. Bounds
  are u32 cell/channel, offset < 2**32, batch <= 2**24;
  `EventContext(diagnose=True)` rejects overlapping offset ranges.
- All seven production call sites pass registry identities
  (`demo` condense/annih with `channel=sp`, `weak`/`bind`/`network`/`atoms`,
  `collapse.probe_sweep`); the legacy scheme stays for toy worlds and 0.1
  history. `CURRENT_SCHEMAS["rng"]` -> `0.2`,
  `NUMERIC_POLICY["addressing"] = "logical-0.2"` so manifests reject mixing.
- 0.1 primitives and their golden vectors untouched; the repeated-prefix
  defect is captured as a regression test instead.

## Acceptance mapping

| Acceptance | Where |
| --- | --- |
| repeated-prefix regression captured; disjoint addresses; duplicates rejected in diagnostic mode | `test_legacy_same_coordinates_restart_the_prefix`, `test_addressed_channels_do_not_share_prefixes`, `test_distinct_logical_events_receive_disjoint_addresses`, `test_diagnostic_mode_rejects_overlapping_ranges` |
| chunking / reorder invariance; omission does not shift streams | `test_chunking_a_range_equals_the_single_call`, `test_reordering_independent_events_is_invariant`, `test_omitted_event_does_not_shift_other_streams` |
| scalar/vector goldens; bounds fail clearly; record/verify identical new-build history | `test_golden_vectors_scalar_and_vector_match`, `test_encoding_is_deterministic_bytes`, `test_out_of_bounds_fields_fail_clearly`, `test_offset_and_batch_bounds`, `test_record_verify_regenerates_identical_history` |
| separately declared statistical battery, no independence overclaim | `test_statistical_battery_per_stream`, `test_disjoint_offsets_never_share_generator_inputs` |

## Validation

- `python -m pytest -q tests/test_rng.py tests/test_rng_addresses.py tests/test_log.py tests/test_replay.py` -> pass
- full suite `python -m pytest -q -p no:cacheprovider` -> **126 passed**
  (65 baseline + 61 candidate controls); checker green.
- trajectory change observed, bands unaffected: seed 42 / 3400 ticks / 8
  cells / probe 2,3 final_hash
  `fe8e094a9753b27c89fc0dffd1905f8de4be45263158d5712618ddd5f6ded1a0` (frozen 0.1)
  -> `f85d189ec3cea061ae3d176236a92c26af164f6f62fe2e6561f8778df59f6b5d`
  (candidate). All 44 characterization-band tests pass on the new stream, so
  no band was re-derived here (stays scheduled at D0-09/D0-11/D0-12); the
  frozen acceptance hash is not re-scored on the candidate.

## Compatibility

Behavior change on the 0.2-candidate track per ADR-D0-01; the preserved 0.1
artifacts and their hashes belong to the archived source environment at the
baseline commit and are unchanged. `physics_build` label stays `0.1` until
the D0-12 release dossier.
