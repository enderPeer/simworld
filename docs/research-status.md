# Research status

This document separates demonstrated implementation behavior from the proposed research program. Its numerical audit results refer to **29 October 2026** and `physics_build 0.1`; they are not a substitute for checking the current revision.

## Implemented scope

The Python micro-seed provides analytic expansion and cooling, finite thermal populations, effective weak conversion and nucleon formation, a bounded nuclear reaction network, aggregate electron capture, event logging, and deterministic replay checks. It is a calibrated reduced model, not a first-principles quantum or precision cosmological calculation.

The roadmap has 17 phases. Detailed `PHASE*.md` files explain proposed mechanisms, dependencies, performance ambitions, and acceptance gates. Their presence does not mark the corresponding phase complete. Simplified nuclear and atomic behavior in the Phase 0 build does not establish completion of the full nuclear and atomic research programs.

The white paper preserves the source snapshot examined when it was written. Current plans may include later additions. Use the current roadmap and document inventory for planning coverage, and the paper's archived materials for reproducing its specific claims.

## Dated verification evidence

The audit used Python 3.11.9, NumPy 2.4.6, and pytest 9.1.1 on the recorded Windows environment.

| Check or observable | Audit result | Interpretation |
| --- | --- | --- |
| Existing full test suite | 65 passed | Existing regression assertions held |
| Seed-42 fresh run | Archived summary and decompressed event log matched | Reproducible in the tested environment |
| Replay | All 34 saved state hashes matched | Regenerated history matched the reference |
| Cells and ticks | 8 cells; 3,400 ticks | One small finite-population experiment |
| Helium-4 mass fraction | 0.2276176024 | Inside the project's broad fitted acceptance band |
| Hydrogen mass fraction | 0.7473444613 | Inside the project's acceptance band |
| Ionized electron fraction | 0.0034572169 | Aggregate electron-ledger statistic |
| Deuterium and lithium ratios | Both zero | Insufficient evidence for abundance validation |

The run and replay each took about 5.55 seconds while other test work was active. These single observations are not controlled throughput benchmarks. The full suite took 123.64 seconds in that audit.

The full-precision [run summary](../website/dist/downloads/SimWorld_Verified_Run.json), [test report](../website/dist/downloads/SimWorld_Test_Report.xml), and [diagnostic evidence](../website/dist/downloads/SimWorld_Audit_Diagnostics.json) are available with the [white paper](../website/dist/downloads/SimWorld_Research_White_Paper.pdf). Public versions redact workstation identifiers without changing the reported scientific outcomes.

## Known gaps

| Area | Observed limitation | What would establish progress |
| --- | --- | --- |
| Nuclear reverse reactions | Channel enumeration can omit dissociation when the forward reactants are absent; reverse coefficients also differ from the stated detailed-balance relation | Derive reversible propensities and test product-only and reactant-rich initial states against a reference equilibrium |
| Atomic ionization | Fully captured species are excluded from updates, allowing a fully neutral state to remain absorbing | Demonstrate relaxation from both neutral and ionized states across fixed-temperature controls |
| Stochastic streams | Calls at the same seed, tick, kind, cell, and sub-lane reuse draw prefixes | Define unique event addressing and test independence and scheduling behavior while preserving versioned replay |
| Physical rates and resolution | Per-tick heuristics and calibrated engine scales do not establish a converged physical-time integrator | Specify units and time mapping; measure time-step, population, and resolution dependence |
| Calibration | Several acceptance observations are also tuning targets | Freeze calibration inputs and evaluate held-out physical cases and uncertainty |
| Rare abundances | A population of roughly a thousand hydrogen nuclei cannot resolve a small primordial deuterium abundance accurately | Use appropriate ensemble or population designs with counting uncertainty |
| Runtime evidence | The array microbenchmark differs from the dictionary-based main storage | Measure the actual integrated workload, including logging, hashing, reactions, and memory |
| Observation | Probe-triggered state changes affect weak conversion | Separate physical measurement, numerical refinement, and display behavior; test the intended observable invariances |

The atomic diagnostic is a concrete counterexample: 100 fully neutral hydrogen nuclei at `T_GATE / 1.2` produced no events over 1,000 steps, although the model's own Saha helper predicted a positive ionized fraction. The existing test suite passed because its assertions do not cover that state. A green suite is evidence for its tested properties, not for every statement in a specification.

## Design records and implementation can disagree

The frozen records in `spec/` preserve the project's design history. Some statements describe intended guarantees more strongly than the code currently supports. In particular, array-only quant storage, general detailed balance, and broad observation independence must not be inferred from those records alone. The [architecture guide](architecture.md), code, and targeted diagnostics provide the implementation-level account.

The terminology of quantum fields, superposition, and collapse also needs care. The baseline has effective field metadata and record transitions; it does not establish coherent quantum dynamics or intrinsic quantum randomness. Seeded pseudorandomness makes experiments repeatable but is a different claim.

## Near-term research sequence

1. Repair and test reverse-path reachability and atomic equilibration without hiding changes behind the existing baseline.
2. Give independent stochastic events explicit, versioned stream identities.
3. Establish dimensional rate conventions and conservation budgets across subsystem boundaries.
4. Separate fitted data from held-out validation, and measure numerical and stochastic uncertainty.
5. Benchmark the actual engine at stated fidelity and problem size.
6. Demonstrate one validated cross-layer experiment before extending to a much larger simulated history.

For later life and social phases, evaluate conditional distributions and controlled interventions rather than require a prescribed historical sequence. Extinction, failed discovery, alternative technologies, and different institutions must remain informative possible results.

The central research question remains open: can transparent effective models preserve useful causal structure while supporting more complex behavior at practical computational cost? The current project's contribution is a reproducible baseline and a detailed agenda for testing that question.
