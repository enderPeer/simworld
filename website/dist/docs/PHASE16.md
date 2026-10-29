# Phase 16 — The Full Emergent Loop (definition of done)

**Goal:** the roadmap's last line becomes a CI artifact. Phase 16
builds **no physics and no sim package** — it runs the world. A
single committed seed + the Phase 0 world rules (D6) go in; a
overnight Great Run on the cluster comes out with the whole ladder
present in the ledgers, in order, with no step scripted:
nucleosynthesis → elements → planetesimals → planet → life →
evolution → humans → fire → bronze → farms → cities → grids → radio
→ **artificial worlds built inside SimWorld by the world's own
agents** (Phase 10's `nest/` at depth 1, D10, born from an in-world
choice event — the roadmap's "AI" demystified to mechanism: a
coalition commissioning a simulation of its own world, its results
entering the claims ledger where the world's own replication fuzz
can and must catch its errors). "No step scripted" is not asserted —
it is **proven structurally**: milestone detectors are frozen
read-only ledger queries written before any Great Run executes; the
run config is linted to contain nothing but world rules + constants +
seed (scripture lint: no phase ≥ 2 noun may appear in it); and the
ladder must complete on **≥ 3 seeds whose paths are structurally
different** — different fire geographies, different numeraires,
different sides of the road, same completeness. Scripted worlds fail
unseen seeds; emergent ones are seed-agnostic, and the diversity
index is reported as the phase's headline number. Second promise, the
playable one: any prefix of the chain opens interactively in under a
minute (era compression D8–D13 + S24 certificates make the past
certificates and the present instantiated), you step forward and the
world keeps **inventing** — the anti-endgame assertion runs a century
past the ladder's last rung and the invention ledger never goes flat.
The definition of done for the whole campaign is this suite green;
the artifact is not a document, it is a world: `seed + log = the
civilization, bit-for-bit, on any machine of the pinned build`.

**Prerequisites (hard gate, from Phase 15 + seam round ten):**

- All sixteen phase gates green; `runtime/` frozen; Phase 14's
  existence suite passing unmodified (this phase inherits it as a
  standing dependency, not a rerun).
- Seam round ten: **S25** landed — a machine-readable cross-phase
  **event ontology** generated from the freeze contracts
  (`spec/ontology.json`, tooling-checked against `KIND_IDS` tables;
  the root cause behind seam S8's kind-id clashes: kinds were
  registried per-phase, never globally). Milestone detectors and the
  surprises ledger both query this ontology; a milestone defined
  against an unregistered kind is red.
- S23/S24 merged (cross-build replay matrix; per-layer
  `::jump_state()` certificates — era traversal without them is
  naive-time and does not fit in nights).
- All compression decisions (D8, D9, D10, D11, D13) machine-checked
  via their S24 certificates — the decisions finally become code, or
  the seams re-open as bugs.
- D6 seeded initial conditions; cluster capacity reserved for the
  nightly Great Run rotation (the overnight-world economics are a
  measured deliverable, not a hope).

**Definition of done:** three seeds, three nights, one table.
**Seed A** (the demo world) completes the full ladder: the frozen
milestone suite queries the chain and returns every rung — first
self-sustaining replication event (Phase 8's closure certificate),
first hominin-grade budget-gated choice (Phase 9), first controlled
fire-analog flux event with the Phase 6/9 fracture-geometry trail,
first smelt-analog (from ore geography, not from a recipe), first
city-grade polis cluster, first grid-tie load-frequency series, first
radio-analog broadcast event on `net/` — each with its era-timestamp
and its surprise-ledger entry, and **zero of them with an injection
timestamp** (there is no such thing; the scripture lint proves the
channel does not exist). **Seed B** reaches every rung by visibly
different paths — different numeraire record class, opposite driving
convention, fire arriving after (not before) a bronze-analog
knapping-legacy route, the academy-analog that commissions the
**nested world** being a fishing coalition, not a university — the
diversity index (structural, computed on milestone *causal ancestry*,
not value hashes) printed beside completeness. **Seed C** runs on a
different cluster machine: same build → bit-identical replay; a
deliberate build bump → within-budget equivalence (D16 asserted both
ways by the suite, never by hand). The nested moment, seed B's
signature scene: a coalition choice event spawns a depth-1 nested
child simulating its fishing grounds; the nested chain hash lands in
the parent chain (D10); its outputs enter the claims ledger; the
world's own replication-analog fuzz **catches one of its claims**
(the in-world modelers' model is wrong about something, caught by
their own world's science — the emergence loop closes on itself with
no human in the loop), and the depth guard proves hard: no child of a
child, the guard tested by adversarial injection attempt.
Playability, measured: opening an arbitrary mid-civilization prefix
interactively takes < 60 s wall on the reference machine (certificates
in, present instantiated), the observer steps a year and follows a
crew through its careers; the **anti-endgame century** runs past the
last rung with the invention-analog ledger still ticking (rate
reported; flatline = red, absorbing states are this phase's only
heresy); the anomaly-by-meter discipline from Phase 14 still holds —
someone can notice anything the world did while nobody was looking.
Cost honesty: per-era wall-time and bytes land in the run record
(the "one world per night" claim is a number, and if it is > 1 night
the number is printed anyway and the era-compression seams re-open as
bugs, never as injections). Failure taxonomy: every Great Run stall
is assigned to its owning phase by milestone-causal bisect (the
chain makes stalls bisectable), filed against that phase's gate —
Phase 16 forbids itself from fixing anything except harness.

---

## Scale contract

- Great Run = the money world's *predecessor chain*: everything from
  seed through the ladder, at era-compressed fidelity, full
  instantiation only where gaze/choice density demands (governor
  rules unchanged).
- Nightly rotation: ≥ 3 Great Run slots (demo seed always; two
  rotating diversity seeds + one cross-build slot weekly); each
  ≤ one cluster night, cost-reported per era (wall-time, chain bytes,
  certificate-refinement count).
- Milestone suite: read-only over the chain; detector code frozen
  (hash-registered) **before** the first Great Run executes —
  detector edits after the fact require the surprises ledger and two
  independent re-derivations of the same chain.
- Nested children: depth 1 hard guard; inner sims sized by their
  commissioners' in-world hardware budget (priced like everything
  else, S16/D10).

## Architecture

No `sim/` additions. Three artifacts, all on the harness side:

```
greatrun/
  seed/       the committed initial conditions: D6 quantum seed +
              constants + world rules ONLY (scripture lint: CI
              rejects any config mentioning phase >= 2 nouns -
              Phase 10's no-device-nouns gate, pointed at the run
              config itself)
  milestones/ frozen read-only queries over the S25 event ontology:
              one detector per ladder rung, each = (event pattern
              over registered kinds + causal-ancestry predicate +
              ordering constraint); written first, hashed, immutable
              in CI; no thresholds tuned post-hoc (bands fixed with
              the detectors, pre-registered)
  reports/    era fingerprints (ordered rung timestamps + surprise
              entries), diversity index (structural: milestone
              causal-ancestry graph edit distance across seeds),
              cost-per-era table, invention-rate chart - all
              derived, replayable, diffable
```

Data rules:

- **The harness has no write path to the world.** It reads chains and
  reports; anything the suite wants from the world it re-derives
  from seed + log (the harness trusts no cached result — including
  its own).
- **Milestones are ledger facts or they are not milestones.** Every
  rung is an event pattern over registered kinds (S25); "civilization
  happened" is not a query; its ledger components are.
- **Diversity before beauty.** A prettier demo seed does not gate;
  cross-seed completeness does. Two seeds agreeing on everything
  *structurally* is itself flagged (hidden-attractor suspicion,
  investigation entry, not a re-tune).

## Work packages

W1 freezes detectors before anything runs (the order is the
methodology); W2 proves seed-agnosticism; W3 closes the nested loop;
W4 earns playability; W5 makes the economics honest; W6 is the
campaign's final gate.

### W1 — Harness + frozen milestones (S25 upstream first)

- [ ] `spec/ontology.json` generated from all freeze contracts +
      KIND_IDS tables (S25; red-first: the S8 clash recurs on
      generation and must resolve).
- [ ] Detector suite written from ROADMAP's ladder text **before any
      Great Run**; hash-registered; scripture lint on run configs.
- [ ] **Tests:** detectors fail loud on synthetic chains missing a
      rung (negative controls — a suite that passes everything is
      not a gate); ordering constraints enforced (fire-analog after
      its geography, smelt-analog after ore, nested child after the
      choice event); lint rejects a planted "fire" noun in a run
      config with a positive control fixture.

### W2 — Seed-agnostic emergence

- [ ] ≥ 3 seeds: completeness table, structural diversity index,
      hidden-attractor flag; nightly rotation wired to the cluster.
- [ ] **Tests:** ladder complete on ALL gating seeds (any seed
      missing a rung = bug against the owning phase, found by
      milestone-causal bisect, filed there — never patched in
      harness); diversity index above floor with floor justified by
      the causal-ancestry metric (reported, not tuned per seed);
      same-build cross-machine replay bit-identical, cross-build
      within-budget (D16 both directions).

### W3 — The nested closure

- [ ] Nested-birth-from-choice-event detection (S25 pattern); depth
      guard adversarial test; child-hash-in-parent-chain check.
- [ ] **Tests:** in-world modelers' claim enters parent claims ledger
      and the replication-analog fuzz catches ≥ 1 error in it (the
      closure keystone - the world's science working on the world's
      own simulations); nested results influence at least one
      subsequent choice event (parent agents act on their simulation;
      reported pathway); depth guard cannot be bypassed by any
      registered event sequence (exhaustive over registered kinds).

### W4 — Playability + anti-endgame

- [ ] Time-travel: open any prefix interactively; observer
      discipline inherited from Phase 14 (no harness-induced
      observation collapse - harness gaze is metered and minimal).
- [ ] **Tests:** prefix-open < 60 s on reference machine (p50,
      p95 reported); step-forward keeps ledgers live; anti-endgame
      century past last rung: invention-analog rate flatline check
      (red on flatline), plus whether any polity starts *narrating*
      the ladder retroactively (Phase 11 meaning machinery -
      reported as history-theology surprise, physics stays linted).

### W5 — Overnight-world economics

- [ ] Cost-per-era table in every run record; cluster slot
      accounting; degradation alerts when era costs drift (ties into
      Phase 15's perf-ledger CI).
- [ ] **Tests:** 3-slot nightly fits in wall-time with margin
      (measured, reported); any era exceeding its compression budget
      re-opens its D-decision as a tracked bug (no silent budget
      raises); byte-growth-per-era monotonicity report (chain
      compression honest).

### W6 — The campaign gate

- [ ] Definition-of-done suite: all sixteen gates + Great Run table +
      diversity + nested closure + playability + anti-endgame +
      economics, one green button.
- [ ] Published worlds = `seed + observation log + pinned build id`
      triples in the releases record; D17 (seed-agnosticism as the
      definition of unscripted) into `spec/decisions.md`; ROADMAP
      checkbox ceremony - the roadmap is then done.

## Performance budget (fill from W2–W5)

| Path                                        | Budget              | Measured |
|---------------------------------------------|---------------------|----------|
| Great Run wall-time (seed A, demo world)    | ≤ 1 cluster night   | ___      |
| era traversal, certificate-only (past eras) | < 1 s / era         | ___      |
| prefix open to interactive (any tick)       | < 60 s p50          | ___      |
| milestone suite over full chain             | < 10 min            | ___      |
| diversity index computation                 | < 30 min            | ___      |
| chain size at ladder completion             | < 100 GB            | ___      |
| nightly 3-slot rotation                     | ≤ 100% of 1 night   | ___      |
| nested child run (commissioner budget)      | parent-priced, S16  | ___      |

## Interface exposed to Phase 17 (there is no Phase 17)

> This is the terminal interface. The world exposes itself: any
> prefix is a save, any save is replayable, any observer is a guest
> of the gaze map. Post-campaign, the standing contract is the Great
> Run suite itself — a future change that breaks the ladder is a
> regression, not a release. What leaves the campaign: seeds + logs
> as worlds, the milestone ontology as the language the world is
> written in, and the published numbers as the answer to "was any of
> it scripted": the suite says no, and the suite is the proof.

## Verification strategy

1. **Detectors-before-data law:** the frozen milestone suite exists
   and is reviewed before the first Great Run executes; post-hoc
   detector edits require two independent chain re-derivations and
   land as surprises-ledger events, never silently.
2. Negative controls over everything: planted-rung synthetic chains
   make detectors fail; planted nouns make the lint fail; planted
   depth-2 nesting attempts must be refused by the guard.
3. Seed-agnosticism is the gate (D17): completeness across all
   gating seeds, structural diversity reported, structural
   agreement flagged as suspicious (the anti-scripted test inverted).
4. Chain-derived-everything: every reported fact re-derives from
   seed + log on a clean machine (harness caches are never trusted,
   including by the harness itself).
5. Surprises ledger, the campaign's closing entry list: which rung
   each seed took longest to reach, whether any seed invents a rung
   in a different order than the ROADMAP lists it (the roadmap is an
   ordering of questions, not of history - if the world disagrees
   about order while completing the ladder, that is a discovery, and
   it is reported as the first one).

## Sequencing

```
Wk 1            Wk 2-4              Wk 4-6               Wk 5-7         Wk 7-8
─────           ─────               ──────               ─────          ─────────
W1 harness +    W2 seeds x3        W3 nested closure    W5 economics   W6 campaign gate
frozen          (nightly           (needs ladder        (cost tables   +published
detectors       rotation starts)   reached on >= 1)     honest)        worlds + D17
(scripture      (failure bisects                        (budget breaks
lint first)     to owning phases)                      re-open D's)
                                   W4 playability +
                                   anti-endgame
                                   (parallel, wk 3+)
```

## Risks

| Risk | Mitigation |
|---|---|
| Milestone gaming: detectors generous enough to pass on noise | detectors frozen pre-run, negative controls mandatory, bands pre-registered; post-hoc edits carry a two-witness ceremony cost |
| The ladder stalls at 3 a.m. on one seed and the phase quietly injects | harness has no write path (architecture, not policy); stalls bisect to owning phases via chain causality; a stall on any gating seed is red for the campaign, loudly |
| Seed lottery: the demo seed carries the narrative | gate is completeness across ALL gating seeds + diversity floor; demo seed is reported, not gated |
| "AI inside SimWorld" overhyped into AGI theater | the nested closure is mechanism: choice event, priced compute, depth guard, claims-ledger feedback, fuzz catching errors; no vocabulary beyond that is permitted in code, tests, or reports |
| Overnight economics fail quietly (era costs drift back to naive) | cost-per-era in every record, drift alerts wired to Phase 15 perf CI, budget exhaustion re-opens the owning D-decision as a bug |
| Playability degrades as worlds age (certificate rot, chain bloat) | prefix-open p95 is a gated number; chain byte-growth report; rot found by nightly replay of oldest published world |

**Gate (the campaign's):** the definition-of-done suite is green
offline: all sixteen phase gates, Great Run ladder complete on all
gating seeds with diversity above floor and zero scripture-lint
findings, nested closure keystone green (nested birth from choice,
fuzz catching a nested claim's error, depth guard unbreachable),
playability numbers met (prefix open p95, anti-endgame century
inventing), economics reported with every era inside its compression
budget, S25 ontology merged, D17 in `spec/decisions.md`, and three
published `seed + log + build` worlds replayable by any clean
machine of the pinned build.
