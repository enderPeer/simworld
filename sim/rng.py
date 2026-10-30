"""The one source of randomness (BUILD0.md RNG spec): counter-based, stateless.

draw(seed, tick, kind, i):
    x = (seed + tick*0x9E3779B97F4A7C15 + fnv1a64(kind) + i) mod 2^64
    return splitmix64(x)

float() = top 53 bits / 2^53. No RNG state is ever serialized anywhere.
kind is a u16 id (sim.constants.KIND_IDS); fnv1a64 runs over its 2-byte
little-endian encoding.
"""

import hashlib

import numpy as np

from .constants import KIND_IDS

M64 = (1 << 64) - 1
GOLDEN_GAMMA = 0x9E3779B97F4A7C15
MIX_A = 0xBF58476D1CE4E5B9
MIX_B = 0x94D049BB133111EB
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3

# D0-04 logical draw addressing (ADR-D0-02-random-addresses.md).
ADDRESSING_SCHEMA = "logical-0.2"
_ADDRESS_SALT = b"simworld-draw-0.2\n"
U32_LIMIT = 1 << 32


class AddressError(ValueError):
    """A logical draw address is out of bounds or a range overlaps another."""


def _check_field(name, value, limit=U32_LIMIT):
    if not isinstance(value, int) or isinstance(value, bool):
        raise AddressError(f"{name} must be an integer, got {value!r}")
    if not 0 <= value < limit:
        raise AddressError(f"{name}={value} outside [0, {limit})")
    return value


def encode_draw_address(event_hash, tick, cell, channel, seed):
    """Deterministic byte encoding of one logical draw address prefix (0.2).

    salt || five little-endian u64 fields: event stable_hash, tick, cell,
    channel, seed. Fixed length 8 + 40 bytes; no separators, no Python
    container or call order anywhere in the encoding.
    """
    event_hash = _check_field("event_hash", event_hash, 1 << 64)
    tick = _check_field("tick", tick, 1 << 64)
    cell = _check_field("cell", cell)
    channel = _check_field("channel", channel)
    seed = _check_field("seed", seed, 1 << 64)
    return _ADDRESS_SALT + b"".join(
        int(v).to_bytes(8, "little")
        for v in (event_hash, tick, cell, channel, seed))


def address_base64(event_hash, tick, cell, channel, seed):
    """u64 stream base: little-endian head of sha256(encode_draw_address).

    Collision assumption: two distinct logical streams share a base only on a
    truncated-sha256 collision (~2^-64 per pair); within one stream the
    counter is a bijection, so disjoint offsets give disjoint generator inputs.
    """
    digest = hashlib.sha256(
        encode_draw_address(event_hash, tick, cell, channel, seed)).digest()
    return int.from_bytes(digest[:8], "little")


def draw_at(event_hash, tick, cell, channel, seed, offset):
    _check_field("offset", offset)
    base = address_base64(event_hash, tick, cell, channel, seed)
    return splitmix64((base + int(offset)) & M64)


def draw_at_float(event_hash, tick, cell, channel, seed, offset):
    return (draw_at(event_hash, tick, cell, channel, seed, offset) >> 11) / _TWO53


def draws_at(event_hash, tick, cell, channel, seed, n, offset=0):
    if n == 0:
        return np.empty(0, dtype=np.float64)
    if not 0 < n <= (1 << 24):
        raise AddressError(f"draw batch must be in (0, 2**24], got {n}")
    _check_field("offset", offset)
    if offset + n > U32_LIMIT:
        raise AddressError(f"range [{offset}, {offset + n}) exceeds 2**32")
    base = address_base64(event_hash, tick, cell, channel, seed)
    with np.errstate(over="ignore"):
        x = (base + _U64(offset) + np.arange(n, dtype=np.uint64)) & _U64(M64)
        x = (x + _U64(GOLDEN_GAMMA)).astype(_U64)
        z = (x ^ (x >> _U64(30))) * _U64(MIX_A)
        z = (z ^ (z >> _U64(27))) * _U64(MIX_B)
        z = z ^ (z >> _U64(31))
    return (z >> _U64(11)).astype(np.float64) * (1.0 / _TWO53)


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
