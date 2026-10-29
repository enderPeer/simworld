"""The one source of randomness (BUILD0.md RNG spec): counter-based, stateless.

draw(seed, tick, kind, i):
    x = (seed + tick*0x9E3779B97F4A7C15 + fnv1a64(kind) + i) mod 2^64
    return splitmix64(x)

float() = top 53 bits / 2^53. No RNG state is ever serialized anywhere.
kind is a u16 id (sim.constants.KIND_IDS); fnv1a64 runs over its 2-byte
little-endian encoding.
"""

import numpy as np

from .constants import KIND_IDS

M64 = (1 << 64) - 1
GOLDEN_GAMMA = 0x9E3779B97F4A7C15
MIX_A = 0xBF58476D1CE4E5B9
MIX_B = 0x94D049BB133111EB
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3

_U64 = np.uint64
_TWO53 = 2.0 ** 53


def splitmix64(x):
    x = (x + GOLDEN_GAMMA) & M64
    z = x
    z = ((z ^ (z >> 30)) * MIX_A) & M64
    z = ((z ^ (z >> 27)) * MIX_B) & M64
    return (z ^ (z >> 31)) & M64


def fnv1a64(data):
    h = FNV_OFFSET
    for byte in data:
        h = ((h ^ byte) * FNV_PRIME) & M64
    return h


_KIND_HASH = {}
for _name, _id in KIND_IDS.items():
    _KIND_HASH[_name] = fnv1a64(_id.to_bytes(2, "little"))
    _KIND_HASH[_id] = _KIND_HASH[_name]

# Log-only entry kinds (never drawn from; keys non-stochastic log events):
# every id here must stay out of KIND_IDS so no draw stream can use them.
LOG_KIND_IDS = {"collapse": 5, "jump": 6}

_LOG_KIND_HASH = {
    _name: fnv1a64(_id.to_bytes(2, "little"))
    for _name, _id in LOG_KIND_IDS.items()
}


def kind_hash(kind):
    return _KIND_HASH[kind]


def entry_kind_hash(kind):
    """u16-able hash for a log entry kind, draw kinds and log-only kinds."""
    if kind in _KIND_HASH:
        return _KIND_HASH[kind]
    return _LOG_KIND_HASH[kind]


def draw(seed, tick, kind, i):
    x = (seed + (tick * GOLDEN_GAMMA) + kind_hash(kind) + i) & M64
    return splitmix64(x)


def draw_float(seed, tick, kind, i):
    return (draw(seed, tick, kind, i) >> 11) / _TWO53


def draws(seed, tick, kind, n, start=0):
    if n == 0:
        return np.empty(0, dtype=np.float64)
    idx = np.arange(start, start + n, dtype=np.uint64)
    with np.errstate(over="ignore"):
        x = (
            _U64(seed & M64)
            + _U64((tick * GOLDEN_GAMMA) & M64)
            + _U64(kind_hash(kind))
            + idx
        )
        x = (x + _U64(GOLDEN_GAMMA)).astype(_U64)
        z = (x ^ (x >> _U64(30))) * _U64(MIX_A)
        z = (z ^ (z >> _U64(27))) * _U64(MIX_B)
        z = z ^ (z >> _U64(31))
    return (z >> _U64(11)).astype(np.float64) * (1.0 / _TWO53)
