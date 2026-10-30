# ADR-D0-02: Distinct logical random addresses for independent events

**Status:** Accepted · **Date:** 2026-10-30 · **Ticket:** [D0-04](../../tasks/D0-04-random-addresses.md) · **Deciders:** Stochastic-kernel maintainer

## Context

`physics_build 0.1` addressed every draw batch as
`seed + tick*γ + fnv(kind) + (cell << 24) + (sub << 48) + offset`.
There is no call counter: two calls at the same
seed/tick/kind/cell/sub restart the same prefix. The public audit reproduces
identical prefixes for a length-10 and a length-16 request with different
payloads; condense and annih calls for different species at one tick and cell
therefore consume the same stream, and per-species behavior inherits
correlated noise (ROADMAP_DIFF defect, D0-04 `problem_evidence`).

D0-03's event registry (semantic_id → 64-bit stable_hash) now provides stable
event/process identity; the ontology lane already separates the four react
producers that `sub` used to (incorrectly) fold together.

## Decision

1. **Addressed streams (RNG schema 0.2).** A logical draw stream is named by
   `(event_hash, tick, cell, channel, seed)`: `event_hash` is the D0-03
   registry `stable_hash` of the event semantic_id, `channel` is an explicit
   u32 species/process id (condense and annih pass the species; the four
   react lanes are distinct events with channel 0), and `offset` allocates a
   sub-range of one stream. Call order, payload and Python container
   iteration order are not inputs.
2. **Deterministic byte encoding.** The address prefix is
   `b"simworld-draw-0.2\n" || LE u64[event_hash] || LE u64[tick] || LE u64[cell] || LE u64[channel] || LE u64[seed]`
   — fixed 58 bytes, no separators, no locale- or platform-dependent pieces.
   `sim/rng.py::encode_draw_address` is the only writer of these bytes.
3. **Stream base and generator.** The stream base is the little-endian head
   (8 bytes) of `sha256(prefix)`. Value `offset` is
   `splitmix64(base + offset)` mapped to [0,1) by the unchanged 0.1
   `>> 11 / 2**53` float rule. Chunking `[0, n)` into sub-ranges yields the
   same values, and values within a stream are a bijection of offsets.
4. **Bounds and overflow.** `cell` and `channel` are u32, `event_hash`,
   `tick`, `seed` are u64; `offset < 2**32` and `offset + n <= 2**32`; the
   batch size stays in `(0, 2**24]`. Violations raise
   `rng.AddressError` before any value is produced; a batch never wraps into
   another stream's counter window.
5. **Duplicate ranges.** `EventContext(diagnose=True)` keeps the allocated
   offset span per `(event, tick, cell, channel)` and rejects an overlapping
   re-allocation with `AddressError` (adjacent offsets are legal; reuse is
   not). Non-diagnostic runs do not pay the bookkeeping, and the acceptance
   battery treats duplicate allocation as a defect signal, not a hard global
   prohibition — the log format does not serialize channel, so cross-process
   duplicate detection is out of scope.
6. **Collision assumptions.** Two distinct logical streams share a base only
   on a truncated-sha256 collision (~2^-64 per pair); we do not claim more.
   Unique addresses guarantee disjoint *inputs*, not statistical
   independence of outputs: independence is exercised by the declared
   battery in `tests/test_rng_addresses.py` (per-stream mean/variance/chi-
   square uniformity, offset-window disjointness) and is never inferred from
   coordinates alone.
7. **Legacy path retained.** Without a registry `event` argument,
   `EventContext.draws` keeps the 0.1 scheme verbatim (toy worlds,
   historical characterization, and the preserved acceptance runs reproduce
   unchanged). Production physics call sites
   (`sim/demo.py`, `weak`, `bind`, `network`, `atoms`, `collapse`) all pass a
   registry identity; new code must not add legacy-addressed stochastic
   calls.
8. **Versioning.** `CURRENT_SCHEMAS["rng"]` advances to `0.2` and
   `NUMERIC_POLICY["addressing"]` is `"logical-0.2"`, so manifests and
   preflight reject mixing addressing schemes. The 0.1 primitive functions
   (`rng.draw`/`draw_float`/`draws`) and their golden vectors are untouched;
   the 0.1 repeated-prefix case is captured as a regression in
   `tests/test_rng_addresses.py` instead of being deleted.

## Consequences

- Trajectories change: seed 42 / 3400 ticks / 8 cells / probe 2,3 moves from
  final_hash `fe8e094a9753b27c89fc0dffd1905f8de4be45263158d5712618ddd5f6ded1a0`
  to `f85d189ec3cea061ae3d176236a92c26af164f6f62fe2e6561f8778df59f6b5d` on the
  candidate. Per D0-01 this is a behavior change on the 0.2-candidate track;
  it does not invalidate the frozen 0.1 acceptance, which belongs to the
  archived source environment at the baseline commit, and a new final hash is
  not a historical-reproduction failure.
- Every characterization band of the 0.1 suite (m2/m3/m4 + physics_bands, 44
  tests) still passes on the re-addressed stream, so no band needed
  re-derivation in D0-04; band re-derivation remains scheduled with
  D0-09/D0-11/D0-12.
- Correlated per-species noise is no longer structurally guaranteed to
  exist; the audit defect "distinct species reuse the same stream" is closed.
  Claims that need *independent* noise (e.g. freeze-out fluctuation
  statistics) may now point at disjoint streams, with the battery above as
  the evidence.
- Log entries are unchanged; verify-mode replay regenerates addressed values
  because replay re-enters each call site with the same registry identity
  and channel. A log is only replayable under the addressing schema
  recorded in its manifest.
