# Documentation index

## Read in this order

| # | Document | Role |
| --- | --- | --- |
| 1 | [README.md](../README.md) | Project overview and pinned environment |
| 2 | [BUILD0.md](../BUILD0.md) | The binding v0 contract and the accepted 0.1 micro-slice |
| 3 | [ROADMAP.md](../ROADMAP.md) | The 17-phase research thesis (long-term vision) |
| 4 | [ROADMAP_DIFF.md](../ROADMAP_DIFF.md) | 29 Oct 2026 audit: roadmap claims vs. executable reality |
| 5 | [DEVELOPMENT_SPEC.md](../DEVELOPMENT_SPEC.md) | **Controlling execution plan**: D0 tickets, R1-R8 stages, seam gates, vocabulary |
| 6 | [PHASE0.md](../PHASE0.md) … [PHASE16.md](../PHASE16.md) | Detailed per-phase research sources (design, not completion proofs) |

## Execution records

| Document | Role |
| --- | --- |
| [spec/development_backlog.json](../spec/development_backlog.json) | Authoritative tickets, phases, seams, dependencies (checked by `scripts/check_development_spec.py`) |
| [spec/status.json](../spec/status.json) | Current implementation state, seam summary, ready queue |
| [spec/development_sources.json](../spec/development_sources.json) | Fingerprints of inputs reconciled for planning v1.0 |
| [../tasks/BOARD.md](../tasks/BOARD.md) | Human work board mirroring the ready queue |
| [spec/adr/](../spec/adr/) | Architecture decision records (ADR-D0-01 first) |
| [spec/baselines/physics-0.1.json](../spec/baselines/physics-0.1.json) | Frozen 0.1 execution identity |
| [spec/test-scope.json](../spec/test-scope.json) | Test classification and execution contexts |

## Frozen specs and references

| Document | Role |
| --- | --- |
| [spec/constants.md](../spec/constants.md) | Frozen constant set for the build line |
| [spec/decisions.md](../spec/decisions.md) | Original D1-D5 build decisions |
| [spec/interfaces.md](../spec/interfaces.md) | Frozen 0.1 module interfaces |
| [spec/seams.md](../spec/seams.md) | S1-S25 seam ledger |
| [spec/surprises.md](../spec/surprises.md) | Recorded unexpected behaviors |
| [architecture.md](architecture.md) | Engine module architecture |
| [research-status.md](research-status.md) | Research status and known gaps |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution and model-versioning discipline |
| [../CHANGELOG.md](../CHANGELOG.md) | Release history |

Rule: a passing test, a plan, or a document never by itself closes a phase —
acceptance requires the evidence named in the ticket and the seam ledger.
