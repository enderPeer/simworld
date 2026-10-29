# Implementation architecture

The current engine is a reduced stochastic micro-seed in Python. This guide describes the executable model; the larger mechanisms in `PHASE*.md` are a research program. The [research-status guide](research-status.md) records where historical design descriptions exceed the implementation.

## Entry points and run artifacts

`python -m sim.demo` calls `run_recorded`, which creates an event context, executes the tick loop, writes periodic state hashes, and saves a final summary. `python -m sim.replay <run-directory>` loads the log header, regenerates the run, verifies event keys, and compares the saved hashes.

The reproducibility inputs include the seed, physics build, tick and cell counts, probe coverage, jump setting, source implementation, and numerical environment. The log is an experiment record, not a complete resumable checkpoint or a cryptographically linked chain of every state.

## State representations

| State | Implementation | Meaning |
| --- | --- | --- |
| Temperature and model time | `lattice.py`, `constants.py` | Shared analytic cooling and expansion schedule |
| Quant records | `quanta.py` | Python dictionaries of per-record lists, per-cell species pools, and NumPy count arrays |
| Effective fields | `fields.py` | Five specified field entries with masses, charges, spins, and coupling labels |
| Nuclear populations | `network.NucStore` | Integer counts indexed by `(Z, A)` and cell |
| Bound electrons | `atoms.AtomStore` | Aggregate captured-electron counts per nuclide and cell |
| Random and logged events | `rng.py`, `log.py` | Deterministic draws, event keys, payload digests, and replay checks |
| State fingerprints | `state.py` | Canonical state columns hashed with SHA-256 |

The main quant storage differs from the array-only structure-of-arrays design measured in `spikes/a_quant_cost`. That prototype's throughput does not describe the integrated engine.

## Tick sequence

The driver in [`sim/demo.py`](../sim/demo.py) coordinates the following operations:

1. Update the prescribed time and uniform cell temperature.
2. Check whether an unprobed, cooled cell is eligible to skip quiet work.
3. Materialize thermal population deficits and remove selected surplus populations.
4. Apply weak flavor conversion and sample effective nucleons below the confinement threshold.
5. Evaluate the bounded nuclear reaction network and aggregate atomic capture when permitted.
6. Apply interaction-threshold and probe-triggered collapse operations.
7. Hash the canonical state at the configured intervals and finish the event record.

Time follows a geometric schedule rather than a fixed physical time step. Population and rate scales are calibrated in engine units. Cell names and a lattice container do not imply that the model includes fluid transport, spatial gravity, or a dynamical cosmological metric.

## Binding and reaction models

`nucbind.py` computes a semi-empirical binding formula with fitted coefficients. `bind.py` caches channel eligibility and adds explicit stability restrictions. `network.py` samples transitions over a finite species range. The registry is a cache of a chosen model, not an exhaustive search over all physically possible nuclei or reactions.

`atoms.py` computes a hydrogenic binding scale and tracks capture through aggregate electron counts. Free electrons are derived from nuclear charge minus bound electrons. This provides an accounting identity, not orbital wavefunctions or a dynamical radiation bath. The summary's `X_neutral = 1 - X_e` is a **bound-electron fraction** and is not generally a neutral-atom number fraction for mixtures of multielectron species.

The current reverse-channel and fully neutral-state limitations are described in [research status](research-status.md). Do not infer validated detailed balance from the appearance of paired rate expressions or an analytic equilibrium helper.

## Observation and numerical detail

Probe coverage and cell-level interaction counts trigger movement between records named superposed and collapsed. These names describe the reduced representation. The engine does not implement general coherent many-body dynamics, interference experiments, or an entanglement solver.

Probe-triggered collapse also affects which quark records can undergo weak conversion. Existing equivalence checks therefore cover selected population and removal observables, not complete observer independence of the physical model.

`jump.py` skips work only in a restricted quiet regime. Its gates consult nuclear and atomic conditions to avoid known active intervals. Selected regression cases match detailed evolution exactly; a small nonzero channel hazard is not a proof that every possible jump is universally equivalent.

## Randomness and replay

`rng.py` generates deterministic values from counter coordinates. `EventContext.draws` partitions coordinates by event kind, cell, and subsystem lane. It logs the event key and a digest of supplied IDs or payloads. In verify mode, the regenerated key must match the next recorded event.

Repeated calls at identical coordinates currently restart at the same prefix. Reproducibility consequently does not establish independence between all stochastic events. Changing stream addressing changes the simulated history and must be versioned and evaluated as a behavioral change.

The demonstrated exact-replay scope is the same source, configuration, and numerical environment. Cross-platform equality, parallel scheduling equivalence, checkpoint resumption, and scientific validity are separate properties.

## Website and project records

The website in `website/dist/` is static HTML, CSS, JavaScript, documents, and downloads. GitHub Pages hosts those files; the Python engine runs separately. The local Node server and optional Cloudflare scripts are development conveniences.

The public downloads distinguish the archived white-paper snapshot from current planning documents. Generated source archives and checksum manifests should be refreshed when their inputs change. They must not include `.runtime`, virtual environments, credentials, or private workstation metadata.
