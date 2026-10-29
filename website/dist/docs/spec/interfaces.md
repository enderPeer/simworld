# Interfaces — frozen at physics_build 0.1 (2026-10-28)

## Phase 0 -> Phase 1 boundary (BUILD0 freeze line, verbatim)

> Phase 1 may read: the quant tables (S/C) by id, the field/coupling
> table, the observation log, jump-state summaries, and the collapse
> rule's θ + interaction counts. Phase 1 may write: extended collapse
> causes (probe contract) and new field rows via a physics-build bump.
> Nothing else crosses the boundary; `bind`/`network` internals are
> private and get replaced wholesale by Phase 2's real kernels.

## Internal coupling contracts (physics_build 0.1)

The only data each subsystem passes per tick. All state is numpy column
arrays; all randomness goes through `EventContext.draws` (kind, cell,
sub-lane, payload); all hot paths are elementwise numpy.

| producer -> consumer      | contract                                        |
|---------------------------|--------------------------------------------------|
| lattice -> all            | `(tick, T)` uniform; `condense.targets(T)` only |
| store -> weak/bind/jump   | alive counts per (cell, species); row ops via store methods only |
| weak -> bind              | freeze-out p_n snapshot (taken once, at T < Lambda_conf, frozen value after weak freeze-out) |
| bind -> network           | `nuc.add(cell, Z, A, k)` — (Z, A) keys, no names |
| network -> atoms/demo     | `nuc.counts[species, cell]` read-only during step |
| network -> jump           | `network.jump_quiet(nuc, cell, T)` — every channel prob < 1e-8 at current T (rates decrease with T, so the check at jump time bounds the whole span) |
| atoms -> jump             | `atoms.jump_quiet(atom, nuc, cell, T)` — capture rates GROW as the cell cools, so the worst case is the landing temperature: quiet iff `T · 1.01^(-span/2) >= T_GATE` |
| atoms -> store/weak       | nothing (atoms never touch quanta; electrons are a charge ledger, not rows) |
| all -> hash chain         | `columns()` float arrays, concatenated in fixed order: lat, store, nuc, atom |
| all -> log                | `ctx.draws(tick, kind, cell, sub, n, payload, cause)`; one entry per call; draw counts are a pure function of state + stream |

### RNG sub-lanes (frozen): 0 weak, 1 bind, 2 nuclear network, 3 atoms.

### Atoms contract (M4)

`AtomStore.captured[cell, species]` = electrons bound to that nuclide in
that cell, `0 .. Z*n`; spread-filling (every nucleus reaches level cap
before any reaches cap+1) makes the scalar sufficient. Free electrons are
derived, never stored: `e_free = sum(Z*n) - sum(captured)` — charge
neutrality is bookkeeping, not dynamics. Forward recombination and
reverse photoionization share one prefactor (detailed balance => Saha
equilibrium by construction); capture is structurally gated at
`T_GATE = 3 I`. No electron rows exist anywhere.

## Replacement plan (why these lines are safe to freeze)

`bind` + `network` + `atoms` are demo-grade kernels with published
interfaces; Phase 2 replaces their insides (real force kernels, real
recombination coefficients) behind the same `add/step/jump_quiet/columns`
shape. The quant tables, log, hash chain, collapse rule, and jump-state
machinery are what Phase 1 actually consumes and does not change.
