import random

import pytest

from sim.rng import draw, draw_float, draws, fnv1a64, splitmix64

M64 = (1 << 64) - 1


def ref_splitmix(x):
    x = (x + 0x9E3779B97F4A7C15) & M64
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return (z ^ (z >> 31)) & M64


def ref_fnv(b):
    h = 0xCBF29CE484222325
    for by in b:
        h = ((h ^ by) * 0x100000001B3) & M64
    return h


REF_KIND_HASH = {
    name: ref_fnv(kid.to_bytes(2, "little"))
    for name, kid in [("condense", 0), ("collide", 1), ("react", 2), ("decay", 3), ("annih", 4)]
}


def ref_draw(seed, tick, kind, i):
    x = (seed + (tick * 0x9E3779B97F4A7C15) + REF_KIND_HASH[kind] + i) & M64
    return ref_splitmix(x)


def test_fnv1a64_published_vectors():
    assert fnv1a64(b"") == 0xCBF29CE484222325
    assert fnv1a64(b"a") == 0xAF63DC4C8601EC8C


def test_splitmix64_stays_in_u64():
    assert splitmix64(M64) <= M64


def test_golden_vectors():
    assert draw(0, 0, "collide", 0) == 0x8407EF2F80C2D2BC
    assert draw(42, 7, "react", 3) == 0x3D042455398D6C13
    assert draw((1 << 64) - 1, (1 << 63) - 1, "annih", (1 << 64) - 1) == 0x4C0C803F8D8A99F4
    assert draw(123456789, 2400, "condense", 5) == 0x8282183EE8DA2466
    assert draw_float(0, 0, "collide", 0) == 0.5157460680936865
    assert draw_float(42, 7, "react", 3) == 0.2383444507664102
    assert draw_float((1 << 64) - 1, (1 << 63) - 1, "annih", (1 << 64) - 1) == 0.29706574966034294
    assert draw_float(123456789, 2400, "condense", 5) == 0.5097975877368772


def test_matches_independent_reference():
    rng = random.Random(1)
    kinds = list(REF_KIND_HASH)
    for _ in range(20000):
        args = (rng.getrandbits(64), rng.randrange(10 ** 6),
                rng.choice(kinds), rng.getrandbits(64))
        assert draw(*args) == ref_draw(*args)


def test_vectorized_matches_scalar():
    vec = [float(x) for x in draws(42, 7, "react", 5)]
    assert vec == [draw_float(42, 7, "react", j) for j in range(5)]
    assert len(draws(1, 2, "decay", 0)) == 0


def test_distribution_smoke():
    big = draws(7, 11, "decay", 200000)
    assert 0.49 < big.mean() < 0.51
    assert big.min() >= 0.0
    assert big.max() < 1.0
    assert len(set(big.tolist())) == len(big)


def test_unknown_kind_raises():
    with pytest.raises(KeyError):
        draw(1, 1, "nonsense", 0)
