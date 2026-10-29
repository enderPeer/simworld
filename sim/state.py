"""Canonical state fingerprints for same-environment replay comparisons.

The digest includes the physics-build label, a NUL separator, the tick and
each supplied column's length and float64 bytes. Integer metadata uses
little-endian encoding; NumPy arrays use the host's native float64 byte
order. World.columns() determines column order and sorts records by ID.
Cross-platform byte equality requires additional numerical guarantees.

HashChain is a historical name for an ordered list of independent state
hashes: each digest does not include the preceding digest. It is not a
cryptographic chain or a complete checkpoint of every runtime variable.
"""

import hashlib
import json

import numpy as np


def canonical_hash(physics_build, tick, columns):
    h = hashlib.sha256()
    h.update(physics_build.encode("utf-8"))
    h.update(b"\x00")
    h.update(int(tick).to_bytes(8, "little"))
    for col in columns:
        arr = np.ascontiguousarray(col, dtype=np.float64)
        h.update(int(arr.size).to_bytes(8, "little"))
        h.update(arr.tobytes())
    return h.hexdigest()


class HashChain:
    def __init__(self):
        self.pairs = []

    def add(self, tick, columns, physics_build):
        digest = canonical_hash(physics_build, tick, columns)
        self.pairs.append((int(tick), digest))
        return digest

    def final(self):
        return self.pairs[-1][1] if self.pairs else None

    def write(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.pairs, fh)

    @staticmethod
    def read(path):
        with open(path, encoding="utf-8") as fh:
            return [(int(t), d) for t, d in json.load(fh)]

    def __eq__(self, other):
        return list(self.pairs) == list(other.pairs if hasattr(other, "pairs") else other)

    def diff(self, other):
        other = list(other.pairs if hasattr(other, "pairs") else other)
        mine = list(self.pairs)
        for i, (a, b) in enumerate(zip(mine, other)):
            if a != b:
                return (i, a, b)
        if len(mine) != len(other):
            return (min(len(mine), len(other)), ("len", len(mine)), ("len", len(other)))
        return None
