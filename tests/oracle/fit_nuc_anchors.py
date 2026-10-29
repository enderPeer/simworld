"""Offline calibration: fit the 5 liquid-drop coefficients on the 5 oracle
anchors (BUILD0: anchors calibrate constants, never runtime lookups).

Run manually:  python tests/oracle/fit_nuc_anchors.py
Paste the printed line into sim/nucbind.py (NUC_COEFFS). Not imported at
runtime; nothing in sim/ reads the anchors.
"""

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
DATA = json.loads((HERE / "nuc_anchors.json").read_text(encoding="utf-8"))


def basis(Z, A):
    pair = 0.0
    if A % 2 == 0:
        pair = 1.0 if Z % 2 == 0 else -1.0
    return [A, -A ** (2.0 / 3.0), -(Z * (Z - 1)) / A ** (1.0 / 3.0),
            -((A - 2 * Z) ** 2) / A, pair * A ** -0.75]


def main():
    rows = np.array([basis(a["Z"], a["A"]) for a in DATA["anchors"]])
    b = np.array([a["B"] for a in DATA["anchors"]])
    coeffs = np.linalg.solve(rows, b)
    names = ("a_v", "a_s", "a_c", "a_a", "a_p")
    for n, c in zip(names, coeffs):
        print(f"{n} = {c:.6f}")
    print("\nNUC_COEFFS =", [round(float(c), 6) for c in coeffs])
    print("\nsanity gaps (want < 0 for A=5, A=8; > 0 for A=2,4):")

    def B(Z, A):
        return float(np.dot(basis(Z, A), coeffs))

    for (Z, A) in [(0, 1), (1, 1), (0, 5), (1, 5), (2, 5), (2, 6), (2, 8),
                   (3, 6), (3, 7), (2, 4)]:
        print(f"B({Z},{A}) = {B(Z, A):8.3f}")
    print("gap 5->4+p:", B(2, 5) - B(2, 4) - B(1, 1))
    print("gap 8->4+4:", B(2, 8) - 2 * B(2, 4))
    print("gap d->p+n:", B(1, 2) - B(1, 1) - B(0, 1))


if __name__ == "__main__":
    main()
