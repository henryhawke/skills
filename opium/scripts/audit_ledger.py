#!/usr/bin/env python3
"""Create, merge, validate, and summarize Opium audit ledgers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
FINGERPRINT_VERSION = 2
CELLS = (
    "CONTRACT",
    "MOUNT",
    "IMPLEMENT",
    "NEGATIVE",
    "LIFECYCLE",
    "SECURITY",
    "TEST",
    "CANDIDATE",
    "LIVE",
)
CELL_STATES = {"SATISFIED", "UNSATISFIED", "UNKNOWN", "NA"}
DISPOSITIONS = {
    "UNASSESSED",
    "VERIFIED_COMPLETE",
    "PARTIAL",
    "MISSING",
    "CONTRADICTED",
    "BLOCKED_UNVERIFIED",
    "OUT_OF_SCOPE",
    "SUPERSEDED",
}
RISKS = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
TOTALITIES = {"TOTAL", "PARTIAL", "INVALID_FOR_CLAIM", "PROVENANCE_UNKNOWN"}
RESULTS = {"PASS", "FAIL", "CANCELLED", "UNKNOWN"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


class LedgerError(RuntimeError):
    pass


def git(repo: Path, *args: str, allow_failure: bool = False) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode and not allow_failure:
        message = proc.stderr.decode("utf-8", "replace").strip()
        raise LedgerError(f"git {' '.join(args)} failed: {message}")
    return proc.stdout


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode("utf-8", "surrogateescape"))
        return digest.hexdigest()
    if not path.is_file():
        digest.update(b"non-regular")
        return digest.hexdigest()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_snapshot(repo: Path) -> dict[str, Any]:
    root_raw = git(repo, "rev-parse", "--show-toplevel")
    root = Path(root_raw.decode().strip()).resolve()
    head = git(root, "rev-parse", "HEAD").decode().strip()
    branch = git(root, "branch", "--show-current").decode().strip() or "DETACHED"
    status_raw = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    status_entries = [
        item.decode("utf-8", "surrogateescape")
        for item in status_raw.split(b"\0")
        if item
    ]
    diff_digest = hashlib.sha256(git(root, "diff", "--binary", "HEAD", "--")).hexdigest()
    submodules_raw = git(root, "submodule", "status", "--recursive", allow_failure=True)
    submodules = [line for line in submodules_raw.decode("utf-8", "replace").splitlines() if line]
    submodule_snapshots: list[dict[str, Any]] = []
    for line in submodules:
        fields = line.lstrip(" +-U").split()
        if len(fields) < 2:
            continue
        relative = fields[1]
        submodule_root = root / relative
        if not submodule_root.exists() or line.startswith("-"):
            submodule_snapshots.append({"path": relative, "initialized": False})
            continue
        try:
            nested = repository_snapshot(submodule_root)
            submodule_snapshots.append(
                {
                    "path": relative,
                    "initialized": True,
                    "head": nested["head"],
                    "dirty": nested["dirty"],
                    "fingerprint": nested["fingerprint"],
                }
            )
        except LedgerError as exc:
            submodule_snapshots.append(
                {"path": relative, "initialized": True, "snapshot_error": str(exc)}
            )

    untracked: list[dict[str, str]] = []
    for entry in status_entries:
        if not entry.startswith("?? "):
            continue
        relative = entry[3:]
        untracked.append({"path": relative, "sha256": hash_file(root / relative)})

    fingerprint_payload = {
        "fingerprint_version": FINGERPRINT_VERSION,
        "head": head,
        "status": status_entries,
        "diff_sha256": diff_digest,
        "untracked": untracked,
        "submodules": submodules,
        "submodule_snapshots": submodule_snapshots,
    }
    encoded = json.dumps(
        fingerprint_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    disk = shutil.disk_usage(root)
    return {
        "repo": str(root),
        "fingerprint_version": FINGERPRINT_VERSION,
        "captured_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "branch": branch,
        "head": head,
        "dirty": bool(status_entries),
        "status": status_entries,
        "diff_sha256": diff_digest,
        "untracked": untracked,
        "submodules": submodules,
        "submodule_snapshots": submodule_snapshots,
        "disk_free_bytes": disk.free,
        "fingerprint": hashlib.sha256(encoded).hexdigest(),
    }


def new_ledger(repo: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "audit": {
            "mode": "FULL",
            "finish_lines": [],
            "scope_boundary": {
                "included": [],
                "excluded": [],
                "manifest_entries_total": None,
                "manifest_entries_read": 0,
                "canonical_sources_exhausted": False,
                "notes": [],
            },
            "snapshot": repository_snapshot(repo),
        },
        "edicts": [],
        "observations": [],
        "checks": [],
        "undated_check_leads": [],
        "unknowns": [],
        "agent_runs": [],
        "warnings": [],
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LedgerError(f"{path} must contain a JSON object")
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def require_keys(value: dict[str, Any], keys: set[str], context: str, errors: list[str]) -> None:
    missing = sorted(keys - set(value))
    if missing:
        errors.append(f"{context}: missing keys {', '.join(missing)}")


def parse_time(value: str) -> datetime | None:
    if not value or value == "UNKNOWN":
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except ValueError:
        return None


def validate_shard(shard: dict[str, Any], fingerprint: str | None = None) -> list[str]:
    errors: list[str] = []
    require_keys(shard, {"schema_version", "agent_run", "observations", "checks", "unknowns"}, "shard", errors)
    if shard.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"shard: schema_version must be {SCHEMA_VERSION}")
    run = shard.get("agent_run")
    if not isinstance(run, dict):
        errors.append("shard.agent_run must be an object")
    else:
        require_keys(
            run,
            {"id", "snapshot_fingerprint", "model", "reasoning_effort", "scope", "method", "exclusions", "tool_limits"},
            "shard.agent_run",
            errors,
        )
        if fingerprint and run.get("snapshot_fingerprint") != fingerprint:
            errors.append("shard.agent_run snapshot_fingerprint does not match ledger")
        if not run.get("scope"):
            errors.append("shard.agent_run.scope must not be empty")

    for index, observation in enumerate(shard.get("observations", [])):
        context = f"shard.observations[{index}]"
        if not isinstance(observation, dict):
            errors.append(f"{context} must be an object")
            continue
        require_keys(
            observation,
            {"edict_id", "cell", "proposed_state", "claim", "evidence", "counterevidence", "disconfirmation", "confidence"},
            context,
            errors,
        )
        if observation.get("cell") not in CELLS:
            errors.append(f"{context}.cell is invalid")
        if observation.get("proposed_state") not in CELL_STATES:
            errors.append(f"{context}.proposed_state is invalid")
        if observation.get("confidence") not in CONFIDENCE:
            errors.append(f"{context}.confidence is invalid")
        if not observation.get("claim"):
            errors.append(f"{context}.claim must not be empty")
        if observation.get("proposed_state") == "SATISFIED" and not observation.get("evidence"):
            errors.append(f"{context}: SATISFIED requires evidence")
        if not observation.get("disconfirmation"):
            errors.append(f"{context}.disconfirmation must not be empty")
    for index, lead in enumerate(shard.get("undated_check_leads", [])):
        if not isinstance(lead, dict) or not lead.get("claim") or not lead.get("evidence"):
            errors.append(f"shard.undated_check_leads[{index}] requires claim and evidence")
    return errors


def validate_ledger(ledger: dict[str, Any], repo: Path | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    require_keys(
        ledger,
        {"schema_version", "audit", "edicts", "observations", "checks", "undated_check_leads", "unknowns", "agent_runs", "warnings"},
        "ledger",
        errors,
    )
    if ledger.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"ledger.schema_version must be {SCHEMA_VERSION}")

    audit = ledger.get("audit", {})
    if not isinstance(audit, dict):
        errors.append("ledger.audit must be an object")
        audit = {}
    if audit.get("mode") not in {"FULL", "DEGRADED"}:
        errors.append("ledger.audit.mode must be FULL or DEGRADED")
    snapshot = audit.get("snapshot", {})
    if repo and isinstance(snapshot, dict) and snapshot.get("fingerprint"):
        current = repository_snapshot(repo)
        if snapshot.get("fingerprint_version") != current.get("fingerprint_version"):
            errors.append("repository fingerprint algorithm changed during the audit; reinitialize the ledger")
        elif current["fingerprint"] != snapshot.get("fingerprint"):
            errors.append("repository snapshot changed after the ledger was initialized")
    scope = audit.get("scope_boundary", {})
    if isinstance(scope, dict):
        if audit.get("mode") == "FULL" and not scope.get("canonical_sources_exhausted"):
            errors.append("FULL audit requires canonical_sources_exhausted=true")
        total = scope.get("manifest_entries_total")
        read = scope.get("manifest_entries_read", 0)
        if total is not None and isinstance(total, int) and read > total:
            errors.append("scope_boundary.manifest_entries_read exceeds total")
        if total is not None and audit.get("mode") == "FULL" and read != total:
            errors.append("FULL audit requires every manifest entry to be read")

    edicts = ledger.get("edicts", [])
    if not edicts:
        errors.append("ledger.edicts must not be empty for final validation")
    ids: list[str] = []
    for index, edict in enumerate(edicts):
        context = f"ledger.edicts[{index}]"
        if not isinstance(edict, dict):
            errors.append(f"{context} must be an object")
            continue
        require_keys(
            edict,
            {"id", "requirement", "sources", "dimension", "risk", "disposition", "obligations", "dependencies", "acceptance"},
            context,
            errors,
        )
        edict_id = edict.get("id")
        if isinstance(edict_id, str):
            ids.append(edict_id)
        if edict.get("risk") not in RISKS:
            errors.append(f"{context}.risk is invalid")
        disposition = edict.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"{context}.disposition is invalid")
        if disposition == "UNASSESSED":
            errors.append(f"{context}: final validation forbids UNASSESSED")
        obligations = edict.get("obligations")
        if not isinstance(obligations, dict):
            errors.append(f"{context}.obligations must be an object")
            continue
        missing_cells = sorted(set(CELLS) - set(obligations))
        if missing_cells:
            errors.append(f"{context}.obligations missing cells: {', '.join(missing_cells)}")
        methods: set[str] = set()
        required_states: list[str] = []
        for cell in CELLS:
            obligation = obligations.get(cell)
            if not isinstance(obligation, dict):
                continue
            require_keys(obligation, {"state", "evidence", "counterevidence", "methods", "agent_ids"}, f"{context}.obligations.{cell}", errors)
            state = obligation.get("state")
            if state not in CELL_STATES:
                errors.append(f"{context}.obligations.{cell}.state is invalid")
            if state != "NA":
                required_states.append(state)
            if state == "SATISFIED" and not obligation.get("evidence"):
                errors.append(f"{context}.obligations.{cell}: SATISFIED requires evidence")
            methods.update(str(item) for item in obligation.get("methods", []) if item)
        if disposition == "VERIFIED_COMPLETE" and any(state != "SATISFIED" for state in required_states):
            errors.append(f"{context}: VERIFIED_COMPLETE requires every applicable obligation SATISFIED")
        if disposition == "BLOCKED_UNVERIFIED" and "UNKNOWN" not in required_states:
            errors.append(f"{context}: BLOCKED_UNVERIFIED requires an UNKNOWN obligation")
        if disposition == "VERIFIED_COMPLETE" and edict.get("risk") in {"CRITICAL", "HIGH"}:
            if len(methods) < 2:
                errors.append(f"{context}: critical/high completion requires two independent methods")
            adversarial = any("advers" in method.lower() or "falsif" in method.lower() for method in methods)
            if not adversarial:
                errors.append(f"{context}: critical/high completion requires adversarial falsification")

    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"duplicate edict ids: {', '.join(duplicate_ids)}")
    edict_ids = set(ids)

    runs = ledger.get("agent_runs", [])
    run_ids = [run.get("id") for run in runs if isinstance(run, dict)]
    duplicate_runs = sorted(str(key) for key, count in Counter(run_ids).items() if key and count > 1)
    if duplicate_runs:
        errors.append(f"duplicate agent run ids: {', '.join(duplicate_runs)}")
    fingerprint = snapshot.get("fingerprint") if isinstance(snapshot, dict) else None
    for index, run in enumerate(runs):
        if isinstance(run, dict) and fingerprint and run.get("snapshot_fingerprint") != fingerprint:
            errors.append(f"ledger.agent_runs[{index}] has a stale snapshot fingerprint")

    for index, observation in enumerate(ledger.get("observations", [])):
        if not isinstance(observation, dict):
            errors.append(f"ledger.observations[{index}] must be an object")
            continue
        if observation.get("edict_id") not in edict_ids:
            errors.append(f"ledger.observations[{index}] references unknown edict {observation.get('edict_id')}")

    checks = ledger.get("checks", [])
    if len(checks) > 10:
        errors.append("ledger.checks may contain at most the latest ten orderable completed runs")
    dated: list[datetime] = []
    check_ids: list[str] = []
    for index, check in enumerate(checks):
        context = f"ledger.checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{context} must be an object")
            continue
        require_keys(check, {"id", "executed_at", "profile", "tree", "target", "result", "totality", "skips", "warnings", "edict_ids", "evidence"}, context, errors)
        check_ids.append(str(check.get("id")))
        when = parse_time(str(check.get("executed_at", "")))
        if when is None:
            errors.append(f"{context}.executed_at must be a valid ISO-8601 time; move undated claims to undated_check_leads")
        else:
            dated.append(when)
        if check.get("result") not in RESULTS:
            errors.append(f"{context}.result is invalid")
        if check.get("totality") not in TOTALITIES:
            errors.append(f"{context}.totality is invalid")
        if check.get("totality") == "TOTAL":
            if not check.get("evidence") or check.get("tree") in {None, "", "UNKNOWN"}:
                errors.append(f"{context}: TOTAL requires evidence and known tree binding")
            if check.get("skips"):
                warnings.append(f"{context}: TOTAL has skips; justify or downgrade totality")
    if dated != sorted(dated, reverse=True):
        errors.append("ledger.checks must be sorted newest first")
    duplicated_checks = sorted(key for key, count in Counter(check_ids).items() if count > 1)
    if duplicated_checks:
        errors.append(f"duplicate check ids: {', '.join(duplicated_checks)}")
    if len(checks) < 10:
        warnings.append(f"latest-ten ledger contains only {len(checks)}/10 orderable runs")

    for index, lead in enumerate(ledger.get("undated_check_leads", [])):
        if not isinstance(lead, dict) or not lead.get("claim") or not lead.get("evidence"):
            errors.append(f"ledger.undated_check_leads[{index}] requires claim and evidence")

    if audit.get("mode") == "DEGRADED":
        warnings.append("audit ran in DEGRADED mode; coverage denominators are provisional")
    if isinstance(snapshot, dict) and snapshot.get("disk_free_bytes", 0) < 1024**3:
        warnings.append("repository filesystem had less than 1 GiB free at snapshot time")
    return errors, warnings


def merge_shard(ledger: dict[str, Any], shard: dict[str, Any]) -> None:
    fingerprint = ledger.get("audit", {}).get("snapshot", {}).get("fingerprint")
    errors = validate_shard(shard, fingerprint)
    if errors:
        raise LedgerError("invalid shard:\n- " + "\n- ".join(errors))
    run = shard["agent_run"]
    if any(existing.get("id") == run.get("id") for existing in ledger.get("agent_runs", [])):
        raise LedgerError(f"agent run id already merged: {run.get('id')}")
    ledger.setdefault("agent_runs", []).append(run)
    for observation in shard.get("observations", []):
        item = dict(observation)
        item["agent_run_id"] = run["id"]
        item["method"] = run["method"]
        ledger.setdefault("observations", []).append(item)
    existing_checks = {item.get("id"): item for item in ledger.get("checks", []) if isinstance(item, dict)}
    for check in shard.get("checks", []):
        check_id = check.get("id") if isinstance(check, dict) else None
        if check_id in existing_checks and existing_checks[check_id] != check:
            raise LedgerError(f"conflicting check record: {check_id}")
        if check_id not in existing_checks:
            ledger.setdefault("checks", []).append(check)
    ledger.setdefault("unknowns", []).extend(shard.get("unknowns", []))
    ledger.setdefault("undated_check_leads", []).extend(shard.get("undated_check_leads", []))


def add_check_evidence(ledger: dict[str, Any], payload: dict[str, Any]) -> None:
    """Add orderable checks and undated leads without direct ledger editing."""
    checks = payload.get("checks", [])
    leads = payload.get("undated_check_leads", [])
    if not isinstance(checks, list) or not isinstance(leads, list):
        raise LedgerError("check-evidence payload fields must be lists")
    existing_checks = {
        item.get("id"): item for item in ledger.get("checks", []) if isinstance(item, dict)
    }
    for check in checks:
        if not isinstance(check, dict) or not check.get("id"):
            raise LedgerError("every orderable check requires an id")
        if parse_time(str(check.get("executed_at", ""))) is None:
            raise LedgerError(f"check {check.get('id')} is undated; add it as an undated lead")
        check_id = check["id"]
        if check_id in existing_checks and existing_checks[check_id] != check:
            raise LedgerError(f"conflicting check record: {check_id}")
        if check_id not in existing_checks:
            ledger.setdefault("checks", []).append(check)
            existing_checks[check_id] = check
    ledger["checks"] = sorted(
        ledger.get("checks", []),
        key=lambda item: parse_time(str(item.get("executed_at", ""))) or datetime.min.astimezone(),
        reverse=True,
    )[:10]

    existing_leads = {
        item.get("id"): item
        for item in ledger.get("undated_check_leads", [])
        if isinstance(item, dict) and item.get("id")
    }
    for lead in leads:
        if not isinstance(lead, dict) or not lead.get("id") or not lead.get("claim") or not lead.get("evidence"):
            raise LedgerError("every undated lead requires id, claim, and evidence")
        lead_id = lead["id"]
        if lead_id in existing_leads and existing_leads[lead_id] != lead:
            raise LedgerError(f"conflicting undated check lead: {lead_id}")
        if lead_id not in existing_leads:
            ledger.setdefault("undated_check_leads", []).append(lead)
            existing_leads[lead_id] = lead


def seed_edicts(ledger: dict[str, Any], payload: dict[str, Any]) -> None:
    """Set the bounded edict universe once, before agent observations arrive."""
    if ledger.get("edicts"):
        raise LedgerError("ledger already contains edicts; seed is intentionally one-time")
    edicts = payload.get("edicts")
    if not isinstance(edicts, list) or not edicts:
        raise LedgerError("seed payload requires a non-empty edicts list")
    ids = [item.get("id") for item in edicts if isinstance(item, dict)]
    if len(ids) != len(edicts) or any(not item for item in ids):
        raise LedgerError("every seeded edict requires a non-empty id")
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise LedgerError(f"duplicate seeded edict ids: {', '.join(sorted(duplicates))}")
    for edict in edicts:
        edict.setdefault("disposition", "UNASSESSED")
    ledger["edicts"] = edicts
    audit = ledger.setdefault("audit", {})
    for key in ("mode", "finish_lines", "scope_boundary"):
        if key in payload:
            audit[key] = payload[key]


def adjudicate(ledger: dict[str, Any], payload: dict[str, Any]) -> None:
    """Apply root-owned dispositions and proof vectors after reviewing observations."""
    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        raise LedgerError("adjudication payload requires a non-empty decisions list")
    by_id = {
        item.get("id"): item
        for item in ledger.get("edicts", [])
        if isinstance(item, dict) and item.get("id")
    }
    seen: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            raise LedgerError("every decision must be an object")
        edict_id = decision.get("edict_id")
        if edict_id not in by_id:
            raise LedgerError(f"decision references unknown edict: {edict_id}")
        if edict_id in seen:
            raise LedgerError(f"duplicate decision for edict: {edict_id}")
        seen.add(edict_id)
        disposition = decision.get("disposition")
        if disposition not in DISPOSITIONS - {"UNASSESSED"}:
            raise LedgerError(f"invalid final disposition for {edict_id}: {disposition}")
        obligations = decision.get("obligations")
        if not isinstance(obligations, dict):
            raise LedgerError(f"decision {edict_id} requires obligations")
        target = by_id[edict_id]
        target["disposition"] = disposition
        target["obligations"] = obligations
        target["adjudication"] = {
            "reason": decision.get("reason", ""),
            "observation_ids": decision.get("observation_ids", []),
            "adjudicated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
        for key in ("acceptance", "dependencies"):
            if key in decision:
                target[key] = decision[key]


def summary(ledger: dict[str, Any]) -> dict[str, Any]:
    disposition_counts = Counter(
        edict.get("disposition", "UNSET") for edict in ledger.get("edicts", []) if isinstance(edict, dict)
    )
    risk_gaps = [
        edict.get("id")
        for edict in ledger.get("edicts", [])
        if isinstance(edict, dict)
        and edict.get("risk") in {"CRITICAL", "HIGH"}
        and edict.get("disposition") != "VERIFIED_COMPLETE"
    ]
    unknown_cells = 0
    for edict in ledger.get("edicts", []):
        if not isinstance(edict, dict):
            continue
        for obligation in edict.get("obligations", {}).values():
            if isinstance(obligation, dict) and obligation.get("state") == "UNKNOWN":
                unknown_cells += 1
    return {
        "mode": ledger.get("audit", {}).get("mode"),
        "snapshot_fingerprint": ledger.get("audit", {}).get("snapshot", {}).get("fingerprint"),
        "edicts": len(ledger.get("edicts", [])),
        "dispositions": dict(sorted(disposition_counts.items())),
        "critical_high_not_complete": risk_gaps,
        "unknown_obligation_cells": unknown_cells,
        "agent_runs": len(ledger.get("agent_runs", [])),
        "observations": len(ledger.get("observations", [])),
        "latest_checks": len(ledger.get("checks", [])),
        "undated_check_leads": len(ledger.get("undated_check_leads", [])),
        "unknowns": len(ledger.get("unknowns", [])),
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="opium-self-test-") as directory:
        repo = Path(directory) / "repo"
        repo.mkdir()
        subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "opium@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Opium Self Test"], check=True)
        (repo / "sample.txt").write_text("sample\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "sample.txt"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "sample"], check=True)
        ledger = new_ledger(repo)
        fingerprint = ledger["audit"]["snapshot"]["fingerprint"]
        final_obligations = {
            cell: {
                "state": "SATISFIED" if cell == "IMPLEMENT" else "NA",
                "evidence": [{"locator": "sample.txt:1"}] if cell == "IMPLEMENT" else [],
                "counterevidence": [],
                "methods": ["source_trace"] if cell == "IMPLEMENT" else [],
                "agent_ids": ["self-test"] if cell == "IMPLEMENT" else [],
            }
            for cell in CELLS
        }
        seed_edicts(
            ledger,
            {
                "mode": "DEGRADED",
                "edicts": [
                    {
                        "id": "E-001",
                        "requirement": "Sample requirement",
                        "sources": [{"path": "sample.txt", "line": 1}],
                        "dimension": "runtime/source",
                        "risk": "LOW",
                        "dependencies": [],
                        "acceptance": ["sample exists"],
                        "obligations": {
                            cell: {
                                "state": "UNKNOWN" if cell == "IMPLEMENT" else "NA",
                                "evidence": [],
                                "counterevidence": [],
                                "methods": [],
                                "agent_ids": [],
                            }
                            for cell in CELLS
                        },
                    }
                ],
            },
        )
        shard = {
            "schema_version": SCHEMA_VERSION,
            "agent_run": {
                "id": "self-test",
                "snapshot_fingerprint": fingerprint,
                "model": "self-test",
                "reasoning_effort": "none",
                "scope": ["E-001:IMPLEMENT"],
                "method": "source_trace",
                "exclusions": [],
                "tool_limits": [],
            },
            "observations": [
                {
                    "edict_id": "E-001",
                    "cell": "IMPLEMENT",
                    "proposed_state": "SATISFIED",
                    "claim": "sample exists",
                    "evidence": [{"kind": "source", "locator": "sample.txt:1", "note": "exists"}],
                    "counterevidence": [],
                    "disconfirmation": "file may change after snapshot",
                    "confidence": "HIGH",
                }
            ],
            "checks": [],
            "undated_check_leads": [],
            "unknowns": [],
        }
        merge_shard(ledger, shard)
        add_check_evidence(
            ledger,
            {
                "checks": [],
                "undated_check_leads": [
                    {
                        "id": "lead-1",
                        "claim": "reported sample check",
                        "evidence": [{"locator": "sample.txt:1"}],
                        "missing": ["execution timestamp", "tree binding"],
                    }
                ],
            },
        )
        adjudicate(
            ledger,
            {
                "decisions": [
                    {
                        "edict_id": "E-001",
                        "disposition": "VERIFIED_COMPLETE",
                        "obligations": final_obligations,
                        "reason": "self-test observation",
                        "observation_ids": ["self-test:0"],
                    }
                ]
            },
        )
        errors, warnings = validate_ledger(ledger, repo)
        if errors:
            raise LedgerError("self-test validation failed:\n- " + "\n- ".join(errors))
        if not warnings:
            raise LedgerError("self-test expected degraded/latest-ten warnings")
        result = summary(ledger)
        if result["agent_runs"] != 1 or result["undated_check_leads"] != 1:
            raise LedgerError("self-test summary mismatch")
    print("audit_ledger.py self-test passed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize a ledger")
    init_parser.add_argument("--repo", type=Path, required=True)
    init_parser.add_argument("--out", type=Path, required=True)

    fingerprint_parser = subparsers.add_parser("fingerprint", help="print a repository snapshot")
    fingerprint_parser.add_argument("--repo", type=Path, required=True)

    merge_parser = subparsers.add_parser("merge-shard", help="validate and merge an agent shard")
    merge_parser.add_argument("--ledger", type=Path, required=True)
    merge_parser.add_argument("--shard", type=Path, required=True)

    seed_parser = subparsers.add_parser("seed-edicts", help="seed the bounded edict universe once")
    seed_parser.add_argument("--ledger", type=Path, required=True)
    seed_parser.add_argument("--input", type=Path, required=True)

    adjudicate_parser = subparsers.add_parser("adjudicate", help="apply root-owned final edict decisions")
    adjudicate_parser.add_argument("--ledger", type=Path, required=True)
    adjudicate_parser.add_argument("--input", type=Path, required=True)

    checks_parser = subparsers.add_parser("add-check-evidence", help="add ordered checks and undated leads")
    checks_parser.add_argument("--ledger", type=Path, required=True)
    checks_parser.add_argument("--input", type=Path, required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a final ledger")
    validate_parser.add_argument("--ledger", type=Path, required=True)
    validate_parser.add_argument("--repo", type=Path)

    summary_parser = subparsers.add_parser("summary", help="print ledger coverage summary")
    summary_parser.add_argument("--ledger", type=Path, required=True)

    subparsers.add_parser("self-test", help="run deterministic self-tests")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            atomic_write(args.out, new_ledger(args.repo))
            print(args.out)
        elif args.command == "fingerprint":
            print(json.dumps(repository_snapshot(args.repo), indent=2, sort_keys=True))
        elif args.command == "merge-shard":
            ledger = load_json(args.ledger)
            merge_shard(ledger, load_json(args.shard))
            atomic_write(args.ledger, ledger)
            print(args.ledger)
        elif args.command == "seed-edicts":
            ledger = load_json(args.ledger)
            seed_edicts(ledger, load_json(args.input))
            atomic_write(args.ledger, ledger)
            print(args.ledger)
        elif args.command == "adjudicate":
            ledger = load_json(args.ledger)
            adjudicate(ledger, load_json(args.input))
            atomic_write(args.ledger, ledger)
            print(args.ledger)
        elif args.command == "add-check-evidence":
            ledger = load_json(args.ledger)
            add_check_evidence(ledger, load_json(args.input))
            atomic_write(args.ledger, ledger)
            print(args.ledger)
        elif args.command == "validate":
            ledger = load_json(args.ledger)
            errors, warnings = validate_ledger(ledger, args.repo)
            for warning in warnings:
                print(f"WARNING: {warning}", file=sys.stderr)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 2
            print("ledger is valid")
        elif args.command == "summary":
            print(json.dumps(summary(load_json(args.ledger)), indent=2, sort_keys=True))
        elif args.command == "self-test":
            self_test()
        return 0
    except LedgerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
