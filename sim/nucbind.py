"""Semi-empirical binding B(Z, A) in engine MeV (BUILD0 M3).

Liquid drop + pairing + asymmetry, five coefficients calibrated offline on
five oracle anchors (tests/oracle/) and published in constants.py; this
module never looks anything up at runtime. Nucleons are the reference:
B = 0 for A <= 1 regardless of the raw polynomial (the formula is not
meant to be applied to single nucleons).
"""

from . import constants as C


def pairing(Z, A):
    if A % 2:
        return 0.0
    return 1.0 if Z % 2 == 0 else -1.0


def binding(Z, A):
    if A <= 1:
        return 0.0
    a13 = A ** (1.0 / 3.0)
    return (C.NUC_A_V * A
            - C.NUC_A_S * a13 * a13
            - C.NUC_A_C * Z * (Z - 1) / a13
            - C.NUC_A_A * (A - 2 * Z) ** 2 / A
            + C.NUC_A_P * pairing(Z, A) * A ** -0.75)


def mass(Z, A, m_u, m_d):
    """Nucleus rest mass from the field table minus binding."""
    return Z * m_u + (A - Z) * m_d - binding(Z, A)
