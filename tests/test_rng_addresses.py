"""D0-04 logical draw addresses (ADR-D0-02-random-addresses.md).

Covers the addressing defect regression (0.1 prefix reuse), the disjoint,
chunk, reorder and omission properties, scalar/vector golden vectors,
bounds and diagnostic duplicate-range behaviour, record/verify identity
on the new build, and a separately declared statistical battery.
"""

import math

import numpy as np
import pytest

from sim import ontology, replay, rng
from sim.log import EventContext, LogError

SEED = 2026
EH = 0x0123456789abcdef  # stream-agnostic test identity, not in the registry
WEAK_HASH = ontology.registry_identity_index()["draw.react@1/weak"]

GOLDENS8 = [0.08693743602724424, 0.5876776471192553, 0.057641638014112484,
            0.1246077175982453, 0.9883546050071871, 0.04811521536692254,
            0.5968271895924384, 0.2108125126434781]
CHUNK3_AT_5 = GOLDENS8[5:8]
ENC_HEX = ("73696d776f726c642d647261772d302e320a"
           "efcdab89674523012a00000000000000"
           "07000000000000000300000000000000"
           "ea07000000000000")
BASE_HEX = "9fbcefb7df96dcf6"
WEAK_STREAM4 = [0.6687223292288889, 0.8177519492971788,
                0.33959659538071474, 0.4202924658004348]


def off_ctx(**kw):
    return EventContext(SEED, mode="off", **kw)


# --- addressing defect regression ------------------------------------------

def test_legacy_same_coordinates_restart_the_prefix():
    """0.1 defect kept as a regression: condense-style calls at the same
    tick/kind/cell/sub return identical values regardless of payload."""
    ctx = off_ctx()
    a = ctx.draws(7, "condense", cell=3, payload=[10.0], n=10)
    b = ctx.draws(7, "condense", cell=3, payload=[16.0], n=16)
    assert np.array_equal(a, b[:10])  # the audited repeated-prefix case


def test_addressed_channels_do_not_share_prefixes():
    ctx = off_ctx()
    a = ctx.draws(7, "condense", cell=3, payload=[10.0], n=10,
                  event="draw.condense@1", channel=2)
    b = ctx.draws(7, "condense", cell=3, payload=[16.0], n=16,
                  event="draw.condense@1", channel=3)
    assert not (set(a.tolist()) & set(b.tolist()))


def test_distinct_logical_events_receive_disjoint_addresses():
    ctx = off_ctx(diagnose=True)
    streams = []
    for event in ("draw.condense@1", "draw.annih@1", "draw.decay@1",
                  "draw.react@1/weak", "draw.react@1/bind"):
        for channel in (0, 1, 2):
            v = ctx.draws(9, "condense", cell=5, n=24, event=event,
                          channel=channel)
            streams.append(v)
    seen = set()
    for v in streams:
        assert not (seen & set(v.tolist()))
        seen |= set(v.tolist())


def test_diagnostic_mode_rejects_overlapping_ranges():
    ctx = off_ctx(diagnose=True)
    ctx.draws(3, "condense", cell=1, n=10, event="draw.condense@1", channel=0)
    ctx.draws(3, "condense", cell=1, n=4, event="draw.condense@1",
              channel=0, offset=10)  # adjacent is fine
    with pytest.raises(rng.AddressError, match="duplicate draw range"):
        ctx.draws(3, "condense", cell=1, n=4, event="draw.condense@1",
                  channel=0, offset=8)
    # other streams are unaffected, and non-diagnosing contexts allow reuse
    ctx.draws(3, "condense", cell=1, n=4, event="draw.condense@1", channel=1)
    EventContext(SEED, mode="off").draws(
        3, "condense", cell=1, n=4, event="draw.condense@1", channel=0)


# --- stream algebra ----------------------------------------------------------

def test_chunking_a_range_equals_the_single_call():
    ctx = off_ctx()
    whole = ctx.draws(4, "react", cell=2, n=16, event="draw.react@1/network")
    head = ctx.draws(4, "react", cell=2, n=10, event="draw.react@1/network")
    tail = ctx.draws(4, "react", cell=2, n=6, event="draw.react@1/network",
                     offset=10)
    assert np.array_equal(whole, np.concatenate([head, tail]))


def test_reordering_independent_events_is_invariant():
    ctx = off_ctx()
    first = {}
    for event in ("draw.react@1/weak", "draw.react@1/atoms", "draw.decay@1"):
        first[event] = ctx.draws(6, "react", cell=0, n=12, event=event)
    ctx2 = off_ctx()
    for event in reversed(list(first)):
        again = ctx2.draws(6, "react", cell=0, n=12, event=event)
        assert np.array_equal(first[event], again)


def test_omitted_event_does_not_shift_other_streams():
    ctx = off_ctx()
    solo = ctx.draws(8, "react", cell=9, n=8, event="draw.react@1/bind")
    ctx2 = off_ctx()
    ctx2.draws(8, "react", cell=9, n=64, event="draw.condense@1", channel=0)
    ctx2.draws(8, "react", cell=9, n=5, event="draw.annih@1", channel=2)
    still = ctx2.draws(8, "react", cell=9, n=8, event="draw.react@1/bind")
    assert np.array_equal(solo, still)


# --- deterministic encoding, goldens, scalar/vector agreement ----------------

def test_encoding_is_deterministic_bytes():
    enc = rng.encode_draw_address(EH, 42, 7, 3, SEED)
    assert enc.hex() == ENC_HEX
    assert len(enc) == 58
    assert rng.address_base64(EH, 42, 7, 3, SEED) == int(BASE_HEX, 16)


def test_golden_vectors_scalar_and_vector_match():
    got = rng.draws_at(EH, 42, 7, 3, SEED, 8)
    assert got.tolist() == GOLDENS8
    scalars = [rng.draw_at_float(EH, 42, 7, 3, SEED, i) for i in range(8)]
    assert scalars == GOLDENS8
    assert rng.draws_at(EH, 42, 7, 3, SEED, 3, offset=5).tolist() == CHUNK3_AT_5


def test_registry_identity_feeds_the_address():
    got = rng.draws_at(WEAK_HASH, 42, 7, 0, SEED, 4)
    assert got.tolist() == WEAK_STREAM4
    ctx = off_ctx()
    via_ctx = ctx.draws(42, "react", cell=7, n=4, event="draw.react@1/weak")
    assert np.array_equal(got, via_ctx)


def test_every_address_field_changes_the_stream():
    base = rng.address_base64(EH, 42, 7, 3, SEED)
    variants = [rng.address_base64(*args) for args in [
        (EH + 1, 42, 7, 3, SEED), (EH, 43, 7, 3, SEED),
        (EH, 42, 8, 3, SEED), (EH, 42, 7, 4, SEED), (EH, 42, 7, 3, SEED + 1)]]
    assert base not in variants
    assert len(set(variants)) == 5


# --- bounds -------------------------------------------------------------------

@pytest.mark.parametrize("field,value", [
    ("cell", 1 << 32), ("cell", -1), ("channel", 1 << 32),
    ("tick", 1 << 64), ("event_hash", -1), ("seed", -1),
    ("cell", 1.5), ("channel", True),
])
def test_out_of_bounds_fields_fail_clearly(field, value):
    args = {"event_hash": EH, "tick": 42, "cell": 7, "channel": 3, "seed": SEED}
    args[field] = value
    with pytest.raises(rng.AddressError):
        rng.address_base64(**args)


def test_offset_and_batch_bounds():
    with pytest.raises(rng.AddressError, match="exceeds 2\\*\\*32"):
        rng.draws_at(EH, 0, 0, 0, SEED, 10, offset=(1 << 32) - 5)
    with pytest.raises(rng.AddressError, match="2\\*\\*24"):
        rng.draws_at(EH, 0, 0, 0, SEED, (1 << 24) + 1)
    with pytest.raises(rng.AddressError):
        rng.draws_at(EH, 0, 0, 0, SEED, 4, offset=-1)
    with pytest.raises(rng.AddressError):
        rng.draw_at(EH, 0, 0, 0, SEED, 1 << 32)


def test_unknown_event_identity_is_rejected():
    ctx = off_ctx()
    with pytest.raises(LogError, match="not in the registry"):
        ctx.draws(1, "react", n=2, event="draw.nobody@9")


# --- record/verify on the new build --------------------------------------------

def test_record_verify_regenerates_identical_history(tmp_path):
    from sim import demo
    from sim.log import LogError
    run_dir = tmp_path / "d004-mini"
    summary = demo.run_recorded(7, 90, 4, run_dir)
    assert replay.replay_dir(run_dir, quiet=True) is True
    assert summary["final_hash"]
    with pytest.raises(LogError):
        replay.replay_dir(run_dir.parent / "does-not-exist")


def test_legacy_history_without_addressing_still_replays(tmp_path):
    """Toy-world logs keep the legacy path: record/verify stays coherent."""
    ctx = EventContext(SEED, mode="record", path=tmp_path / "a.jsonl.gz",
                       physics_build="0.1")
    a = ctx.draws(1, "collide", cell=0, n=5)
    ctx.finish("deadbeef")
    ctx2 = EventContext(SEED, mode="verify", verify_path=tmp_path / "a.jsonl.gz",
                        physics_build="0.1")
    b = ctx2.draws(1, "collide", cell=0, n=5)
    assert np.array_equal(a, b)
    ctx2.finish("deadbeef")


# --- separately declared statistical battery (no independence claims) ---------

def _chi2_p_uniform(samples, bins=16, n=1 << 14):
    edges = np.linspace(0.0, 1.0, bins + 1)
    obs, _ = np.histogram(samples, bins=edges)
    exp = n / bins
    z2 = float(np.sum((obs - exp) ** 2 / exp))
    # Wilson-Hilferty upper-tail approximation for df = bins - 1
    df = bins - 1
    t = (z2 / df) ** (1.0 / 3.0)
    z = (t - (1.0 - 2.0 / (9.0 * df))) / np.sqrt(2.0 / (9.0 * df))
    return 0.5 * float(math.erfc(z / np.sqrt(2.0)))


def test_statistical_battery_per_stream():
    """Within-stream uniformity for a sample of streams; this battery does
    NOT assert cross-stream independence and unique coordinates do not
    prove it (collision assumptions live in the ADR)."""
    means, variances, ps = [], [], []
    for k in range(8):
        v = rng.draws_at(EH + k, 100 + k, k, k * 7, SEED, 1 << 14)
        assert v.min() >= 0.0 and v.max() < 1.0
        means.append(v.mean())
        variances.append(v.var())
        ps.append(_chi2_p_uniform(v))
        assert len(np.unique(v)) == len(v)
    assert abs(np.mean(means) - 0.5) < 0.005
    assert abs(np.mean(variances) - 1 / 12) < 0.002
    assert min(ps) > 0.001


def test_disjoint_offsets_never_share_generator_inputs():
    """splitmix64 is a bijection: [base, base+n) windows of one stream and a
    second stream with a different base are disjoint unless the truncated
    sha256 bases collide (~2^-64 per pair)."""
    a = rng.draws_at(EH, 1, 2, 3, SEED, 4096)
    b = rng.draws_at(EH + 1, 1, 2, 3, SEED, 4096)
    tail = rng.draws_at(EH, 1, 2, 3, SEED, 1024, offset=4096)
    assert not (set(a.tolist()) & set(tail.tolist()))
    assert not (set(a.tolist()) & set(b.tolist()))
