"""D0-02: run manifest round trip, validation, preflight and legacy policy.

Candidate controls added under a new test name per the ADR-D0-01 scope
policy; they exercise sim/manifest.py, the log 0.2 header binding and the
replay compatibility preflight without altering any 0.1 test.
"""

import gzip
import json
import shutil

import pytest

from sim import constants as C
from sim import manifest as M
from sim.demo import run_recorded
from sim.log import EventContext, LogError
from sim.manifest import ManifestError
from sim.replay import replay_dir

TICKS = 240
CELLS = 8


def base():
    return M.build(M.build_config(7, 100, 4, 50, [1, 3], True))


@pytest.fixture(scope="module")
def run_dir(tmp_path_factory):
    out = tmp_path_factory.mktemp("run") / "manifested"
    run_recorded(42, TICKS, CELLS, out)
    return out


def test_manifest_round_trip_preserves_semantic_fields(tmp_path):
    manifest = base()
    path = tmp_path / "manifest.json"
    M.write_manifest(path, manifest)
    assert json.loads(path.read_text(encoding="utf-8")) == manifest
    back = M.read_manifest(path)
    assert M.canonical_semantic(back) == M.canonical_semantic(manifest)
    assert M.semantic_digest(back) == M.semantic_digest(manifest)


def test_missing_required_fields_rejected():
    for drop in (("config", "seed"), ("config", "ticks"), ("config", "probe_cells"),
                 ("config", "jump"), ("identity", "constants_digest"),
                 ("schemas", "manifest")):
        manifest = base()
        del manifest[drop[0]][drop[1]]
        with pytest.raises(ManifestError):
            M.validate(manifest)
    manifest = base()
    del manifest["physics_build"]
    with pytest.raises(ManifestError):
        M.validate(manifest)


def test_unsupported_schema_versions_rejected():
    manifest = base()
    manifest["schema_version"] = "run-manifest/9.9"
    with pytest.raises(ManifestError):
        M.validate(manifest)
    manifest = base()
    manifest["schemas"]["rng"] = "9.9"
    with pytest.raises(ManifestError):
        M.preflight(manifest)
    manifest = base()
    manifest["schemas"]["log"] = "0.1-legacy"
    with pytest.raises(ManifestError):
        M.preflight(manifest)


def test_contradictory_configuration_rejected():
    for field, bad in (("ticks", 0), ("ticks", -5), ("cells", 0), ("seed", 1.5),
                       ("jump", "yes"), ("hash_every", 0)):
        config = M.build_config(7, 100, 4, 50, [1, 3], True)
        config[field] = bad
        with pytest.raises(ManifestError):
            M.validate(M.build(config))
    config = M.build_config(7, 100, 4, 50, [1], True)
    config["probe_cells"] = [3, 1]
    with pytest.raises(ManifestError):
        M.validate(M.build(config))
    manifest = base()
    manifest["config"]["cells"] = 2
    with pytest.raises(ManifestError):  # probe cells 1,3 outside 0..1
        M.validate(manifest)


def test_preflight_accepts_current_recording(run_dir):
    recorded = M.read_manifest(run_dir / "manifest.json")
    assert M.preflight(recorded) is True


def _poisoned_copy(run_dir, tmp_path, name):
    copy = tmp_path / name
    shutil.copytree(run_dir, copy)
    path = copy / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return copy, manifest, path


def test_preflight_fails_before_simulation_on_constant_drift(run_dir, tmp_path, monkeypatch):
    copy, manifest, path = _poisoned_copy(run_dir, tmp_path, "const")
    manifest["identity"]["constants_digest"] = "0" * 64  # old label, changed constants
    path.write_text(json.dumps(manifest), encoding="utf-8")

    def _never(*args, **kwargs):
        raise AssertionError("preflight must fail before world allocation")

    monkeypatch.setattr("sim.replay.run", _never)
    with pytest.raises(LogError, match="constants"):
        replay_dir(copy)


def test_preflight_fails_on_runtime_fingerprint(run_dir, tmp_path, monkeypatch):
    copy, manifest, path = _poisoned_copy(run_dir, tmp_path, "runtime")
    manifest["identity"]["environment"]["numpy"] = "9.9.9"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    def _never(*args, **kwargs):
        raise AssertionError("preflight must fail before world allocation")

    monkeypatch.setattr("sim.replay.run", _never)
    with pytest.raises(LogError, match="numpy"):
        replay_dir(copy)


def test_preflight_fails_on_physics_label_change(run_dir, tmp_path):
    copy, manifest, path = _poisoned_copy(run_dir, tmp_path, "label")
    manifest["physics_build"] = "0.9"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(LogError, match="physics_build"):
        replay_dir(copy)


def test_replay_detects_manifest_log_contradiction(run_dir, tmp_path):
    copy, manifest, path = _poisoned_copy(run_dir, tmp_path, "binding")
    manifest["config"]["seed"] += 1  # semantic change rehashes the manifest
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(LogError):
        replay_dir(copy)


def test_log_binding_rejects_digest_mismatch(run_dir):
    with gzip.open(run_dir / "run.jsonl.gz", "rt", encoding="utf-8") as fh:
        header = json.loads(fh.readline())
    assert header.get("log_schema") == M.LOG_SCHEMA
    assert header.get("manifest_digest") == M.semantic_digest(
        M.read_manifest(run_dir / "manifest.json"))
    with pytest.raises(LogError, match="manifest_digest"):
        EventContext(header["seed"], mode="verify",
                     verify_path=run_dir / "run.jsonl.gz",
                     physics_build=C.PHYSICS_BUILD, meta=header["meta"],
                     log_schema=M.LOG_SCHEMA, manifest_digest="f" * 64)


def test_legacy_run_without_manifest_is_rejected(run_dir, tmp_path):
    copy, _manifest, path = _poisoned_copy(run_dir, tmp_path, "legacy")
    path.unlink()
    with pytest.raises(LogError, match="archived source"):
        replay_dir(copy)


def test_informational_fields_never_enter_semantic_identity(tmp_path):
    first = tmp_path / "run-a"
    second = tmp_path / "deeper\\elsewhere\\run-b"
    summary_a = run_recorded(42, TICKS, CELLS, first)
    summary_b = run_recorded(42, TICKS, CELLS, second)
    assert summary_a["final_hash"] == summary_b["final_hash"]
    manifest_a = M.read_manifest(first / "manifest.json")
    manifest_b = M.read_manifest(second / "manifest.json")
    assert M.semantic_digest(manifest_a) == M.semantic_digest(manifest_b)
    manifest_b["informational"]["created_utc"] = "2000-01-01T00:00:00+00:00"
    manifest_b["informational"]["platform"] = "somewhere else"
    assert M.semantic_digest(manifest_b) == M.semantic_digest(manifest_a)


def test_manifest_written_before_simulation(tmp_path, monkeypatch):
    class Boom(Exception):
        pass

    def _boom(*args, **kwargs):
        raise Boom

    monkeypatch.setattr("sim.demo.run", _boom)
    out = tmp_path / "order"
    with pytest.raises(Boom):
        run_recorded(1, 10, 2, out)
    assert (out / "manifest.json").is_file()
