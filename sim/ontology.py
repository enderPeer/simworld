"""Machine-readable event ontology (D0-03, closes the foundation for S25).

spec/ontology.json registers every event kind implemented in physics build
0.1 with a stable semantic ID, payload contract, producer ownership and
draw-versus-log-only role. Identity comes from declaration: it never derives
from dict order, call order or wall-clock time. The registry is bound into
run manifests through schemas.events (see sim/manifest.py).

The serialized log identity in 0.1-legacy and 0.2 logs remains the legacy
truncated kind hash (legacy_0_1 in the registry); stable_hash is registry-side
identity for future addressing (D0-04), not a retrofitted claim about old logs.
"""

import importlib
import json
import re
from pathlib import Path

from . import constants as C
from . import rng
from .manifest import CURRENT_SCHEMAS

ONTOLOGY_SCHEMA = "event-ontology/0.1"
EVENTS_SCHEMA = CURRENT_SCHEMAS["events"]
ONTOLOGY_PATH = Path(__file__).resolve().parents[1] / "spec" / "ontology.json"

_SEMANTIC_ID = re.compile(r"^(draw|log_only)\.([a-z_]+)@([1-9][0-9]*)(/([a-z_]+))?$")
_PRODUCER = re.compile(r"^sim/([a-z_]+)\.py:([A-Za-z_][A-Za-z0-9_]*)$")
_EVENT_REQUIRED = ("semantic_id", "stable_hash", "name", "kind_id", "role",
                   "schema_version", "producer", "sub_lane", "causes",
                   "q_fields", "payload_fields")
_TOP_REQUIRED = ("schema", "registry_version", "manifest_binding",
                 "introduced_by_ticket", "s25_closure", "roles",
                 "identity_model", "events", "extension", "legacy_0_1")


class OntologyError(RuntimeError):
    """The registry is malformed, inconsistent or fabricates unimplemented kinds."""


def canonical_identity(event):
    lane = event.get("lane") or event.get("lane_or_dash") or _lane(event["semantic_id"])
    return (f"{event['name']}|{event['role']}|{event['kind_id']}"
            f"|{event['schema_version']}|{lane or '-'}")


def stable_hash(event):
    return rng.fnv1a64(canonical_identity(event).encode("utf-8"))


def _lane(semantic_id):
    return semantic_id.split("/", 1)[1] if "/" in semantic_id else None


def load(path=None):
    doc = json.loads(Path(path or ONTOLOGY_PATH).read_text(encoding="utf-8"))
    validate(doc)
    return doc


_REGISTRY_INDEX = None


def registry_identity_index():
    """semantic_id -> stable_hash, loaded once per process."""
    global _REGISTRY_INDEX
    if _REGISTRY_INDEX is None:
        _REGISTRY_INDEX = identity_map(load())
    return _REGISTRY_INDEX


def identity_map(doc):
    """semantic_id -> stable_hash, built from sorted ids (order-independent)."""
    by_id = {event["semantic_id"]: event for event in doc["events"]}
    if len(by_id) != len(doc["events"]):
        raise OntologyError("duplicate semantic_id in registry")
    return {sid: stable_hash(by_id[sid]) for sid in sorted(by_id)}


def engine_kinds():
    kinds = {name: ("draw", kind_id) for name, kind_id in C.KIND_IDS.items()}
    kinds.update((name, ("log_only", kind_id))
                 for name, kind_id in rng.LOG_KIND_IDS.items())
    return kinds


def _check_event(problems, event, engine, reserved):
    if not isinstance(event, dict):
        problems.append("event must be an object")
        return
    missing = [f for f in _EVENT_REQUIRED if f not in event]
    if missing:
        problems.append(f"event {event.get('semantic_id', '?')} missing {missing}")
        return
    sid = event["semantic_id"]
    match = _SEMANTIC_ID.match(sid)
    if not match:
        problems.append(f"semantic_id {sid!r} violates the registry format")
    else:
        if match.group(2) != event["name"]:
            problems.append(f"{sid}: embedded name != name {event['name']!r}")
        if int(match.group(3)) != event["schema_version"]:
            problems.append(f"{sid}: embedded schema_version != {event['schema_version']}")
    if event["role"] not in ("draw", "log_only"):
        problems.append(f"{sid}: unknown role {event['role']!r}")
        return
    if event["role"] == "log_only" and _lane(sid) is not None:
        problems.append(f"{sid}: log_only events are unlaned (one producer per kind)")
    kind_id = event["kind_id"]
    if not isinstance(kind_id, int) or not 0 <= kind_id <= 0xFFFF:
        problems.append(f"{sid}: kind_id must be a u16 integer")
    if event.get("name") in reserved:
        problems.append(f"{sid}: kind {event.get('name')!r} is legacy-reserved "
                        "without a producer and must not be registered as an event")
    if event["name"] not in engine:
        problems.append(f"{sid}: kind {event['name']!r} is not implemented in this build")
    else:
        want_role, want_id = engine[event["name"]]
        if event["role"] != want_role:
            problems.append(f"{sid}: role {event['role']!r} != engine role {want_role!r}")
        if kind_id != want_id:
            problems.append(f"{sid}: kind_id {kind_id} != engine id {want_id}")
    producer = event["producer"]
    if event["role"] == "draw" and not producer:
        problems.append(f"{sid}: draw event without registered producer")
        return
    match = _PRODUCER.match(producer or "")
    if not match:
        problems.append(f"{sid}: producer {producer!r} must be sim/<module>.py:<function>")
    else:
        module_name, func_name = match.groups()
        if not (Path(__file__).resolve().parent / f"{module_name}.py").is_file():
            problems.append(f"{sid}: producer module sim/{module_name}.py does not exist")
        else:
            module = importlib.import_module(f"sim.{module_name}")
            if not callable(getattr(module, func_name, None)):
                problems.append(f"{sid}: producer sim/{module_name}.{func_name} not callable")
    for field in ("causes", "q_fields", "payload_fields"):
        value = event[field]
        if not isinstance(value, list) or any(not isinstance(x, str) or not x
                                              for x in value):
            problems.append(f"{sid}: {field} must be a list of non-empty strings")
    if not event["causes"]:
        problems.append(f"{sid}: causes must not be empty")
    if event["stable_hash"] != stable_hash(event):
        problems.append(f"{sid}: stable_hash does not match the canonical identity")


def validate(doc):
    problems = []
    if not isinstance(doc, dict):
        raise OntologyError("registry must be an object")
    missing = [f for f in _TOP_REQUIRED if f not in doc]
    if missing:
        raise OntologyError(f"registry missing top-level fields {missing}")
    if doc["schema"] != ONTOLOGY_SCHEMA:
        raise OntologyError(f"unsupported registry schema {doc['schema']!r}")
    if doc["registry_version"] != EVENTS_SCHEMA:
        problems.append(f"registry_version {doc['registry_version']!r} != manifest "
                        f"schemas.events {EVENTS_SCHEMA!r}")
    if doc["manifest_binding"] != "schemas.events":
        problems.append("manifest_binding must be 'schemas.events'")
    if doc["s25_closure"] != "partial_foundation":
        problems.append("S25 closure must be 'partial_foundation' in 0.1 "
                        "(the registry is foundation work, not a global close)")
    engine = engine_kinds()
    legacy = doc["legacy_0_1"]
    reserved = legacy.get("reserved_kind_ids_without_producer", {})
    if legacy.get("registry_identity_present_in_serialized_logs"):
        problems.append("legacy policy may not claim registry IDs in serialized logs")
    for name, kind_id in reserved.items():
        if engine.get(name, (None, None))[1] != kind_id:
            problems.append(f"legacy reserved {name!r}/{kind_id} != engine id")
    seen_ids = set()
    seen_lanes = set()
    kind_roles = {}
    for event in doc["events"]:
        _check_event(problems, event, engine, reserved)
        if not isinstance(event, dict):
            continue
        sid = event.get("semantic_id")
        if sid in seen_ids:
            problems.append(f"duplicate semantic_id {sid!r}")
        seen_ids.add(sid)
        lane = _lane(sid) if isinstance(sid, str) else None
        key = (event.get("name"), lane)
        if key in seen_lanes:
            problems.append(f"duplicate (name, lane) {key!r} at {sid!r}")
        seen_lanes.add(key)
        kind = event.get("kind_id")
        role = event.get("role")
        if kind_roles.setdefault(kind, role) != role:
            problems.append(f"kind_id {kind} used by roles {kind_roles[kind]!r} "
                            f"and {role!r}")
    registered_names = {e.get("name") for e in doc["events"] if isinstance(e, dict)}
    missing_kinds = sorted(name for name in engine
                           if name not in registered_names and name not in reserved)
    if missing_kinds:
        problems.append(f"engine kinds without a registered event: {missing_kinds}")
    next_id = doc["extension"].get("next_kind_id")
    used = [e.get("kind_id") for e in doc["events"] if isinstance(e, dict)]
    if not isinstance(next_id, int) or used and next_id <= max(
            [k for k in used if isinstance(k, int)] + list(reserved.values())):
        problems.append("extension.next_kind_id must exceed every registered and reserved id")
    if problems:
        raise OntologyError("invalid event registry: " + "; ".join(problems))


def classify_entry_kind(entry, doc):
    """Identify how a serialized log entry encodes its kind.

    Returns ("legacy_truncated_hash", name) when the u16 field matches the
    legacy hash of a registered kind id, else ("unknown", None). Registry
    stable_hash never appears in serialized entries.
    """
    value = entry.get("kind")
    if not isinstance(value, int):
        return "unknown", None
    for event in doc["events"]:
        if (rng.entry_kind_hash(event["name"]) & 0xFFFF) == (value & 0xFFFF):
            return "legacy_truncated_hash", event["name"]
    return "unknown", None
