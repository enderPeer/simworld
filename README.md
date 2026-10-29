# SimWorld

**A reproducible physical seed and a research program for an emergent world.**

[Project website](https://enderpeer.github.io/simworld/) · [Research white paper](website/dist/downloads/SimWorld_Research_White_Paper.pdf) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

[![CI](https://github.com/enderPeer/simworld/actions/workflows/ci.yml/badge.svg)](https://github.com/enderPeer/simworld/actions/workflows/ci.yml)
[![GitHub Pages](https://github.com/enderPeer/simworld/actions/workflows/pages.yml/badge.svg)](https://github.com/enderPeer/simworld/actions/workflows/pages.yml)

SimWorld explores whether physical processes, life, learning, technology, and institutions can connect through one continuous simulated history. The long-term goal is to study higher-level patterns that arise from explicit local mechanisms, with recorded causes and measurable approximation errors.

The executable project is currently a **small, effective stochastic physics model**. It expands and cools a hot seed, forms simplified nuclei, captures electrons, and records a history that can be replayed. Chemistry, planets, life, agents, and civilizations are research plans; they have not been implemented or demonstrated by this engine.

## Start here

| If you want to… | Read or run… |
| --- | --- |
| Understand the idea and explore the documents | [Project website](https://enderpeer.github.io/simworld/) |
| Run the existing model | [Quick start](#quick-start) below |
| Understand the implementation | [Architecture guide](docs/architecture.md) |
| Evaluate the scientific claims and limitations | [Research status](docs/research-status.md) and the [white paper](website/dist/downloads/SimWorld_Research_White_Paper.pdf) |
| See the full research program | [ROADMAP.md](ROADMAP.md) and the individual `PHASE*.md` plans |
| Propose a change | [CONTRIBUTING.md](CONTRIBUTING.md) |

## What is implemented

- A shared analytic expansion and cooling schedule, with finite thermal populations in cells.
- Effective weak conversion, simplified nucleon formation, a bounded nuclear reaction network, and aggregate electron capture.
- Seeded random draws, compressed event logs, canonical state hashes, and replay verification.
- Restricted skipping of quiet cells, with regression tests against detailed evolution in selected cases.
- A static project website with the roadmap, document reader, research references, and downloadable evidence.

The current physics version is `physics_build 0.1`. The model uses explicit assumptions, fitted coefficients, and structural restrictions. Names such as “quant,” “superposed,” and “collapse” describe this implementation's representation; they do not establish that it solves fundamental quantum dynamics.

## Quick start

Run commands from the repository root. The audited environment used **Python 3.11.9**, **NumPy 2.4.6**, and **pytest 9.1.1**. Dependencies are pinned in [requirements.txt](requirements.txt).

### Windows PowerShell

```powershell
git clone https://github.com/enderPeer/simworld.git
cd simworld
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out runs/demo
.\.venv\Scripts\python.exe -m sim.replay runs/demo
```

### Linux or macOS

```sh
git clone https://github.com/enderPeer/simworld.git
cd simworld
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out runs/demo
.venv/bin/python -m sim.replay runs/demo
```

The commands are portable entry points. Exact cross-platform output identity is **not** an established guarantee; compare runs within the same source, configuration, and numerical environment.

The demo produces:

| File | Purpose |
| --- | --- |
| `summary.json` | Configuration, final metrics, and final state hash |
| `run.jsonl.gz` | Compressed event history used during replay |
| `hashes.json` | Periodic state hashes for comparison |

Successful replay prints `REPLAY PASS`. Replay regenerates the run and checks its recorded events and hashes; it does not simply display the saved result. Use a new output directory for a new experiment to preserve previous evidence. Run `python -m sim.demo --help` with your environment's Python for available options, including `--no-jump`.

## Verified baseline and open problems

The **29 October 2026 audit** reported 65 passing tests. A fresh seed-42 run reproduced the archived summary, decompressed event log, and all 34 recorded state hashes in that environment. This is dated verification evidence, not a claim that every later revision passes or that the physical model is independently validated.

The same audit identified important gaps:

- Some nuclear reverse pathways are omitted when the corresponding forward reactants are absent.
- Fully neutral atomic populations can become absorbing states even when the model's equilibrium helper predicts ionization.
- Repeated random calls at the same stream coordinates can share prefixes.
- The array-storage speed prototype uses a different representation from the main dictionary-based quant store.

Broad fitted acceptance bands, a small population, and a passing regression suite do not establish precision cosmology. See [research status](docs/research-status.md) for the scope of each result and the proposed next experiments.

## Repository map

| Location | Contents |
| --- | --- |
| [`sim/`](sim/) | Runnable Python engine and replay CLI |
| [`tests/`](tests/) | Regression tests, acceptance bands, and calibration anchors |
| [`spikes/`](spikes/) | Separate quant-cost and shell-approximation experiments |
| [`spec/`](spec/) | Constants, decisions, interfaces, known surprises, and cross-phase dependencies |
| [`BUILD0.md`](BUILD0.md) | Contract for the first runnable micro-seed |
| [`ROADMAP.md`](ROADMAP.md), `PHASE*.md` | Proposed scope, mechanisms, and gates across 17 phases |
| [`docs/`](docs/) | Reader guides and implementation status |
| [`website/`](website/) | Static website, content tooling, and optional local server |
| [`website/dist/downloads/`](website/dist/downloads/) | Public white paper, source archives, and audit evidence |

White paper **v1.1** includes detailed profiles of all 17 phases and the verified project status at its recorded source commit. The research archive separates that current source baseline from the preserved original simulation audit. Editable publication sources are in [`research/whitepaper/`](research/whitepaper/). A new plan is not evidence that its proposed system has been built.

## Website and downloads

The public site is hosted at **[enderpeer.github.io/simworld](https://enderpeer.github.io/simworld/)**. GitHub Pages serves the static content independently of a developer's computer or local Cloudflare process. It does not run the Python simulation in visitors' browsers.

For a local preview, install Node.js and run:

```sh
node website/server.mjs
```

Then open `http://127.0.0.1:8787`. The optional Cloudflare scripts in `website/` provide temporary sharing; they are not required for the GitHub Pages site.

Use the website's [download section](https://enderpeer.github.io/simworld/#downloads) for the paper and public research materials. Download manifests include SHA-256 checksums. Workstation identifiers have been removed from public evidence distributions; scientific results and model assumptions remain documented.

## Contributing and licensing

Changes should explain the problem, the mechanism, the affected model assumptions, and the validation performed. Physics or stochastic behavior changes require explicit versioning and a new baseline rather than silently replacing old evidence. [CONTRIBUTING.md](CONTRIBUTING.md) describes the workflow and commit-message format.

No software license has been selected for this repository. Public availability does not itself grant a general license to reuse, modify, or redistribute the work. Do not assume an open-source license from the repository's visibility.
