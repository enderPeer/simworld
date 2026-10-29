"""physics-build 0.1 table (BUILD0.md). Changing any value bumps PHYSICS_BUILD.

Real-world numbers never appear here; oracle values live in tests/oracle/ only.
"""

PHYSICS_BUILD = "0.1"

T0_MEV = 100.0
T0_S = 1.0e-5
EXPANSION_RATE = 1.01
N_CELLS = 8
TOTAL_TICKS = 3400  # M4: extended to carry the world through recombination

M_Q = 300.0
DELTA_FLAVOR = 0.01
M_E = 0.511
ALPHA_S = 0.5
ALPHA_EM = 1.0 / 137.036
LAMBDA_CONF = 0.2
ETA = 6.1e-10
EPS_B = 1.0e-9
C_W = 3.3e-3   # M3: bands green over seeds 0-2026; freeze-out T ~ 1.3 MeV
C_CAP = 5.0    # M3: network rate; burns 3He in before the jump window shuts
S_FACTOR = 1.0

# M2 slice calibration (engine units; part of build 0.1)
V_CELL = 0.05
THETA = 100
THETA_BATCH = 2
JUMP_SPAN = 1000

# M3 slice: liquid-drop coefficients fit offline on the five oracle anchors
# (tests/oracle/fit_nuc_anchors.py); published here as engine constants,
# never runtime lookups. Nucleon-level masses are the reference B = 0.
NUC_A_V = 13.624573
NUC_A_S = 11.660260
NUC_A_C = 0.550939
NUC_A_A = 24.412199
NUC_A_P = 10.956941
GAMOW_G = 4.0
SAHA_PHI = 0.02
NUC_Z_MAX = 4
NUC_A_MAX = 12

# M4 slice: atoms. I = 1/2 alpha_em^2 m_e is computed in atoms.py, not here.
# C_REC fixes when capture completes; SAHA_PHI_E is the atomic phase-space
# scale that puts the Saha transition in the run; T_REC_REF is the published
# T-law reference. Rejected alternative: engineering the transition shape
# directly (that would not be detailed balance).
C_REC = 6.0e-5
T_REC_REF = 1.0e-3
SAHA_PHI_E = 1.8e5

KIND_IDS = {
    "condense": 0,
    "collide": 1,
    "react": 2,
    "decay": 3,
    "annih": 4,
}


def time_at(tick, expansion_rate=EXPANSION_RATE, t0_s=T0_S):
    return t0_s * (expansion_rate ** tick)


def scale_factor(t, t0_s=T0_S):
    return (t / t0_s) ** 0.5


def temperature(t, t0_mev=T0_MEV, t0_s=T0_S):
    return t0_mev / scale_factor(t, t0_s)
