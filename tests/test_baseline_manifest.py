"""D0-01 baseline manifest and test-scope checks.

Deterministic identity validation only: verifies fingerprints of preserved
artifacts and the frozen source trees without re-running the universe, and
enforces the ADR-D0-01 test-scope policy. See spec/baselines/physics-0.1.json.
"""

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "spec" / "baselines" / "physics-0.1.json"
CANDIDATE_PATH = ROOT / "spec" / "baselines" / "candidate.json"
SCOPE_PATH = ROOT / "spec" / "test-scope.json"
STATUS_PATH = ROOT / "spec" / "status.json"
BACKLOG_PATH = ROOT / "spec" / "development_backlog.json"

VALID_CLASSES = {"shared_invariant", "characterization_0_1", "model_validation"}
REQUIRED_TOP_FIELDS = {
    "schema_version",
    "physics_build",
    "status",
    "recorded",
    "source",
    "environment",
    "schemas",
    "model_claim_scope",
    "known_defects",
    "artifacts",
    "reproduction",
}
ARTIFACT_FIELDS = {"path", "role", "sha256", "bytes"}


class ManifestError(Exception):
    """Raised when the manifest does not resolve against the repository."""


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_of(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def verify_manifest(manifest, root=ROOT):
    """Validate every artifact fingerprint; raise ManifestError on any drift."""
    checked = []
    for artifact in manifest.get("artifacts", []):
        missing = ARTIFACT_FIELDS - set(artifact)
        if missing:
            raise ManifestError(f"artifact {artifact.get('path')} missing {sorted(missing)}")
        path = root / artifact["path"]
        if not path.is_file():
            raise ManifestError(f"artifact missing on disk: {artifact['path']}")
        if path.stat().st_size != artifact["bytes"]:
            raise ManifestError(f"size drift for {artifact['path']}")
        if sha256_of(path) != artifact["sha256"].upper():
            raise ManifestError(f"hash drift for {artifact['path']}")
        checked.append(artifact["path"])
    return checked


def git_tree(rev, subpath):
    proc = subprocess.run(
        ["git", "rev-parse", f"{rev}:{subpath}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise FileNotFoundError(proc.stderr.strip())
    return proc.stdout.strip()


def collected_test_ids():
    proc = subprocess.run(
        ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--collect-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout + proc.stderr)
    return {line.strip() for line in proc.stdout.splitlines() if "::" in line}


def test_manifest_has_required_identity_fields():
    manifest = load_json(MANIFEST_PATH)
    assert REQUIRED_TOP_FIELDS <= set(manifest), sorted(REQUIRED_TOP_FIELDS - set(manifest))
    assert manifest["physics_build"] == "0.1"
    assert manifest["status"] == "accepted_historical_micro_slice"
    commit = manifest["source"]["baseline_commit"]
    assert len(commit) == 40 and all(c in "0123456789abcdef" for c in commit)
    assert {"sim", "tests", "spikes"} <= set(manifest["source"]["engine_trees_at_baseline"])
    assert {"model", "log", "rng", "state"} <= set(manifest["schemas"])


def test_artifact_hashes_validate_without_rerun():
    manifest = load_json(MANIFEST_PATH)
    checked = verify_manifest(manifest)
    assert len(checked) == len(manifest["artifacts"]) >= 4
    roles = {a["role"] for a in manifest["artifacts"]}
    assert any(r.startswith("preserved 0.1 acceptance run") for r in roles)


def test_engine_trees_match_frozen_baseline():
    manifest = load_json(MANIFEST_PATH)
    commit = manifest["source"]["baseline_commit"]
    try:
        frozen_sim_tree = git_tree(commit, "sim")
    except FileNotFoundError:
        pytest.skip("git not available")
    for subpath, frozen in manifest["source"]["engine_trees_at_baseline"].items():
        assert git_tree(commit, subpath) == frozen, (
            f"the frozen baseline commit itself must remain immutable ({subpath})")
    head_sim_tree = git_tree("HEAD", "sim")
    if head_sim_tree != manifest["source"]["engine_trees_at_baseline"]["sim"]:
        candidate = load_json(CANDIDATE_PATH)
        assert candidate["sim_tree"] == head_sim_tree, (
            "HEAD drifted from the frozen 0.1 baseline without a registered "
            "candidate identity (ADR-D0-01)")
        assert candidate["physics_build"] == manifest["physics_build"], (
            "a candidate may not claim a new physics label before D0-12 acceptance")


def test_negative_tamper_is_rejected():
    manifest = load_json(MANIFEST_PATH)
    tampered_hash = json.loads(json.dumps(manifest))
    tampered_hash["artifacts"][0]["sha256"] = "0" * 64
    with pytest.raises(ManifestError):
        verify_manifest(tampered_hash)
    tampered_path = json.loads(json.dumps(manifest))
    tampered_path["artifacts"][0]["path"] = "website/dist/downloads/does-not-exist"
    with pytest.raises(ManifestError):
        verify_manifest(tampered_path)
    tampered_size = json.loads(json.dumps(manifest))
    tampered_size["artifacts"][0]["bytes"] += 1
    with pytest.raises(ManifestError):
        verify_manifest(tampered_size)
    missing_field = json.loads(json.dumps(manifest))
    del missing_field["artifacts"][0]["sha256"]
    with pytest.raises(ManifestError):
        verify_manifest(missing_field)


def test_known_defects_reference_audit_evidence_and_tickets():
    manifest = load_json(MANIFEST_PATH)
    ticket_ids = {t["id"] for t in load_json(BACKLOG_PATH)["starter_tickets"]}
    for defect in manifest["known_defects"]:
        assert {"id", "summary", "owner_ticket", "evidence"} <= set(defect)
        assert defect["owner_ticket"] in ticket_ids
        evidence_file = defect["evidence"].split(":", 1)[0]
        assert (ROOT / evidence_file).is_file(), evidence_file


def test_scope_covers_full_collection_with_valid_classes():
    scope = load_json(SCOPE_PATH)
    recorded = scope["tests"]
    assert set(recorded.values()) <= VALID_CLASSES
    counts = {}
    for klass in recorded.values():
        counts[klass] = counts.get(klass, 0) + 1
    assert counts == scope["counts"]
    collected = collected_test_ids()
    exempt = tuple(scope["scope_exempt_files"])
    unexpected = {
        node_id
        for node_id in collected
        if node_id not in recorded and not node_id.startswith(exempt)
    }
    assert not unexpected, f"uncategorized tests: {sorted(unexpected)}"
    missing = {node_id for node_id in recorded if node_id not in collected}
    assert not missing, f"recorded tests no longer collected: {sorted(missing)}"


def test_manifest_and_status_agree_on_physics_build():
    manifest = load_json(MANIFEST_PATH)
    status = load_json(STATUS_PATH)
    assert status["physics_build"] == manifest["physics_build"]
