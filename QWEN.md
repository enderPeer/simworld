# QWEN.md — working notes for AI agents on this repo

Read this first, then trust the structured records over any prose. The project
is **SimWorld**: a small deterministic-replay cosmology/physics demo (`sim/`)
under strict change-control (`spec/`, `tasks/`). Current work is executing the
**D0 tickets** in the development backlog one at a time, in dependency order,
each ending in one commit.

## Current state (snapshot 2026-10-30)

- HEAD = `0771afe` **"D0-04: distinct logical random addresses (RNG schema 0.2)"**.
  Commit chain: `2a74160` frozen baseline → `d27ed0d` D0-01 → `b5b6287` D0-02 →
  `4d332c6` D0-03 → `0771afe` D0-04. Working tree clean; **126/126 tests green**.
- Verified tickets: D0-01 (baseline freeze), D0-02 (run manifests), D0-03
  (event ontology), D0-04 (addressed RNG streams). Ready queue: **D0-05, D0-06**.
- Next ticket: **D0-05 "Fingerprint the full causal state with a typed
  schema"** — read its backlog entry (state schema, canonical hash, driver
  flags, lossless int ids, explicit endianness; new files
  `spec/state-schema.json`, `tests/test_causal_state.py`). D0-06 is the other
  ready one (kinetic time, design-heavy, includes `ADR-D0-03-kinetic-time.md`).
- D0-04 changed trajectories: candidate seed-42/3400 final_hash is
  `f85d189ec3cea061ae3d176236a92c26af164f6f62fe2e6561f8778df59f6b5d`
  (frozen 0.1 acceptance hash stays `fe8e094a...d1a0` — never re-score it).
  All 44 characterization-band tests still pass, so nothing is archived-gated
  yet; band re-derivation stays scheduled at D0-09/D0-11/D0-12.

## Sources of truth (update together, never prose-only)

| File | Role |
| --- | --- |
| `spec/development_backlog.json` | authoritative tickets; flip `state`, fill `evidence` (paths must exist), keep top-level `ready_now` == recomputed queue |
| `spec/status.json` | must mirror `ready_now` exactly (checker enforces both copies) |
| `spec/test-scope.json` | classification of the frozen 65 baseline tests + `scope_exempt_files` for new candidate-control files (each new `tests/test_*.py` needs an exemption entry + a `notes` line, else `test_scope_covers_full_collection` fails) |
| `spec/baselines/candidate.json` | candidate sim-tree registration (see commit dance) |
| `spec/baselines/physics-0.1.json`, `website/dist/downloads/*` | frozen 0.1 evidence — never edit |
| `tasks/BOARD.md` + one card `tasks/D0-0X-*.md` per ticket | human mirror |
| `DEVELOPMENT_SPEC.md` §5A, `spec/seams.md` | spec text; seams stay OPEN unless fully closed |
| `scripts/check_development_spec.py` | the validator — run until it says OK |

Engine facts: `sim/manifest.py::CURRENT_SCHEMAS = {log:0.2, rng:0.2, state:0.1,
events:0.1, manifest:run-manifest/0.1}`; `NUMERIC_POLICY` carries
`rng_scheme: splitmix64-fnv1a-0.1` (0.1 primitives, untouched) and
`addressing: logical-0.2`. Addressed draws live in `sim/rng.py`
(`encode_draw_address/address_base64/draws_at`); `EventContext.draws(...,
event=, channel=, offset=)` (event = `spec/ontology.json` semantic_id, see
`sim/ontology.py`). Legacy addressing stays for toy-world tests.
`physics_build` label stays **0.1** until D0-12 per ADR-D0-01.

## The ticket loop (repeat for D0-05 …)

1. `python scripts/check_development_spec.py --ready`; pick the earliest ready
   ticket; read its backlog entry + `DEVELOPMENT_SPEC.md` section + linked
   audit evidence.
2. Implement per `change` + `acceptance`. New tests get **new names**; never
   weaken or xfail existing 0.1 tests. Map each acceptance clause to a named
   test in the ticket card.
3. If you add a test file: exempt it in `spec/test-scope.json`
   (`scope_exempt_files` + `notes`).
4. Full verify: `python -m pytest -q -p no:cacheprovider` (expect previous
   count + new tests), then the ticket's `validation_commands_after_implementation`.
5. Registries: backlog `state: "verified"` + `evidence` paths; both `ready_now`
   lists shrink; card under `tasks/`; BOARD row moves to "Recently completed".
6. Commit dance (PowerShell, from repo root):

   ```
   python scripts/check_development_spec.py        # must be OK before commit
   git add sim tests spec tasks
   $TREE = git write-tree; git rev-parse ("{0}:sim" -f $TREE)   # new sim tree
   # put that tree into candidate.json: sim_tree = new, previous_sim_trees
   #   gets the old one as "after_D0-0X", bump ticket/note (+schema fields if a
   #   schema moved); re-add spec
   git add spec; $TREE = git write-tree
   if ((git rev-parse ("{0}:sim" -f $TREE)) -eq "<that tree>") { git commit ... }
   ```

   `test_engine_trees_match_frozen_baseline` compares **HEAD**:sim against
   `candidate.json`, so the full suite is only fully green *after* the commit
   lands — run pytest post-commit too, plus `git status --porcelain` (must be
   empty) and the checker.

## Environment & shell pitfalls

- Windows 10, PowerShell 5.1, Python 3.11.9, NumPy 2.4.6 (repo is pinned to
  this env; CI mirrors it). `pytest -p no:cacheprovider`.
- PowerShell has **no heredoc and no `&&`**. For multi-line Python, write a
  script under `tmp/` (gitignored) and run `python tmp/whatever.py`; chain with
  `;` + `if ($?) { ... }`. Avoid `"$VAR:sim"` (it eats `:sim`) — use
  `("{0}:sim" -f $VAR)`. CRLF→LF warnings from `git add` are normal.
- `np.math` is gone in NumPy 2.x — use `math.erfc` etc.
- The `cluster_*` MCP tools and the gen-1 tunnel notes in global AGENTS.md are
  dead — ignore; everything here is local.
- `tmp/` currently holds patcher scripts and `d004-run/` (a demo output); safe
  to delete, gitignored.

## Style rules learned the hard way

- Checker: `ready_now` must match the recomputed queue in **both** registries;
  every `evidence` path must exist; seam-ledger parsing uses the **last column**
  of `spec/seams.md` rows.
- Do not touch frozen artifacts (`website/dist/downloads/*`,
  `physics-0.1.json`, baseline commit) or the 0.1 golden vectors in
  `tests/test_rng.py`; record new goldens as new named constants instead.
- Preflight (`sim/manifest.py`) rejects manifests with foreign schema versions
  — when you bump a schema in `CURRENT_SCHEMAS`, expect old disposable run
  dirs under `tmp/` to be rejected (that's the point, not a bug).
- `replay_dir()` returns `True`/raises; `run_recorded()` returns the summary
  dict. `demo.run_recorded(seed, ticks, cells, out_dir, probe_cells=(), jump)`.
- Keep ADR prose in the house format (see `spec/adr/`), status/date/ticket/
  deciders header line, Context/Decision/Consequences.
- Commits: one per ticket, message = title line + factual body; stage only
  `sim/ tests/ spec/ tasks/` (+ `scripts/` if a script changed).

## Useful entry points

- Run: `python -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out tmp/run`
- Replay/verify: `python -m sim.replay tmp/run`
- Addressing ADR: `spec/adr/ADR-D0-02-random-addresses.md`; versioning ADR:
  `spec/adr/ADR-D0-01-versioning.md`; defects ledger: `ROADMAP_DIFF.md`.
- Test classes (D0-01 ADR): 27 `shared_invariant`, 34 `characterization_0_1`,
  4 `model_validation`; archived 0.1 env = `git worktree add <dir> 2a74160`
  (only needed if a characterization test ever starts failing on the candidate).
