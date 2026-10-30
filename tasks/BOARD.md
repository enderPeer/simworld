# Work board

The authoritative record is [`spec/development_backlog.json`](../spec/development_backlog.json),
validated by `python scripts/check_development_spec.py`. This board mirrors the
ready queue for humans and links a card per active task. Do not mark a phase or
ticket done here; update the structured records together with a card's evidence.

## Recently completed

| Card | Ticket | State |
| --- | --- | --- |
| [D0-03 Event registry and stable event identities](D0-03-event-registry.md) | D0-03 | verified (101/101 tests 2026-10-30, S25 partial foundation) |
| [D0-02 Run manifests and compatibility preflight](D0-02-run-manifests.md) | D0-02 | verified (commit `b5b6287`) |
| [D0-01 Baseline freeze and change control](D0-01-baseline-freeze.md) | D0-01 | verified (commit `d27ed0d`) |

## Next (ready)

| Ticket | Title | State |
| --- | --- | --- |
| D0-04 | Give independent stochastic events distinct random addresses | ready |
| D0-05 | Fingerprint the full causal state with a typed schema | ready |
| D0-06 | Kinetic time units and closed-box reference harness | ready |

## Everything else

D0-07..D0-12 and the R1-R8 stage work packages remain `blocked`; see the
dependency graph in [DEVELOPMENT_SPEC.md](../DEVELOPMENT_SPEC.md) section 5A and
`python scripts/check_development_spec.py --ready` for the live queue.

## Completed here

- 2026-10-30: workspace cleanup — removed gitignored generated data only
  (`tmp/`, `runs/`, `_m3run/`, `_m4run/`, `output/`, `website/.runtime/`,
  `.pytest_cache/`, `__pycache__/`, `_nightly_ci.xml`); `git status` clean before
  and after; all public evidence lives in tracked `website/dist/downloads/`.
- 2026-10-30: spec checker verified green — `Development specification OK:
  17 phases, 12 starter tickets, 112 work packages, 25 seams. Ready queue: D0-01`.
