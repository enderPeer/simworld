"""Versioned run manifests and replay compatibility preflight (D0-02).

A run manifest records the execution identity alongside the run directory:
model label, per-dimension schema versions, run configuration, constants
digest, source revision and runtime environment. Preflight compares a
recorded manifest with the code that is about to replay it and fails before
a world is allocated, so a changed constant, source tree, schema or runtime
under an unchanged physics label cannot silently re-execute history.

Identity is a set of independent dimensions (ADR-D0-01): the physics_build
label alone never implies compatibility. Informational fields (timestamps,
platform strings, paths) must never enter RNG coordinates or canonical state
hashes; the semantic digest covers everything else.

Historical runs recorded before manifests existed (physics build 0.1 with no
manifest.json) are rejected with archived-source reproduction instructions;
no guessed migration is performed.
"""

import hashlib
import json
import platform as _platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from . import constants as C

RUN_MANIFEST_SCHEMA = "run-manifest/0.1"
LOG_SCHEMA = "0.2"
CURRENT_SCHEMAS = {
    "log": LOG_SCHEMA,
    "rng": "0.2",
    "state": "0.1",
    "events": "0.1",
    "manifest": RUN_MANIFEST_SCHEMA,
}
NUMERIC_POLICY = {
    "dtype": "float64",
    "byte_order": "native",
    "rng_scheme": "splitmix64-fnv1a-0.1",
    "addressing": "logical-0.2",
}
LEGACY_INSTRUCTION = (
    "run has no manifest.json: it predates run manifests (log schema "
    "0.1-legacy). Reproduce it only in the archived source environment: "
    "checkout commit 2a74160e5934fe76b8e14726d78ba6e2c3c7d40f (or extract "
    "website/dist/downloads/SimWorld_Current_Source.zip) on Python 3.11.9 / "
    "NumPy 2.4.6 and run python -m sim.replay there; this build will not "
    "guess a migration"
)

_SEMANTIC_FIELDS = ("schema_version", "physics_build", "schemas", "config", "identity")


class ManifestError(RuntimeError):
    """Manifest is malformed, unsupported or incompatible with this build."""


def _repo_root():
    return Path(__file__).resolve().parent.parent


SCHEMA_PATH = _repo_root() / "spec" / "run-manifest.schema.json"


def schema_document():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def constants_digest():
    path = Path(__file__).with_name("constants.py")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args):
    try:
        proc = subprocess.run(
            ["git", *args], cwd=_repo_root(), capture_output=True, text=True)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def source_block():
    commit = _git("rev-parse", "HEAD")
    sim_tree = _git("rev-parse", "HEAD:sim")
    if commit is None or sim_tree is None:
        return {"available": False}
    return {"available": True, "commit": commit, "sim_tree": sim_tree}


def environment_block():
    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "numeric_policy": dict(NUMERIC_POLICY),
    }


def build_config(seed, ticks, cells, hash_every, probe_cells, jump):
    return {
        "seed": int(seed),
        "ticks": int(ticks),
        "cells": int(cells),
        "hash_every": int(hash_every),
        "probe_cells": sorted({int(c) for c in probe_cells}),
        "jump": bool(jump),
    }


def build(config):
    return {
        "schema_version": RUN_MANIFEST_SCHEMA,
        "physics_build": C.PHYSICS_BUILD,
        "schemas": dict(CURRENT_SCHEMAS),
        "config": dict(config),
        "identity": {
            "constants_digest": constants_digest(),
            "source": source_block(),
            "environment": environment_block(),
        },
        "informational": {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "platform": _platform.platform(),
        },
    }


def canonical_semantic(manifest):
    subset = {field: manifest[field] for field in _SEMANTIC_FIELDS if field in manifest}
    return json.dumps(subset, sort_keys=True, separators=(",", ":"))


def semantic_digest(manifest):
    return hashlib.sha256(canonical_semantic(manifest).encode("utf-8")).hexdigest()


def _check_type(problems, value, name, expected_type):
    if expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            problems.append(f"{name} must be an integer")
            return False
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            problems.append(f"{name} must be a boolean")
            return False
    elif expected_type == "string":
        if not isinstance(value, str) or not value:
            problems.append(f"{name} must be a non-empty string")
            return False
    elif expected_type == "object":
        if not isinstance(value, dict):
            problems.append(f"{name} must be an object")
            return False
    elif expected_type == "array":
        if not isinstance(value, list):
            problems.append(f"{name} must be an array")
            return False
    return True


def validate(manifest):
    """Validate structure and self-consistency against the schema document."""
    if not isinstance(manifest, dict):
        raise ManifestError("manifest must be an object")
    doc = schema_document()
    problems = []
    for field in doc["required"]:
        if field not in manifest:
            problems.append(f"missing required field {field!r}")
    props = doc.get("properties", {})

    def walk(prefix, node, subspec):
        for field in subspec.get("required", []):
            if field not in node:
                problems.append(f"missing {prefix}{field}")
        for field, spec in subspec.get("properties", {}).items():
            if field not in node:
                continue
            value = node[field]
            expected = spec.get("type")
            if not _check_type(problems, value, f"{prefix}{field}", expected):
                continue
            if isinstance(spec.get("minimum"), int) and value < spec["minimum"]:
                problems.append(f"{prefix}{field} must be >= {spec['minimum']}")
            if "required" in spec:
                walk(f"{prefix}{field}.", value, spec)
            if expected == "array" and subspec_type(spec, "items"):
                for item in value:
                    _check_type(problems, item, f"{prefix}{field}[]",
                                subspec_type(spec, "items"))

    for field in ("schemas", "config", "identity", "informational"):
        if field in manifest and isinstance(manifest[field], dict):
            walk(f"{field}.", manifest[field], props.get(field, {}))

    schemas = manifest.get("schemas")
    if isinstance(schemas, dict):
        supported = set(doc.get("x_supported_manifest_schema_versions", []))
        if manifest.get("schema_version") not in supported:
            problems.append(
                f"unsupported manifest schema_version {manifest.get('schema_version')!r}")
        for key, value in schemas.items():
            if not isinstance(value, str) or not value:
                problems.append(f"schemas.{key} must be a non-empty string")
    config = manifest.get("config")
    if isinstance(config, dict):
        cells = config.get("cells")
        if isinstance(cells, int) and cells >= 1:
            for cell in config.get("probe_cells", []):
                if not isinstance(cell, int) or not 0 <= cell < cells:
                    problems.append(
                        f"probe cell {cell!r} outside 0..{cells - 1}: contradictory configuration")
        if isinstance(config.get("probe_cells"), list) and \
                config["probe_cells"] != sorted(set(config["probe_cells"])):
            problems.append("probe_cells must be sorted and free of duplicates")
    identity = manifest.get("identity")
    if isinstance(identity, dict):
        digest = identity.get("constants_digest")
        if not (isinstance(digest, str) and len(digest) == 64
                and all(c in "0123456789abcdef" for c in digest)):
            problems.append("identity.constants_digest must be a sha256 hex digest")
        source = identity.get("source")
        if isinstance(source, dict) and source.get("available"):
            for key in ("commit", "sim_tree"):
                if not isinstance(source.get(key), str) or not source[key]:
                    problems.append(f"identity.source.{key} required when source is available")
    if problems:
        raise ManifestError("invalid run manifest: " + "; ".join(problems))
    return manifest


def subspec_type(spec, key):
    items = spec.get("items")
    return items.get("type") if isinstance(items, dict) else None


def write_manifest(path, manifest):
    validate(manifest)
    Path(path).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return manifest


def read_manifest(path):
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ManifestError(f"cannot read run manifest {path}: {exc}") from exc
    return validate(raw)


def preflight(recorded):
    """Compatibility check against this build; raises before world allocation.

    Every identity dimension that exact replay depends on is compared
    explicitly. A mismatch means this code is not the environment that made
    the recording: reject, never adapt silently.
    """
    validate(recorded)
    problems = []
    if recorded["physics_build"] != C.PHYSICS_BUILD:
        problems.append(
            f"physics_build {recorded['physics_build']!r} != code {C.PHYSICS_BUILD!r}")
    for dimension, current in CURRENT_SCHEMAS.items():
        recorded_value = recorded["schemas"].get(dimension)
        if recorded_value != current:
            problems.append(
                f"schemas.{dimension} {recorded_value!r} not supported by this build "
                f"(expects {current!r}); replay in the archived source environment instead")
    identity = recorded["identity"]
    if identity["constants_digest"] != constants_digest():
        problems.append(
            "constants digest differs from the current sim/constants.py: a behavior-"
            "relevant constant changed while the physics label stayed "
            f"{recorded['physics_build']!r}; that requires a new identity, not this replay")
    environment = identity["environment"]
    current_environment = environment_block()
    for key in ("python", "numpy"):
        if environment.get(key) != current_environment[key]:
            problems.append(
                f"runtime {key} {environment.get(key)!r} != current "
                f"{current_environment[key]!r} (exact replay is environment-scoped)")
    if environment.get("numeric_policy") != current_environment["numeric_policy"]:
        problems.append("numeric policy differs from the current build")
    source = identity["source"]
    if source.get("available"):
        current_source = source_block()
        if current_source.get("available"):
            if source.get("sim_tree") != current_source["sim_tree"]:
                problems.append(
                    "sim/ source tree differs from the recorded revision "
                    f"{source.get('commit', '?')}: replay the recorded commit instead")
    if problems:
        raise ManifestError("preflight failed: " + "; ".join(problems))
    return True
