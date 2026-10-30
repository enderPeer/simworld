#!/usr/bin/env python3
"""Check the development plan's structure, traceability and evidence references.

This is a documentation check, not acceptance of a model or its scientific claims.
Run with --check-sources when reviewing source drift; normal implementation can
change an input without silently rewriting this planning version's fingerprints.
"""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
TASK_STATES = {"planned", "ready", "blocked", "in_progress", "verified"}
GATE_STATES = {"unverified", "in_progress", "verified"}
PHASE_ZERO_IDS = {
    "P00-D1", "P00-D2", "P00-D3", "P00-D4", "P00-D5",
    "P00-SPIKE-A", "P00-SPIKE-B", "P00-BASELINE",
}


class PlanCheck:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def path(self, value: str, context: str, *, exists: bool = True) -> Path | None:
        """Require a portable repository path, never a path outside the repo."""
        if not isinstance(value, str) or not value:
            self.errors.append(f"{context}: expected a nonempty relative path")
            return None
        parts = PurePosixPath(value)
        if (parts.is_absolute() or ".." in parts.parts or "\\" in value
                or re.match(r"^[A-Za-z]:", value)):
            self.errors.append(f"{context}: unsafe or nonportable path {value!r}")
            return None
        target = (self.root / value).resolve()
        if not target.is_relative_to(self.root):
            self.errors.append(f"{context}: path escapes the repository: {value}")
            return None
        if exists:
            self.require(target.is_file(), f"{context}: missing file {value}")
        return target

    def evidence(self, record: dict, context: str, *, required: bool = False) -> None:
        """Evidence entries are links to reviewed records, not inline assertions."""
        entries = record.get("evidence", [])
        self.require(isinstance(entries, list), f"{context}: evidence must be a list")
        if not isinstance(entries, list):
            return
        if required:
            self.require(bool(entries), f"{context}: verified claims require evidence")
        for entry in entries:
            reference = entry if isinstance(entry, str) else entry.get("url", entry.get("path")) if isinstance(entry, dict) else None
            if not isinstance(reference, str) or not reference:
                self.errors.append(f"{context}: evidence must contain a path or HTTPS URL")
                continue
            parsed = urlsplit(reference)
            if parsed.scheme:
                self.require(parsed.scheme == "https" and bool(parsed.netloc),
                             f"{context}: invalid evidence URL {reference!r}")
            else:
                self.path(unquote(parsed.path), f"{context} evidence")

    def index(self, records: list[dict], key: str, context: str) -> dict:
        result = {}
        for record in records:
            identifier = record.get(key)
            self.require(identifier is not None, f"{context}: missing {key}")
            self.require(identifier not in result, f"{context}: duplicate {key} {identifier}")
            result[identifier] = record
        return result

    def dag(self, records: dict, dependency_key: str, context: str) -> None:
        """Validate dependency references and detect cycles without execution."""
        for identifier, record in records.items():
            dependencies = record.get(dependency_key, [])
            self.require(len(dependencies) == len(set(dependencies)),
                         f"{context} {identifier}: duplicate dependencies")
            for dependency in dependencies:
                self.require(dependency in records,
                             f"{context} {identifier}: unknown dependency {dependency}")
        visited, active = set(), []

        def visit(identifier):
            if identifier in active:
                cycle = active[active.index(identifier):] + [identifier]
                self.errors.append(f"{context}: dependency cycle: {' -> '.join(map(str, cycle))}")
                return
            if identifier in visited:
                return
            active.append(identifier)
            for dependency in records[identifier].get(dependency_key, []):
                if dependency in records:
                    visit(dependency)
            active.pop()
            visited.add(identifier)

        for identifier in records:
            visit(identifier)

    def task(self, record: dict, context: str) -> None:
        state = record.get("state")
        self.require(state in TASK_STATES, f"{context}: invalid task state {state!r}")
        self.evidence(record, context, required=state == "verified")

    def validate(self, backlog: dict, status: dict, sources: dict, markdown: str,
                 *, check_sources: bool = False) -> list[dict]:
        for name, document in (("backlog", backlog), ("status", status), ("sources", sources)):
            self.require(document.get("schema_version") == "1.0", f"{name}: unsupported schema_version")
            self.require(document.get("source_baseline") == backlog.get("source_baseline"),
                         f"{name}: source baseline differs from backlog")
        self.require(bool(re.fullmatch(r"[0-9a-f]{40}", backlog.get("source_baseline", ""))),
                     "backlog: source_baseline must be a full commit hash")
        self.require(backlog.get("planning_version") == status.get("planning_version"),
                     "status: planning_version differs from backlog")
        for name, value in (("backlog date", backlog.get("date")),
                            ("status as_of", status.get("as_of")),
                            ("source date", sources.get("date"))):
            try:
                date.fromisoformat(value)
            except (TypeError, ValueError):
                self.errors.append(f"{name}: expected an ISO date (YYYY-MM-DD)")

        tickets = self.index(backlog["starter_tickets"], "id", "starter tickets")
        milestones = self.index(backlog["milestones"], "id", "milestones")
        phases = self.index(backlog["phases"], "phase", "phases")
        phase_status = self.index(status["phases"], "phase", "phase status")
        seams = self.index(backlog["seams"], "id", "seams")
        self.require(set(tickets) == {f"D0-{i:02d}" for i in range(1, 13)}, "expected starter tickets D0-01 through D0-12")
        self.require(set(phases) == set(range(17)), "expected phases 0 through 16")
        self.require(set(phase_status) == set(phases), "status phase coverage differs from backlog")
        self.require(set(seams) == {f"S{i}" for i in range(1, 26)}, "expected seams S1 through S25")
        self.dag(tickets, "depends_on", "starter tickets")
        self.dag(milestones, "depends_on", "milestones")
        self.dag(phases, "integration_prerequisite_phases", "phase integration")
        for name, document in (("backlog", backlog), ("status", status)):
            self.require(document.get("first_milestone") in milestones,
                         f"{name}: unknown first_milestone")
        self.require(status.get("first_milestone") == backlog.get("first_milestone"),
                     "status: first_milestone differs from backlog")

        for identifier, milestone in milestones.items():
            self.task(milestone, f"milestone {identifier}")
            for number in milestone.get("phases", []):
                self.require(number in phases, f"milestone {identifier}: unknown phase {number}")
            if milestone.get("state") == "verified":
                self.require(all(milestones.get(dep, {}).get("state") == "verified" for dep in milestone.get("depends_on", [])),
                             f"milestone {identifier}: verified milestone has unverified dependencies")
        for identifier, ticket in tickets.items():
            self.task(ticket, identifier)
            self.require(ticket.get("milestone") in milestones, f"{identifier}: unknown milestone")
            for path in ticket.get("files_existing", []):
                self.path(path, f"{identifier} existing files")
            for path in ticket.get("files_new", []):
                self.path(path, f"{identifier} proposed files", exists=False)
            self.require(bool(ticket.get("acceptance")), f"{identifier}: missing acceptance criteria")
            self.require(bool(ticket.get("source_trace")), f"{identifier}: missing source trace")
            self.require(bool(ticket.get("validation_commands_after_implementation")), f"{identifier}: missing planned validation commands")
            self.require(ticket.get("commands_are_planned") is True,
                         f"{identifier}: proposed commands must be labeled as planned")
            if ticket.get("state") in {"ready", "in_progress", "verified"}:
                self.require(all(tickets.get(dep, {}).get("state") == "verified" for dep in ticket.get("depends_on", [])),
                             f"{identifier}: active/verified ticket has unverified dependencies")

        ready = [ticket for ticket in tickets.values()
                 if ticket.get("state") in {"planned", "ready", "blocked"}
                 and all(tickets.get(dep, {}).get("state") == "verified" for dep in ticket.get("depends_on", []))]
        ready_ids = [ticket["id"] for ticket in ready]
        for name, document in (("backlog", backlog), ("status", status)):
            self.require(document.get("ready_now") == ready_ids,
                         f"{name}: ready_now should be {ready_ids}")

        packages = []
        for number, phase in phases.items():
            label = f"phase {number}"
            source = self.path(phase.get("source_file"), label)
            self.require(phase.get("source_file") == f"PHASE{number}.md", f"{label}: incorrect source_file")
            self.require(phase.get("delivery_stage") in milestones, f"{label}: unknown delivery_stage")
            if phase.get("delivery_stage") in milestones:
                self.require(number in milestones[phase["delivery_stage"]].get("phases", []),
                             f"{label}: delivery stage does not include this phase")
            work = phase.get("work_packages", [])
            package_ids = [item["id"] for item in work]
            packages.extend(work)
            if number == 0:
                self.require(set(package_ids) == PHASE_ZERO_IDS, "phase 0: incomplete decision/spike/baseline coverage")
            elif source and source.is_file():
                source_packages = re.findall(r"^#{1,6}\s+(W\d+)\b", source.read_text(encoding="utf-8"), re.MULTILINE)
                self.require([item.get("source_work_package") for item in work] == source_packages,
                             f"{label}: work packages differ from source W headings")
                self.require(package_ids == [f"P{number:02d}-{item}" for item in source_packages],
                             f"{label}: work package IDs do not match source headings")
            for item in work:
                self.task(item, item["id"])
                self.require(bool(item.get("description")), f"{item['id']}: missing description")
            for gate in ("local_gate_state", "integration_gate_state"):
                self.require(phase.get(gate) in GATE_STATES, f"{label}: invalid {gate}")
            complete = phase.get("full_phase_complete")
            self.require(isinstance(complete, bool), f"{label}: full_phase_complete must be boolean")
            self.evidence(phase, label, required=complete or any(phase.get(gate) == "verified" for gate in ("local_gate_state", "integration_gate_state")))
            if complete:
                self.require(phase.get("local_gate_state") == phase.get("integration_gate_state") == "verified",
                             f"{label}: full completion requires both gates verified")
                self.require(all(item.get("state") == "verified" for item in work),
                             f"{label}: full completion has unverified work packages")
            for seam in phase.get("related_seams", []):
                self.require(seam in seams, f"{label}: unknown related seam {seam}")
            mirror = phase_status.get(number, {})
            for field in ("title", "implementation_state", "specification_state", "local_gate_state",
                          "integration_gate_state", "full_phase_complete", "related_seams", "evidence"):
                self.require(mirror.get(field) == phase.get(field), f"{label}: status differs on {field}")
            self.require(mirror.get("required_work_packages") == package_ids,
                         f"{label}: status work package coverage differs")
        package_index = self.index(packages, "id", "work packages")
        self.require(len(package_index) == 112, "expected 112 source work packages")
        self.require(not set(package_index).intersection(tickets), "work package and ticket IDs overlap")

        ledger = (self.root / "spec/seams.md").read_text(encoding="utf-8")
        source_seams = {}
        for row in ledger.splitlines():
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if cells and re.fullmatch(r"S\d+", cells[0]):
                value = cells[-1]
                source_seams[cells[0]] = ("FIXED_WORDING_ONLY" if value.startswith("FIXED") and re.search(r"wording|reworded", value, re.I)
                                          else value.split(" ", 1)[0].split("(", 1)[0])
        self.require(set(source_seams) == set(seams), "seam coverage differs from spec/seams.md")
        for identifier, seam in seams.items():
            self.require(seam.get("ledger_status") == source_seams.get(identifier),
                         f"{identifier}: ledger_status differs from source seam ledger")
            verified = seam.get("implementation_status") == "verified"
            self.require(seam.get("implementation_status") in {"not_verified", "in_progress", "verified"},
                         f"{identifier}: invalid implementation_status")
            self.evidence(seam, identifier, required=verified)
            for field in ("upstream", "work", "downstreamGates", "test"):
                self.require(bool(seam.get(field)), f"{identifier}: missing {field}")
        summary = status.get("seam_summary", {})
        self.require(summary.get("total") == len(seams), "status: incorrect seam total")
        self.require(summary.get("open") == sum(s.get("ledger_status") == "OPEN" for s in seams.values()), "status: incorrect open seam count")
        self.require(summary.get("contract_corrections") == [key for key, value in seams.items() if value.get("ledger_status") == "FIXED_WORDING_ONLY"], "status: incorrect contract correction list")
        self.require(summary.get("implemented_closures_verified_here") == sum(s.get("implementation_status") == "verified" for s in seams.values()), "status: incorrect verified seam count")

        source_index = self.index(sources["inputs"], "path", "source fingerprints")
        required_sources = {"ROADMAP.md", "ROADMAP_DIFF.md", "BUILD0.md", "spec/seams.md"} | {f"PHASE{i}.md" for i in range(17)}
        self.require(required_sources.issubset(source_index), "source fingerprints omit a roadmap, phase, build or seam input")
        for path, source in source_index.items():
            target = self.path(path, "source fingerprint")
            digest = source.get("sha256_normalized_utf8_lf", "")
            self.require(bool(re.fullmatch(r"[0-9a-f]{64}", digest)), f"{path}: invalid SHA-256 fingerprint")
            self.require(isinstance(source.get("normalized_bytes"), int) and source["normalized_bytes"] > 0, f"{path}: invalid normalized byte length")
            if check_sources and target and target.is_file():
                data = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
                self.require(hashlib.sha256(data).hexdigest() == digest and len(data) == source.get("normalized_bytes"),
                             f"{path}: source drift; review the plan and deliberately refresh its fingerprint")

        for identifier in list(tickets) + list(package_index) + list(seams):
            self.require(bool(re.search(rf"(?<![\w-]){re.escape(identifier)}(?![\w-])", markdown)), f"DEVELOPMENT_SPEC.md: missing {identifier}")
        for number in phases:
            self.require(f"](PHASE{number}.md)" in markdown, f"DEVELOPMENT_SPEC.md: missing source link PHASE{number}.md")
        for link in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", markdown):
            destination = link.strip().strip("<>")
            parsed = urlsplit(destination)
            if not parsed.scheme and not destination.startswith("#"):
                self.path(unquote(parsed.path), "DEVELOPMENT_SPEC.md link")
        return ready


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready", action="store_true", help="print the starter tickets whose dependencies are verified")
    parser.add_argument("--check-sources", action="store_true", help="also compare the reconciled input fingerprints to the current files")
    args = parser.parse_args()
    checker = PlanCheck(ROOT)
    try:
        backlog = json.loads((ROOT / "spec/development_backlog.json").read_text(encoding="utf-8"))
        status = json.loads((ROOT / "spec/status.json").read_text(encoding="utf-8"))
        sources = json.loads((ROOT / "spec/development_sources.json").read_text(encoding="utf-8"))
        markdown = (ROOT / "DEVELOPMENT_SPEC.md").read_text(encoding="utf-8")
        ready = checker.validate(backlog, status, sources, markdown, check_sources=args.check_sources)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        checker.errors.append(f"cannot validate malformed or missing plan data: {exc}")
        ready = []
    if checker.errors:
        print(f"Development specification failed ({len(checker.errors)} issue(s)):", file=sys.stderr)
        for error in checker.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Development specification OK: 17 phases, 12 starter tickets, 112 work packages, 25 seams.")
    if args.check_sources:
        print(f"Source fingerprints OK: {len(sources['inputs'])} reconciled inputs.")
    if args.ready:
        if ready:
            for ticket in ready:
                print(f"Ready: {ticket['id']} - {ticket['title']} ({ticket['owner_role']})")
        else:
            print("No pending starter tickets are ready; inspect in-progress work and dependencies.")
    else:
        print("Ready queue: " + (", ".join(ticket["id"] for ticket in ready) or "empty"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
