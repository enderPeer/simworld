# Constants — physics_build 0.1 (frozen 2026-10-28)

Source of truth is `sim/constants.py`; this is the published table with
calibration anchors. Changing any value bumps `PHYSICS_BUILD`. Real-world
numbers appear here **only** as engine-side anchors already absorbed into
tuned constants; oracle values live exclusively in `tests/oracle/`.

Natural units, energies in MeV.

## Cosmology & lattice

| constant         | value    | role                                        |
|------------------|----------|---------------------------------------------|
| `T0_MEV`         | 100.0    | start temperature                           |
| `T0_S`           | 1e-5     | start time [s]                              |
| `EXPANSION_RATE` | 1.01     | geometric tick step (D5)                    |
| `N_CELLS`        | 8        | demo lattice (jump-eligible cells: all 8)   |
| `TOTAL_TICKS`    | 3400     | default run through recombination (M4)      |
| `V_CELL`         | 0.05     | engine cell volume (density scale)          |
| `THETA`          | 100      | collapse threshold (D4)                     |
| `THETA_BATCH`    | 2        | max thetas swept per cell interaction       |
| `JUMP_SPAN`      | 1000     | jump-state skip length (D5)                 |

## Fields (D2)

| constant         | value       | role                                  |
|------------------|-------------|----------------------------------------|
| `M_Q`            | 300.0       | base quark mass                        |
| `DELTA_FLAVOR`   | 0.01        | u/d split -> nucleon gap (FIXED, anchor)|
| `M_E`            | 0.511       | electron mass                          |
| `ALPHA_S`        | 0.5         | strong coupling                        |
| `ALPHA_EM`       | 1/137.036   | em coupling                            |
| `LAMBDA_CONF`    | 0.2         | confinement scale (~tick 1246)         |
| `ETA`            | 6.1e-10     | baryon asymmetry                       |
| `EPS_B`          | 1e-9        | matter-antimatter excess (baked into condensation sampling) |

## Reaction slice (M3)

| constant        | value    | role                                        |
|-----------------|----------|----------------------------------------------|
| `C_W`           | 3.3e-3   | effective weak rate — **calibrated**          |
| `C_CAP`         | 5.0      | radiative capture scale — **calibrated**      |
| `S_FACTOR`      | 1.0      | astrophysical S-factor (charged fusion)       |
| `GAMOW_G`       | 4.0      | Gamow window width (engine units)             |
| `SAHA_PHI`      | 0.02     | nuclear Saha phase-space scale                |
| `NUC_A_V/S/C/A/P` | 13.624573 / 11.660260 / 0.550939 / 24.412199 / 10.956941 | liquid-drop coefficients, fit OFFLINE on the five `tests/oracle/nuc_anchors.json` anchors only — published, never runtime lookups |
| `NUC_Z_MAX`     | 4        | chart extent (engine truncation)              |
| `NUC_A_MAX`     | 12       | chart extent                                  |

## Atom slice (M4)

I = 1/2 alpha_em^2 m_e = 1.3606e-5 MeV is **computed** from `ALPHA_EM`
and `M_E` in `sim/atoms.py`, never stored — that is the hydrogenic
analytic anchor, the only real-physics form allowed in `sim/` besides
`hydrogenic` naming.

| constant       | value   | role                                            |
|----------------|---------|--------------------------------------------------|
| `T_GATE`       | 3*I     | capture gate, structural: atoms off above it     |
| `C_REC`        | 6.0e-5  | recombination prefactor — **calibrated** (X_neutral band) |
| `T_REC_REF`    | 1e-3    | T-law reference (alpha ~ T^-1/2)                 |
| `SAHA_PHI_E`   | 1.8e5   | atomic phase-space scale; Saha reads X_e ≈ 0.17 at the 3I gate and ≈ 0.006 at run end, so the transition epoch lands inside the capture window |

Recombination and photoionization share the one prefactor, so equilibrium
is Saha by construction (detailed balance), not by engineering; the
closed form `atoms.saha_x_e` is that same equilibrium.

## Calibration protocol (declared before tuning, BUILD0 risk table)

Three acceptance anchors: n/p band 0.10-0.20, Y_p band 0.20-0.30, X_H
band 0.69-0.80. Tuned: `C_W` (n/p + epoch), `C_CAP` (Y_p; also burns
3He before the jump window shuts). `DELTA_FLAVOR` fixed. M4 added one
band (X_neutral >= 0.90 + X_e <= 2 Saha, order-of-magnitude below) tuned
with `C_REC`; `SAHA_PHI_E` shapes where the Saha curve sits inside the
window (gate onset itself is structural: T_GATE = 3I, first capture at
tick 2958). Everything else published untouched. Six seeds 0-2026 pass
all bands simultaneously; no seed cherry-picking.

## RNG lanes (sub-streams, frozen)

sub 0 = weak flips; sub 1 = baryon bind; sub 2 = nuclear network;
sub 3 = atoms. KIND_IDS: condense 0, collide 1, react 2, decay 3,
annih 4 — atoms draws are kind `react`, cause `atoms`.

## Oracle discipline

`tests/oracle/` is the only place real-world numbers live
(`nuc_anchors.json` = the five binding anchors). A suite test greps
`sim/` for element/material names (helium, lithium, deuter, tritium,
beryllium, boron) and fails the build on any hit — `hydrogenic` is the
one sanctioned analytic word.
