# Contributing to SimWorld

SimWorld is a research prototype. A useful contribution makes a mechanism clearer, an experiment more reproducible, or a scientific claim better supported. Read the [README](README.md), [architecture guide](docs/architecture.md), and [research status](docs/research-status.md) before changing the engine.

## Scope a change

Open an issue or describe the proposed change in a pull request. State the behavior you observed, the behavior you expect, and why the difference matters. For an engine problem, include the seed, configuration, `physics_build`, Python and NumPy versions, and the smallest reproducing command or initial state. Attach public, relevant evidence; remove credentials, local hostnames, and personal filesystem paths.

Separate documentation corrections, implementation repairs, and new physical assumptions. A failed prediction may indicate a model limitation rather than a programming error. A new phase document is a proposal until its implementation and validation exist.

No software license has been chosen. Clarify contribution and reuse terms with the project owner before submitting substantial external work; do not import third-party code or datasets without checking their provenance and terms.

## Preserve experimental meaning

- Keep calibration inputs separate from held-out validation data. Do not tune a model on a benchmark and then present the same benchmark as independent validation.
- Do not silently change constants, reaction semantics, event order, random-stream addressing, or other behavior while retaining the same physics baseline. Update the relevant build identifier, specification, and expected evidence together.
- Retain historical run records. A changed result should have an explanation and a new output directory, not an overwritten artifact.
- Explain approximations and their domain. Passing broad bands is not evidence for stronger physical claims.
- Keep caches regenerable, units explicit, and resource or conservation budgets visible at subsystem boundaries.
- Describe exact replay as an environment-scoped guarantee unless cross-environment tests establish more.

## Work locally

Create a branch for a focused change. Follow the virtual-environment setup in the README, then run the checks relevant to the affected mechanism.

```sh
python -m pytest -q
python -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out runs/change-check
python -m sim.replay runs/change-check
```

Use your virtual environment's Python. The full suite checks existing invariants and acceptance criteria. A repair to a known gap also needs a targeted case that fails before the repair and exercises the missing property afterward. For stochastic changes, state the ensemble, uncertainty, and comparison method instead of relying on a successful single seed.

Website changes should preserve relative paths under the `/simworld/` GitHub Pages project URL, document-reader behavior, mobile layout, and downloadable-file checksums. Do not publish runtime logs, virtual environments, credentials, caches, or temporary analysis files.

## Write understandable code comments

Use comments to explain an assumption, invariant, unit convention, or non-obvious ordering choice. Avoid restating the next line of code. If a kernel is an approximation, identify the approximation and link to the corresponding specification or research-status entry. Keep comments consistent with the executable behavior; a comment asserting detailed balance is not a substitute for a derivation and a test.

## Write commits as a research record

Use a short imperative subject with a scope, followed by a body explaining **what changed, why, and how it was checked**. Keep unrelated changes in separate commits. Do not manufacture historical milestone commits for work that was imported as one existing baseline.

Example:

```text
fix(network): retain reverse channels when reactants are absent

Enumerate reversible channels from the allowed species graph so a
product-only initial state can reach the intended dissociation path.

Explain the changed rate and scheduling assumptions here, including
the new physics baseline and any affected historical comparisons.

Validation: add a product-only regression case, compare fixed-temperature
equilibration from both directions, and verify a newly recorded replay.
```

This example describes a proposed future repair; it is not a claim that the repair has already landed. For documentation-only changes, say which source or observed behavior the text now reflects. For a website deployment, describe the public content and path changes rather than writing only “update site.”

## Prepare a pull request

Explain the concrete problem and resulting behavior first. Include the relevant commands and results, any changed model assumptions or build identifiers, affected documentation, and remaining limitations. For visual changes, include a desktop and mobile view. Link the issue or source evidence where useful.

Reviewers should be able to tell which claims are implemented, which are tested, and which remain proposed. Automated checks help reproduce the work but do not replace scientific review.
