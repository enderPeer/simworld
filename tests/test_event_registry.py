"""D0-03 candidate controls: event registry validation and identity stability."""

import copy
import gzip
import importlib
import json
import random

import pytest

from sim import ontology as O
from sim import rng
from sim.demo import run_recorded
from sim.manifest import ManifestError
from sim.ontology import OntologyError, stable_hash


def _tampered(mutate):
    doc = O.load()
    mutate(doc)
    with pytest.raises(OntologyError):
        O.validate(doc)


def _drop_event(doc, semantic_id):
    doc["events"] = [e for e in doc["events"] if e["semantic_id"] != semantic_id]


def test_clean_registry_validates():
    doc = O.load()
    assert len(doc["events"]) == 9
    assert doc["registry_version"] == O.EVENTS_SCHEMA


def test_duplicate_semantic_id_rejected():
    def mutate(doc):
        doc["events"].append(copy.deepcopy(doc["events"][0]))

    _tampered(mutate)


def test_duplicate_name_and_lane_rejected():
    def mutate(doc):
        dup = copy.deepcopy(doc["events"][1])
        dup["semantic_id"] = "draw.react@2/weak"
        dup["schema_version"] = 2
        doc["events"].append(dup)

    _tampered(mutate)


def test_conflicting_name_in_semantic_id_rejected():
    def mutate(doc):
        for event in doc["events"]:
            if event["semantic_id"] == "draw.condense@1":
                event["name"] = "evaporate"

    _tampered(mutate)


def test_missing_required_field_rejected():
    def mutate(doc):
        doc["events"][0].pop("payload_fields")

    _tampered(mutate)


def test_unregistered_producer_rejected():
    def mutate(doc):
        doc["events"][0]["producer"] = "sim/nonexistent_module.py:run"

    _tampered(mutate)


def test_producer_function_not_callable_rejected():
    def mutate(doc):
        doc["events"][0]["producer"] = "sim/demo.py:_np_ratio_missing"

    _tampered(mutate)


def test_unimplemented_kind_fabrication_rejected():
    def mutate(doc):
        doc["events"].append({
            "semantic_id": "draw.bc@1", "stable_hash": 0, "name": "bc",
            "kind_id": 7, "role": "draw", "schema_version": 1,
            "producer": "sim/demo.py:run", "sub_lane": None,
            "causes": ["boundary"], "q_fields": [], "payload_fields": [],
        })

    _tampered(mutate)


def test_legacy_reserved_kind_cannot_be_registered():
    def mutate(doc):
        doc["events"].append({
            "semantic_id": "draw.collide@1", "stable_hash": 0, "name": "collide",
            "kind_id": 1, "role": "draw", "schema_version": 1,
            "producer": "sim/demo.py:run", "sub_lane": None,
            "causes": ["thermal"], "q_fields": [], "payload_fields": [],
        })

    _tampered(mutate)


def test_registered_kind_must_not_go_unregistered():
    doc = O.load()
    _drop_event(doc, "log_only.jump@1")
    with pytest.raises(OntologyError, match="without a registered event"):
        O.validate(doc)


def test_role_conflict_on_kind_id_rejected():
    def mutate(doc):
        for event in doc["events"]:
            if event["semantic_id"] == "log_only.jump@1":
                event["kind_id"] = 2

    _tampered(mutate)


def test_stable_hash_must_match_canonical_identity():
    def mutate(doc):
        doc["events"][0]["stable_hash"] += 1

    _tampered(mutate)


def test_identity_survives_cache_regeneration_and_reenumeration():
    doc = O.load()
    baseline = O.identity_map(doc)
    reloaded = importlib.reload(importlib.import_module("sim.ontology"))
    assert reloaded.identity_map(reloaded.load()) == baseline

    shuffled = copy.deepcopy(doc)
    random.Random(2026).shuffle(shuffled["events"])
    lanes = {}
    for event in shuffled["events"]:
        if event["role"] == "draw" and event["name"] == "react":
            lanes[event["semantic_id"]] = event["sub_lane"]
    renumbered = dict(zip(sorted(lanes), sorted(lanes, reverse=True)))
    for event in shuffled["events"]:
        if event["semantic_id"] in renumbered:
            event["sub_lane"] = renumbered[event["semantic_id"]]
    O.validate(shuffled)
    assert O.identity_map(shuffled) == baseline


def test_manifest_binds_registry_version():
    from sim import manifest as M

    manifest = M.build(M.build_config(3, 5, 2, 2, [1], True))
    assert manifest["schemas"]["events"] == O.EVENTS_SCHEMA
    M.preflight(manifest)
    manifest["schemas"]["events"] = "0.9"
    with pytest.raises(ManifestError, match="events"):
        M.preflight(manifest)


def test_legacy_truncated_hash_identified_separately(tmp_path):
    doc = O.load()
    out = tmp_path / "legacy"
    summary = run_recorded(11, 40, 3, out)
    with gzip.open(out / "run.jsonl.gz", "rt", encoding="utf-8") as fh:
        entries = [json.loads(line) for line in fh if line.strip()]
    body = [e for e in entries if e.get("k") not in ("header", "end")]
    assert body
    stable_ids = {e["stable_hash"] for e in doc["events"]}
    for entry in body:
        classification, name = O.classify_entry_kind(entry, doc)
        if entry["k"] == "condense":
            assert classification == "legacy_truncated_hash"
            assert name == "condense"
        assert entry.get("kind") not in stable_ids
    assert doc["legacy_0_1"]["registry_identity_present_in_serialized_logs"] is False
    assert set(doc["legacy_0_1"]["applies_to_log_schemas"]) == {"0.1-legacy", "0.2"}
    assert summary["final_hash"]


def test_registry_contains_only_implemented_kinds():
    doc = O.load()
    engine = O.engine_kinds()
    assert {e["name"] for e in doc["events"]} <= set(engine)
    assert doc["extension"]["reserved_for_future_phases"].startswith("none")
    assert doc["s25_closure"] == "partial_foundation"
