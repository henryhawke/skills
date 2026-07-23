#!/usr/bin/env python3
"""Create, merge, validate, and summarize evidence-bound Opium audit ledgers."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, NoReturn

SCHEMA_VERSION = 1
ENGINE_VERSION = 2
FINGERPRINT_VERSION = 3
MAX_JSON_BYTES = 16 * 1024 * 1024
GIT_TIMEOUT_SECONDS = 30

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
AUDIT_MODES = {"FULL", "DEGRADED"}

ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]*$")
IMPLEMENTATION_METHOD_MARKERS = ("source", "static", "trace", "mount", "reachab")
VALIDATION_METHOD_MARKERS = ("test", "ci", "candidate", "runtime", "live", "device")
ADVERSARIAL_METHOD_MARKERS = ("advers", "falsif", "skeptic", "negative_space")


class LedgerError(RuntimeError):
    """A user-correctable ledger, payload, repository, or command error."""


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message} [{self.code}]"


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    def error(self, code: str, path: str, message: str) -> None:
        self.issues.append(ValidationIssue("ERROR", code, path, message))

    def warning(self, code: str, path: str, message: str) -> None:
        self.issues.append(ValidationIssue("WARNING", code, path, message))

    def extend(self, other: ValidationReport) -> None:
        self.issues.extend(other.issues)

    @property
    def errors(self) -> list[str]:
        return [issue.render() for issue in self.issues if issue.severity == "ERROR"]

    @property
    def warnings(self) -> list[str]:
        return [issue.render() for issue in self.issues if issue.severity == "WARNING"]

    def to_json(self) -> dict[str, Any]:
        return {
            "valid": not self.errors,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [asdict(issue) for issue in self.issues],
        }


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: bytes
    stderr: bytes


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _raise_json_constant(value: str) -> NoReturn:
    raise LedgerError(f"JSON contains unsupported numeric constant {value}")


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LedgerError(f"JSON contains duplicate object key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        size = path.stat().st_size
        if size > MAX_JSON_BYTES:
            raise LedgerError(
                f"JSON file exceeds {MAX_JSON_BYTES} byte safety limit: {path}"
            )
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_raise_json_constant,
        )
    except LedgerError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LedgerError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LedgerError(f"{path} must contain a JSON object")
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        try:
            directory_descriptor = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_descriptor = None
        if directory_descriptor is not None:
            try:
                try:
                    os.fsync(directory_descriptor)
                except OSError:
                    pass
            finally:
                os.close(directory_descriptor)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run_git(
    repo: Path,
    *args: str,
    allow_failure: bool = False,
    timeout: int = GIT_TIMEOUT_SECONDS,
) -> GitResult:
    environment = os.environ.copy()
    environment.update(
        {
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    try:
        process = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise LedgerError(f"git {' '.join(args)} could not run: {exc}") from exc
    result = GitResult(process.returncode, process.stdout, process.stderr)
    if result.returncode and not allow_failure:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise LedgerError(
            f"git {' '.join(args)} failed with exit {result.returncode}: {message}"
        )
    return result


def git(repo: Path, *args: str, allow_failure: bool = False) -> bytes:
    """Compatibility wrapper for callers that only need standard output."""
    return run_git(repo, *args, allow_failure=allow_failure).stdout


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        if path.is_symlink():
            digest.update(b"symlink\0")
            digest.update(os.readlink(path).encode("utf-8", "surrogateescape"))
            return digest.hexdigest()
        if not path.exists():
            digest.update(b"missing\0")
            return digest.hexdigest()
        if not path.is_file():
            digest.update(b"non-regular\0")
            digest.update(str(path.stat().st_mode).encode("ascii"))
            return digest.hexdigest()
        digest.update(b"file\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        digest.update(b"unreadable\0")
        digest.update(str(exc).encode("utf-8", "replace"))
    return digest.hexdigest()


def _parse_porcelain_v2(raw: bytes) -> list[str]:
    tokens = [token for token in raw.split(b"\0") if token]
    records: list[str] = []
    index = 0
    while index < len(tokens):
        record = tokens[index].decode("utf-8", "surrogateescape")
        index += 1
        if record.startswith("2 ") and index < len(tokens):
            original = tokens[index].decode("utf-8", "surrogateescape")
            index += 1
            record = f"{record} original={original}"
        records.append(record)
    return records


def _untracked_from_status(root: Path, status: Iterable[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for record in status:
        if not record.startswith("? "):
            continue
        relative = record[2:]
        entries.append({"path": relative, "sha256": hash_file(root / relative)})
    return sorted(entries, key=lambda item: item["path"])


def _optional_git_text(repo: Path, *args: str) -> tuple[str | None, str | None]:
    result = run_git(repo, *args, allow_failure=True)
    if result.returncode:
        message = result.stderr.decode("utf-8", "replace").strip()
        return None, message or f"git {' '.join(args)} exited {result.returncode}"
    return result.stdout.decode("utf-8", "replace").strip(), None


def repository_snapshot(
    repo: Path,
    *,
    _seen: set[Path] | None = None,
) -> dict[str, Any]:
    requested = repo.expanduser().resolve()
    root_result = run_git(requested, "rev-parse", "--show-toplevel")
    root = Path(root_result.stdout.decode().strip()).resolve()
    seen = set() if _seen is None else set(_seen)
    if root in seen:
        raise LedgerError(f"recursive repository/submodule cycle detected at {root}")
    seen.add(root)

    head_result = run_git(root, "rev-parse", "--verify", "HEAD", allow_failure=True)
    head = (
        head_result.stdout.decode().strip()
        if head_result.returncode == 0
        else "UNBORN"
    )
    branch = (
        run_git(root, "branch", "--show-current").stdout.decode().strip()
        or "DETACHED"
    )
    status_raw = run_git(
        root,
        "status",
        "--porcelain=v2",
        "-z",
        "--untracked-files=all",
    ).stdout
    status = _parse_porcelain_v2(status_raw)

    if head == "UNBORN":
        staged_diff = run_git(root, "diff", "--cached", "--binary", "--").stdout
        tracked_diff = staged_diff
    else:
        staged_diff = run_git(
            root,
            "diff",
            "--cached",
            "--binary",
            "HEAD",
            "--",
        ).stdout
        tracked_diff = run_git(root, "diff", "--binary", "HEAD", "--").stdout
    unstaged_diff = run_git(root, "diff", "--binary", "--").stdout

    upstream, upstream_error = _optional_git_text(
        root,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{upstream}",
    )
    ahead = behind = None
    if upstream:
        counts, counts_error = _optional_git_text(
            root,
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream}",
        )
        if counts and not counts_error:
            fields = counts.split()
            if len(fields) == 2 and all(field.isdigit() for field in fields):
                ahead, behind = int(fields[0]), int(fields[1])

    tool_errors: list[str] = []
    submodule_result = run_git(
        root,
        "submodule",
        "status",
        "--recursive",
        allow_failure=True,
    )
    if submodule_result.returncode:
        error = submodule_result.stderr.decode("utf-8", "replace").strip()
        tool_errors.append(f"submodule status unavailable: {error}")
        submodule_lines: list[str] = []
    else:
        submodule_lines = [
            line
            for line in submodule_result.stdout.decode(
                "utf-8", "replace"
            ).splitlines()
            if line
        ]

    submodule_snapshots: list[dict[str, Any]] = []
    for line in submodule_lines:
        fields = line.lstrip(" +-U").split()
        if len(fields) < 2:
            submodule_snapshots.append(
                {"raw": line, "snapshot_error": "unparseable submodule status"}
            )
            continue
        relative = fields[1]
        submodule_root = root / relative
        if not submodule_root.exists() or line.startswith("-"):
            submodule_snapshots.append(
                {"path": relative, "initialized": False, "raw": line}
            )
            continue
        try:
            nested = repository_snapshot(submodule_root, _seen=seen)
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
                {
                    "path": relative,
                    "initialized": True,
                    "snapshot_error": str(exc),
                }
            )

    untracked = _untracked_from_status(root, status)
    fingerprint_payload = {
        "fingerprint_version": FINGERPRINT_VERSION,
        "head": head,
        "branch": branch,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "status": status,
        "status_sha256": _sha256(status_raw),
        "tracked_diff_sha256": _sha256(tracked_diff),
        "staged_diff_sha256": _sha256(staged_diff),
        "unstaged_diff_sha256": _sha256(unstaged_diff),
        "untracked": untracked,
        "submodules": submodule_lines,
        "submodule_snapshots": submodule_snapshots,
        "tool_errors": tool_errors,
    }
    encoded = json.dumps(
        fingerprint_payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    disk = shutil.disk_usage(root)
    git_version = run_git(root, "--version").stdout.decode().strip()
    return {
        "repo": str(root),
        "fingerprint_version": FINGERPRINT_VERSION,
        "captured_at": _now(),
        "git_version": git_version,
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "upstream_error": upstream_error,
        "ahead": ahead,
        "behind": behind,
        "dirty": bool(status),
        "status": status,
        "status_sha256": _sha256(status_raw),
        "tracked_diff_sha256": _sha256(tracked_diff),
        "staged_diff_sha256": _sha256(staged_diff),
        "unstaged_diff_sha256": _sha256(unstaged_diff),
        "untracked": untracked,
        "submodules": submodule_lines,
        "submodule_snapshots": submodule_snapshots,
        "tool_errors": tool_errors,
        "disk_free_bytes": disk.free,
        "fingerprint": _sha256(encoded),
    }


def new_ledger(repo: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "engine": {
            "name": "opium-audit-ledger",
            "version": ENGINE_VERSION,
        },
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


def parse_time(value: str) -> datetime | None:
    if not value or value == "UNKNOWN":
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo is not None else None


def require_keys(
    value: dict[str, Any],
    keys: set[str],
    context: str,
    report: ValidationReport,
) -> None:
    missing = sorted(keys - set(value))
    if missing:
        report.error(
            "missing_keys",
            context,
            f"missing keys {', '.join(missing)}",
        )


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string(
    value: Any,
    path: str,
    report: ValidationReport,
    *,
    identifier: bool = False,
) -> None:
    if not _is_non_empty_string(value):
        report.error("invalid_string", path, "must be a non-empty string")
    elif identifier and not ID_PATTERN.fullmatch(value):
        report.error(
            "invalid_identifier",
            path,
            "must start with a letter and contain only letters, digits, '.', '_', ':', or '-'",
        )


def _validate_string_list(
    value: Any,
    path: str,
    report: ValidationReport,
    *,
    allow_empty: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        report.error("invalid_list", path, "must be a list")
        return []
    if not allow_empty and not value:
        report.error("empty_list", path, "must not be empty")
    result: list[str] = []
    for index, item in enumerate(value):
        if not _is_non_empty_string(item):
            report.error(
                "invalid_string",
                f"{path}[{index}]",
                "must be a non-empty string",
            )
        else:
            result.append(item)
    return result


def _validate_evidence(
    value: Any,
    path: str,
    report: ValidationReport,
    *,
    required: bool = False,
) -> None:
    if not isinstance(value, list):
        report.error("invalid_evidence", path, "must be a list")
        return
    if required and not value:
        report.error("missing_evidence", path, "must contain precise evidence")
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            report.error("invalid_evidence", item_path, "must be an object")
            continue
        _validate_string(item.get("locator"), f"{item_path}.locator", report)
        if "kind" not in item:
            report.warning(
                "evidence_kind_missing",
                item_path,
                "should identify its evidence kind",
            )
        elif not _is_non_empty_string(item.get("kind")):
            report.error(
                "invalid_evidence_kind",
                f"{item_path}.kind",
                "must be a non-empty string",
            )
        if "note" not in item:
            report.warning(
                "evidence_note_missing",
                item_path,
                "should state what the locator proves and does not prove",
            )
        elif not _is_non_empty_string(item.get("note")):
            report.error(
                "invalid_evidence_note",
                f"{item_path}.note",
                "must be a non-empty string",
            )


def _validate_agent_run(
    run: Any,
    path: str,
    report: ValidationReport,
    *,
    fingerprint: str | None = None,
) -> None:
    if not isinstance(run, dict):
        report.error("invalid_agent_run", path, "must be an object")
        return
    require_keys(
        run,
        {
            "id",
            "snapshot_fingerprint",
            "model",
            "reasoning_effort",
            "scope",
            "method",
            "exclusions",
            "tool_limits",
        },
        path,
        report,
    )
    _validate_string(run.get("id"), f"{path}.id", report, identifier=True)
    _validate_string(
        run.get("snapshot_fingerprint"),
        f"{path}.snapshot_fingerprint",
        report,
    )
    _validate_string(run.get("model"), f"{path}.model", report)
    _validate_string(
        run.get("reasoning_effort"),
        f"{path}.reasoning_effort",
        report,
    )
    _validate_string(run.get("method"), f"{path}.method", report)
    _validate_string_list(
        run.get("scope"),
        f"{path}.scope",
        report,
        allow_empty=False,
    )
    _validate_string_list(run.get("exclusions"), f"{path}.exclusions", report)
    _validate_string_list(run.get("tool_limits"), f"{path}.tool_limits", report)
    if (
        fingerprint
        and run.get("snapshot_fingerprint")
        and run.get("snapshot_fingerprint") != fingerprint
    ):
        report.error(
            "stale_snapshot",
            f"{path}.snapshot_fingerprint",
            "does not match the ledger snapshot",
        )


def _scope_covers(scope: list[str], edict_id: str, cell: str) -> bool:
    accepted = {
        edict_id,
        f"edict:{edict_id}",
        f"{edict_id}:{cell}",
        f"edict:{edict_id}:{cell}",
    }
    return any(item in accepted for item in scope)


def _validate_observation(
    observation: Any,
    path: str,
    report: ValidationReport,
    *,
    edict_ids: set[str] | None = None,
) -> tuple[str | None, str | None]:
    if not isinstance(observation, dict):
        report.error("invalid_observation", path, "must be an object")
        return None, None
    require_keys(
        observation,
        {
            "edict_id",
            "cell",
            "proposed_state",
            "claim",
            "evidence",
            "counterevidence",
            "disconfirmation",
            "confidence",
        },
        path,
        report,
    )
    if "id" in observation:
        _validate_string(
            observation.get("id"),
            f"{path}.id",
            report,
            identifier=True,
        )
    edict_id = observation.get("edict_id")
    cell = observation.get("cell")
    _validate_string(edict_id, f"{path}.edict_id", report, identifier=True)
    if edict_ids is not None and edict_id not in edict_ids:
        report.error(
            "unknown_edict",
            f"{path}.edict_id",
            f"references unknown edict {edict_id!r}",
        )
    if cell not in CELLS:
        report.error("invalid_cell", f"{path}.cell", f"must be one of {CELLS}")
    state = observation.get("proposed_state")
    if state not in CELL_STATES:
        report.error(
            "invalid_cell_state",
            f"{path}.proposed_state",
            f"must be one of {sorted(CELL_STATES)}",
        )
    _validate_string(observation.get("claim"), f"{path}.claim", report)
    _validate_evidence(
        observation.get("evidence"),
        f"{path}.evidence",
        report,
        required=state in {"SATISFIED", "UNSATISFIED"},
    )
    _validate_evidence(
        observation.get("counterevidence"),
        f"{path}.counterevidence",
        report,
    )
    _validate_string(
        observation.get("disconfirmation"),
        f"{path}.disconfirmation",
        report,
    )
    if observation.get("confidence") not in CONFIDENCE:
        report.error(
            "invalid_confidence",
            f"{path}.confidence",
            f"must be one of {sorted(CONFIDENCE)}",
        )
    return (
        edict_id if isinstance(edict_id, str) else None,
        cell if isinstance(cell, str) else None,
    )


def _validate_check(
    check: Any,
    path: str,
    report: ValidationReport,
    *,
    edict_ids: set[str] | None = None,
) -> datetime | None:
    if not isinstance(check, dict):
        report.error("invalid_check", path, "must be an object")
        return None
    require_keys(
        check,
        {
            "id",
            "executed_at",
            "profile",
            "tree",
            "target",
            "result",
            "totality",
            "skips",
            "warnings",
            "edict_ids",
            "evidence",
        },
        path,
        report,
    )
    _validate_string(check.get("id"), f"{path}.id", report, identifier=True)
    _validate_string(check.get("profile"), f"{path}.profile", report)
    _validate_string(check.get("tree"), f"{path}.tree", report)
    _validate_string(check.get("target"), f"{path}.target", report)
    when = parse_time(str(check.get("executed_at", "")))
    if when is None:
        report.error(
            "undated_check",
            f"{path}.executed_at",
            "must be a timezone-aware ISO-8601 time; move unorderable claims to undated_check_leads",
        )
    if check.get("result") not in RESULTS:
        report.error(
            "invalid_result",
            f"{path}.result",
            f"must be one of {sorted(RESULTS)}",
        )
    if check.get("totality") not in TOTALITIES:
        report.error(
            "invalid_totality",
            f"{path}.totality",
            f"must be one of {sorted(TOTALITIES)}",
        )
    skips = _validate_string_list(check.get("skips"), f"{path}.skips", report)
    _validate_string_list(check.get("warnings"), f"{path}.warnings", report)
    referenced = _validate_string_list(
        check.get("edict_ids"),
        f"{path}.edict_ids",
        report,
    )
    if edict_ids is not None:
        for index, edict_id in enumerate(referenced):
            if edict_id not in edict_ids:
                report.error(
                    "unknown_edict",
                    f"{path}.edict_ids[{index}]",
                    f"references unknown edict {edict_id!r}",
                )
    _validate_evidence(
        check.get("evidence"),
        f"{path}.evidence",
        report,
        required=check.get("totality") == "TOTAL",
    )
    if check.get("totality") == "TOTAL":
        if check.get("tree") in {None, "", "UNKNOWN"}:
            report.error(
                "unbound_total_check",
                f"{path}.tree",
                "TOTAL requires a known tree binding",
            )
        if check.get("result") == "UNKNOWN":
            report.error(
                "unknown_total_result",
                f"{path}.result",
                "TOTAL cannot have an UNKNOWN result",
            )
        if skips:
            report.warning(
                "total_check_has_skips",
                path,
                "TOTAL has skips; justify them explicitly or downgrade totality",
            )
    return when


def _validate_lead(lead: Any, path: str, report: ValidationReport) -> None:
    if not isinstance(lead, dict):
        report.error("invalid_check_lead", path, "must be an object")
        return
    require_keys(lead, {"id", "claim", "evidence"}, path, report)
    _validate_string(lead.get("id"), f"{path}.id", report, identifier=True)
    _validate_string(lead.get("claim"), f"{path}.claim", report)
    _validate_evidence(
        lead.get("evidence"),
        f"{path}.evidence",
        report,
        required=True,
    )
    if "missing" in lead:
        _validate_string_list(lead.get("missing"), f"{path}.missing", report)


def _validate_unknowns(value: Any, path: str, report: ValidationReport) -> None:
    if not isinstance(value, list):
        report.error("invalid_unknowns", path, "must be a list")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if isinstance(item, str):
            if not item.strip():
                report.error(
                    "invalid_unknown",
                    item_path,
                    "string unknown must not be empty",
                )
            else:
                report.warning(
                    "unstructured_unknown",
                    item_path,
                    "prefer an object with id, claim, blocker, and evidence_needed",
                )
        elif isinstance(item, dict):
            _validate_string(item.get("id"), f"{item_path}.id", report)
            _validate_string(item.get("claim"), f"{item_path}.claim", report)
            _validate_string(item.get("blocker"), f"{item_path}.blocker", report)
            _validate_string_list(
                item.get("evidence_needed"),
                f"{item_path}.evidence_needed",
                report,
                allow_empty=False,
            )
        else:
            report.error(
                "invalid_unknown",
                item_path,
                "must be a string or structured object",
            )


def validate_shard_report(
    shard: dict[str, Any],
    fingerprint: str | None = None,
    edict_ids: set[str] | None = None,
) -> ValidationReport:
    report = ValidationReport()
    require_keys(
        shard,
        {
            "schema_version",
            "agent_run",
            "observations",
            "checks",
            "undated_check_leads",
            "unknowns",
        },
        "shard",
        report,
    )
    if shard.get("schema_version") != SCHEMA_VERSION:
        report.error(
            "schema_version",
            "shard.schema_version",
            f"must be {SCHEMA_VERSION}",
        )
    run = shard.get("agent_run")
    _validate_agent_run(run, "shard.agent_run", report, fingerprint=fingerprint)
    scope = run.get("scope", []) if isinstance(run, dict) else []

    observations = shard.get("observations")
    seen_cells: set[tuple[str, str]] = set()
    if not isinstance(observations, list):
        report.error(
            "invalid_observations",
            "shard.observations",
            "must be a list",
        )
    else:
        for index, observation in enumerate(observations):
            edict_id, cell = _validate_observation(
                observation,
                f"shard.observations[{index}]",
                report,
                edict_ids=edict_ids,
            )
            if edict_id and cell:
                key = (edict_id, cell)
                if key in seen_cells:
                    report.error(
                        "duplicate_observation_cell",
                        f"shard.observations[{index}]",
                        f"duplicates {edict_id}:{cell}; use one observation per edict cell",
                    )
                seen_cells.add(key)
                if isinstance(scope, list) and not _scope_covers(
                    scope,
                    edict_id,
                    cell,
                ):
                    report.error(
                        "observation_outside_scope",
                        f"shard.observations[{index}]",
                        f"{edict_id}:{cell} is not declared in agent_run.scope",
                    )

    checks = shard.get("checks")
    if not isinstance(checks, list):
        report.error("invalid_checks", "shard.checks", "must be a list")
    else:
        check_ids: list[str] = []
        for index, check in enumerate(checks):
            _validate_check(
                check,
                f"shard.checks[{index}]",
                report,
                edict_ids=edict_ids,
            )
            if isinstance(check, dict) and _is_non_empty_string(check.get("id")):
                check_ids.append(check["id"])
        _report_duplicates(check_ids, "shard.checks", "check", report)

    leads = shard.get("undated_check_leads")
    if not isinstance(leads, list):
        report.error(
            "invalid_check_leads",
            "shard.undated_check_leads",
            "must be a list",
        )
    else:
        lead_ids: list[str] = []
        for index, lead in enumerate(leads):
            _validate_lead(
                lead,
                f"shard.undated_check_leads[{index}]",
                report,
            )
            if isinstance(lead, dict) and _is_non_empty_string(lead.get("id")):
                lead_ids.append(lead["id"])
        _report_duplicates(
            lead_ids,
            "shard.undated_check_leads",
            "check lead",
            report,
        )
    _validate_unknowns(shard.get("unknowns"), "shard.unknowns", report)
    return report


def validate_shard(
    shard: dict[str, Any],
    fingerprint: str | None = None,
    edict_ids: set[str] | None = None,
) -> list[str]:
    return validate_shard_report(shard, fingerprint, edict_ids).errors


def _report_duplicates(
    values: Iterable[str],
    path: str,
    label: str,
    report: ValidationReport,
) -> None:
    duplicates = sorted(
        value for value, count in Counter(values).items() if value and count > 1
    )
    if duplicates:
        report.error(
            f"duplicate_{label.replace(' ', '_')}_ids",
            path,
            f"duplicate {label} ids: {', '.join(duplicates)}",
        )


def _validate_scope(
    audit: dict[str, Any],
    report: ValidationReport,
    *,
    final: bool,
) -> None:
    if audit.get("mode") not in AUDIT_MODES:
        report.error(
            "invalid_audit_mode",
            "ledger.audit.mode",
            f"must be one of {sorted(AUDIT_MODES)}",
        )
    finish_lines = audit.get("finish_lines")
    _validate_string_list(
        finish_lines,
        "ledger.audit.finish_lines",
        report,
        allow_empty=not final,
    )
    scope = audit.get("scope_boundary")
    if not isinstance(scope, dict):
        report.error(
            "invalid_scope_boundary",
            "ledger.audit.scope_boundary",
            "must be an object",
        )
        return
    require_keys(
        scope,
        {
            "included",
            "excluded",
            "manifest_entries_total",
            "manifest_entries_read",
            "canonical_sources_exhausted",
            "notes",
        },
        "ledger.audit.scope_boundary",
        report,
    )
    _validate_string_list(
        scope.get("included"),
        "ledger.audit.scope_boundary.included",
        report,
    )
    _validate_string_list(
        scope.get("excluded"),
        "ledger.audit.scope_boundary.excluded",
        report,
    )
    _validate_string_list(
        scope.get("notes"),
        "ledger.audit.scope_boundary.notes",
        report,
    )
    total = scope.get("manifest_entries_total")
    read = scope.get("manifest_entries_read")
    if total is not None and (
        isinstance(total, bool) or not isinstance(total, int) or total < 0
    ):
        report.error(
            "invalid_manifest_total",
            "ledger.audit.scope_boundary.manifest_entries_total",
            "must be null or a non-negative integer",
        )
    if isinstance(read, bool) or not isinstance(read, int) or read < 0:
        report.error(
            "invalid_manifest_read",
            "ledger.audit.scope_boundary.manifest_entries_read",
            "must be a non-negative integer",
        )
    elif isinstance(total, int) and read > total:
        report.error(
            "manifest_read_exceeds_total",
            "ledger.audit.scope_boundary",
            "manifest_entries_read exceeds manifest_entries_total",
        )
    exhausted = scope.get("canonical_sources_exhausted")
    if not isinstance(exhausted, bool):
        report.error(
            "invalid_exhaustion_flag",
            "ledger.audit.scope_boundary.canonical_sources_exhausted",
            "must be a boolean",
        )
    if final and audit.get("mode") == "FULL":
        if not exhausted:
            report.error(
                "full_scope_not_exhausted",
                "ledger.audit.scope_boundary",
                "FULL requires canonical_sources_exhausted=true",
            )
        if total is None:
            report.error(
                "full_scope_unbounded",
                "ledger.audit.scope_boundary.manifest_entries_total",
                "FULL requires an explicit bounded source count; use 0 when no manifest exists",
            )
        elif isinstance(read, int) and read != total:
            report.error(
                "full_scope_incomplete",
                "ledger.audit.scope_boundary",
                "FULL requires every manifest entry to be read",
            )


def _validate_snapshot(
    snapshot: Any,
    report: ValidationReport,
    repo: Path | None,
) -> str | None:
    if not isinstance(snapshot, dict):
        report.error(
            "invalid_snapshot",
            "ledger.audit.snapshot",
            "must be an object",
        )
        return None
    require_keys(
        snapshot,
        {
            "repo",
            "fingerprint_version",
            "captured_at",
            "branch",
            "head",
            "dirty",
            "status",
            "disk_free_bytes",
            "fingerprint",
        },
        "ledger.audit.snapshot",
        report,
    )
    fingerprint = snapshot.get("fingerprint")
    _validate_string(
        fingerprint,
        "ledger.audit.snapshot.fingerprint",
        report,
    )
    if snapshot.get("fingerprint_version") != FINGERPRINT_VERSION:
        report.error(
            "fingerprint_version",
            "ledger.audit.snapshot.fingerprint_version",
            f"must be {FINGERPRINT_VERSION}; reinitialize the ledger",
        )
    if repo and _is_non_empty_string(fingerprint):
        try:
            current = repository_snapshot(repo)
        except LedgerError as exc:
            report.error(
                "snapshot_refresh_failed",
                "ledger.audit.snapshot",
                str(exc),
            )
        else:
            if Path(str(snapshot.get("repo", ""))).expanduser().resolve() != Path(
                current["repo"]
            ).resolve():
                report.error(
                    "repository_identity_mismatch",
                    "ledger.audit.snapshot.repo",
                    f"ledger is bound to {snapshot.get('repo')!r}, not {current['repo']!r}",
                )
            if current["fingerprint"] != fingerprint:
                report.error(
                    "repository_changed",
                    "ledger.audit.snapshot.fingerprint",
                    "repository snapshot changed after ledger initialization",
                )
    if snapshot.get("tool_errors"):
        report.warning(
            "snapshot_tool_errors",
            "ledger.audit.snapshot.tool_errors",
            "snapshot contains tool errors that cap exhaustive claims",
        )
    if snapshot.get("disk_free_bytes", 0) < 1024**3:
        report.warning(
            "low_disk_space",
            "ledger.audit.snapshot.disk_free_bytes",
            "repository filesystem had less than 1 GiB free",
        )
    return fingerprint if isinstance(fingerprint, str) else None


def _validate_sources(value: Any, path: str, report: ValidationReport) -> None:
    if not isinstance(value, list):
        report.error("invalid_sources", path, "must be a list")
        return
    if not value:
        report.error("missing_sources", path, "must not be empty")
    for index, source in enumerate(value):
        source_path = f"{path}[{index}]"
        if not isinstance(source, dict):
            report.error("invalid_source", source_path, "must be an object")
            continue
        locator = source.get("locator") or source.get("path")
        _validate_string(locator, f"{source_path}.locator", report)


def _method_quorum(methods: set[str]) -> tuple[bool, bool, bool]:
    normalized = {method.casefold() for method in methods}
    implementation = any(
        marker in method
        for method in normalized
        for marker in IMPLEMENTATION_METHOD_MARKERS
    )
    validation = any(
        marker in method
        for method in normalized
        for marker in VALIDATION_METHOD_MARKERS
    )
    adversarial = any(
        marker in method
        for method in normalized
        for marker in ADVERSARIAL_METHOD_MARKERS
    )
    return implementation, validation, adversarial


def _validate_obligations(
    obligations: Any,
    path: str,
    report: ValidationReport,
) -> tuple[list[str], set[str], set[str]]:
    states: list[str] = []
    methods: set[str] = set()
    agent_ids: set[str] = set()
    if not isinstance(obligations, dict):
        report.error("invalid_obligations", path, "must be an object")
        return states, methods, agent_ids
    missing = sorted(set(CELLS) - set(obligations))
    extra = sorted(set(obligations) - set(CELLS))
    if missing:
        report.error(
            "missing_obligation_cells",
            path,
            f"missing cells {', '.join(missing)}",
        )
    if extra:
        report.error(
            "unknown_obligation_cells",
            path,
            f"unknown cells {', '.join(extra)}",
        )
    for cell in CELLS:
        obligation = obligations.get(cell)
        cell_path = f"{path}.{cell}"
        if not isinstance(obligation, dict):
            if cell in obligations:
                report.error(
                    "invalid_obligation",
                    cell_path,
                    "must be an object",
                )
            continue
        require_keys(
            obligation,
            {
                "state",
                "evidence",
                "counterevidence",
                "methods",
                "agent_ids",
            },
            cell_path,
            report,
        )
        state = obligation.get("state")
        if state not in CELL_STATES:
            report.error(
                "invalid_cell_state",
                f"{cell_path}.state",
                f"must be one of {sorted(CELL_STATES)}",
            )
        elif state != "NA":
            states.append(state)
        _validate_evidence(
            obligation.get("evidence"),
            f"{cell_path}.evidence",
            report,
            required=state in {"SATISFIED", "UNSATISFIED"},
        )
        _validate_evidence(
            obligation.get("counterevidence"),
            f"{cell_path}.counterevidence",
            report,
        )
        methods.update(
            _validate_string_list(
                obligation.get("methods"),
                f"{cell_path}.methods",
                report,
            )
        )
        agent_ids.update(
            _validate_string_list(
                obligation.get("agent_ids"),
                f"{cell_path}.agent_ids",
                report,
            )
        )
    return states, methods, agent_ids


def _validate_disposition(
    edict: dict[str, Any],
    path: str,
    states: list[str],
    methods: set[str],
    agent_ids: set[str],
    report: ValidationReport,
    *,
    final: bool,
) -> None:
    disposition = edict.get("disposition")
    if disposition not in DISPOSITIONS:
        report.error(
            "invalid_disposition",
            f"{path}.disposition",
            f"must be one of {sorted(DISPOSITIONS)}",
        )
        return
    if final and disposition == "UNASSESSED":
        report.error(
            "unassessed_edict",
            f"{path}.disposition",
            "final validation forbids UNASSESSED",
        )
        return
    if disposition == "VERIFIED_COMPLETE":
        if not states:
            report.error(
                "no_applicable_obligations",
                f"{path}.obligations",
                "VERIFIED_COMPLETE requires at least one applicable obligation",
            )
        if any(state != "SATISFIED" for state in states):
            report.error(
                "incomplete_proof_vector",
                f"{path}.disposition",
                "VERIFIED_COMPLETE requires every applicable obligation SATISFIED",
            )
        if edict.get("risk") in {"CRITICAL", "HIGH"}:
            implementation, validation, adversarial = _method_quorum(methods)
            if len({method.casefold() for method in methods}) < 3:
                report.error(
                    "insufficient_independent_methods",
                    f"{path}.obligations",
                    "critical/high completion requires at least three distinct methods",
                )
            if not implementation:
                report.error(
                    "missing_implementation_method",
                    f"{path}.obligations",
                    "critical/high completion requires current implementation evidence",
                )
            if not validation:
                report.error(
                    "missing_validation_method",
                    f"{path}.obligations",
                    "critical/high completion requires focused validation or stronger target evidence",
                )
            if not adversarial:
                report.error(
                    "missing_adversarial_method",
                    f"{path}.obligations",
                    "critical/high completion requires fresh falsification",
                )
            if len(agent_ids) < 2:
                report.warning(
                    "single_agent_high_risk_quorum",
                    f"{path}.obligations",
                    "critical/high completion has fewer than two recorded independent agents",
                )
    elif disposition == "BLOCKED_UNVERIFIED" and "UNKNOWN" not in states:
        report.error(
            "blocked_without_unknown",
            f"{path}.disposition",
            "BLOCKED_UNVERIFIED requires an UNKNOWN obligation",
        )
    elif disposition == "PARTIAL":
        if "SATISFIED" not in states or not any(
            state in {"UNSATISFIED", "UNKNOWN"} for state in states
        ):
            report.warning(
                "weak_partial_classification",
                f"{path}.disposition",
                "PARTIAL normally requires both proven progress and an unresolved or unsatisfied applicable cell",
            )
    elif disposition == "MISSING" and "UNSATISFIED" not in states:
        report.error(
            "missing_without_unsatisfied",
            f"{path}.disposition",
            "MISSING requires at least one evidenced UNSATISFIED obligation",
        )
    elif disposition == "CONTRADICTED":
        obligations = edict.get("obligations", {})
        has_counterevidence = any(
            isinstance(item, dict) and item.get("counterevidence")
            for item in obligations.values()
        )
        if "UNSATISFIED" not in states or not has_counterevidence:
            report.error(
                "contradiction_without_counterevidence",
                f"{path}.disposition",
                "CONTRADICTED requires an UNSATISFIED cell and recorded counterevidence",
            )


def _validate_dependency_graph(
    edicts: list[Any],
    ids: set[str],
    report: ValidationReport,
) -> None:
    graph: dict[str, list[str]] = {}
    for index, edict in enumerate(edicts):
        if not isinstance(edict, dict) or not isinstance(edict.get("id"), str):
            continue
        dependencies = edict.get("dependencies")
        if not isinstance(dependencies, list):
            continue
        graph[edict["id"]] = [
            dependency
            for dependency in dependencies
            if isinstance(dependency, str)
        ]
        for dependency_index, dependency in enumerate(dependencies):
            path = f"ledger.edicts[{index}].dependencies[{dependency_index}]"
            if dependency == edict["id"]:
                report.error(
                    "self_dependency",
                    path,
                    "edict cannot depend on itself",
                )
            elif dependency not in ids:
                report.error(
                    "unknown_dependency",
                    path,
                    f"references unknown edict {dependency!r}",
                )

    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in active_set:
            start = active.index(node)
            cycle = active[start:] + [node]
            report.error(
                "dependency_cycle",
                "ledger.edicts",
                f"dependency cycle detected: {' -> '.join(cycle)}",
            )
            return
        active.append(node)
        active_set.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        active.pop()
        active_set.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def _validate_edicts(
    edicts: Any,
    report: ValidationReport,
    *,
    final: bool,
) -> set[str]:
    if not isinstance(edicts, list):
        report.error("invalid_edicts", "ledger.edicts", "must be a list")
        return set()
    if final and not edicts:
        report.error(
            "empty_edicts",
            "ledger.edicts",
            "must not be empty for final validation",
        )
    ids: list[str] = []
    for index, edict in enumerate(edicts):
        path = f"ledger.edicts[{index}]"
        if not isinstance(edict, dict):
            report.error("invalid_edict", path, "must be an object")
            continue
        require_keys(
            edict,
            {
                "id",
                "requirement",
                "sources",
                "dimension",
                "risk",
                "disposition",
                "obligations",
                "dependencies",
                "acceptance",
            },
            path,
            report,
        )
        edict_id = edict.get("id")
        _validate_string(edict_id, f"{path}.id", report, identifier=True)
        if isinstance(edict_id, str) and edict_id:
            ids.append(edict_id)
        _validate_string(
            edict.get("requirement"),
            f"{path}.requirement",
            report,
        )
        _validate_sources(edict.get("sources"), f"{path}.sources", report)
        _validate_string(edict.get("dimension"), f"{path}.dimension", report)
        if edict.get("risk") not in RISKS:
            report.error(
                "invalid_risk",
                f"{path}.risk",
                f"must be one of {sorted(RISKS)}",
            )
        _validate_string_list(
            edict.get("dependencies"),
            f"{path}.dependencies",
            report,
        )
        _validate_string_list(
            edict.get("acceptance"),
            f"{path}.acceptance",
            report,
            allow_empty=False,
        )
        states, methods, agent_ids = _validate_obligations(
            edict.get("obligations"),
            f"{path}.obligations",
            report,
        )
        _validate_disposition(
            edict,
            path,
            states,
            methods,
            agent_ids,
            report,
            final=final,
        )
    _report_duplicates(ids, "ledger.edicts", "edict", report)
    id_set = set(ids)
    _validate_dependency_graph(edicts, id_set, report)
    return id_set


def validate_ledger_report(
    ledger: dict[str, Any],
    repo: Path | None,
    *,
    final: bool = True,
) -> ValidationReport:
    report = ValidationReport()
    require_keys(
        ledger,
        {
            "schema_version",
            "audit",
            "edicts",
            "observations",
            "checks",
            "undated_check_leads",
            "unknowns",
            "agent_runs",
            "warnings",
        },
        "ledger",
        report,
    )
    if ledger.get("schema_version") != SCHEMA_VERSION:
        report.error(
            "schema_version",
            "ledger.schema_version",
            f"must be {SCHEMA_VERSION}",
        )
    engine = ledger.get("engine")
    if engine is None:
        report.warning(
            "legacy_engine_metadata",
            "ledger.engine",
            "missing engine metadata; ledger predates engine version 2",
        )
    elif not isinstance(engine, dict) or engine.get("version") != ENGINE_VERSION:
        report.warning(
            "engine_version",
            "ledger.engine",
            f"expected engine version {ENGINE_VERSION}",
        )

    audit = ledger.get("audit")
    if not isinstance(audit, dict):
        report.error("invalid_audit", "ledger.audit", "must be an object")
        audit = {}
    _validate_scope(audit, report, final=final)
    fingerprint = _validate_snapshot(audit.get("snapshot"), report, repo)
    edict_ids = _validate_edicts(ledger.get("edicts"), report, final=final)

    runs = ledger.get("agent_runs")
    run_ids: list[str] = []
    if not isinstance(runs, list):
        report.error(
            "invalid_agent_runs",
            "ledger.agent_runs",
            "must be a list",
        )
        runs = []
    for index, run in enumerate(runs):
        _validate_agent_run(
            run,
            f"ledger.agent_runs[{index}]",
            report,
            fingerprint=fingerprint,
        )
        if isinstance(run, dict) and _is_non_empty_string(run.get("id")):
            run_ids.append(run["id"])
    _report_duplicates(run_ids, "ledger.agent_runs", "agent run", report)
    run_id_set = set(run_ids)

    observations = ledger.get("observations")
    observation_ids: list[str] = []
    observation_edicts: dict[str, str] = {}
    observed_cells: set[tuple[str, str, str]] = set()
    if not isinstance(observations, list):
        report.error(
            "invalid_observations",
            "ledger.observations",
            "must be a list",
        )
        observations = []
    for index, observation in enumerate(observations):
        path = f"ledger.observations[{index}]"
        edict_id, cell = _validate_observation(
            observation,
            path,
            report,
            edict_ids=edict_ids,
        )
        if not isinstance(observation, dict):
            continue
        observation_id = observation.get("id")
        _validate_string(
            observation_id,
            f"{path}.id",
            report,
            identifier=True,
        )
        if isinstance(observation_id, str) and observation_id:
            observation_ids.append(observation_id)
            if edict_id:
                observation_edicts[observation_id] = edict_id
        run_id = observation.get("agent_run_id")
        _validate_string(
            run_id,
            f"{path}.agent_run_id",
            report,
            identifier=True,
        )
        if run_id not in run_id_set:
            report.error(
                "unknown_agent_run",
                f"{path}.agent_run_id",
                f"references unknown agent run {run_id!r}",
            )
        if isinstance(run_id, str) and edict_id and cell:
            key = (run_id, edict_id, cell)
            if key in observed_cells:
                report.error(
                    "duplicate_run_observation_cell",
                    path,
                    f"agent run {run_id} contains multiple observations for {edict_id}:{cell}",
                )
            observed_cells.add(key)
    _report_duplicates(
        observation_ids,
        "ledger.observations",
        "observation",
        report,
    )
    observation_id_set = set(observation_ids)

    for index, edict in enumerate(
        ledger.get("edicts") if isinstance(ledger.get("edicts"), list) else []
    ):
        if not isinstance(edict, dict):
            continue
        disposition = edict.get("disposition")
        if disposition in {None, "UNASSESSED"}:
            continue
        adjudication = edict.get("adjudication")
        path = f"ledger.edicts[{index}].adjudication"
        if not isinstance(adjudication, dict):
            report.error(
                "missing_adjudication",
                path,
                "assessed edict requires root adjudication provenance",
            )
            continue
        require_keys(
            adjudication,
            {"reason", "observation_ids", "adjudicated_at"},
            path,
            report,
        )
        _validate_string(adjudication.get("reason"), f"{path}.reason", report)
        references = _validate_string_list(
            adjudication.get("observation_ids"),
            f"{path}.observation_ids",
            report,
        )
        for reference_index, observation_id in enumerate(references):
            reference_path = f"{path}.observation_ids[{reference_index}]"
            if observation_id not in observation_id_set:
                report.error(
                    "unknown_observation",
                    reference_path,
                    f"references unknown observation {observation_id!r}",
                )
            elif observation_edicts.get(observation_id) != edict.get("id"):
                report.error(
                    "cross_edict_observation",
                    reference_path,
                    "references evidence for a different edict",
                )
        if (
            final
            and disposition
            not in {"OUT_OF_SCOPE", "SUPERSEDED", "BLOCKED_UNVERIFIED"}
            and not references
        ):
            report.warning(
                "adjudication_without_observations",
                path,
                "assessed edict has no merged observation references",
            )

    checks = ledger.get("checks")
    check_ids: list[str] = []
    dated: list[datetime] = []
    if not isinstance(checks, list):
        report.error("invalid_checks", "ledger.checks", "must be a list")
        checks = []
    if len(checks) > 10:
        report.error(
            "too_many_checks",
            "ledger.checks",
            "may contain at most the latest ten orderable completed runs",
        )
    for index, check in enumerate(checks):
        when = _validate_check(
            check,
            f"ledger.checks[{index}]",
            report,
            edict_ids=edict_ids,
        )
        if when is not None:
            dated.append(when)
        if isinstance(check, dict) and _is_non_empty_string(check.get("id")):
            check_ids.append(check["id"])
    _report_duplicates(check_ids, "ledger.checks", "check", report)
    if dated != sorted(dated, reverse=True):
        report.error(
            "checks_out_of_order",
            "ledger.checks",
            "must be sorted newest first",
        )
    if final and len(checks) < 10:
        report.warning(
            "latest_ten_incomplete",
            "ledger.checks",
            f"contains only {len(checks)}/10 orderable runs",
        )

    leads = ledger.get("undated_check_leads")
    lead_ids: list[str] = []
    if not isinstance(leads, list):
        report.error(
            "invalid_check_leads",
            "ledger.undated_check_leads",
            "must be a list",
        )
        leads = []
    for index, lead in enumerate(leads):
        _validate_lead(
            lead,
            f"ledger.undated_check_leads[{index}]",
            report,
        )
        if isinstance(lead, dict) and _is_non_empty_string(lead.get("id")):
            lead_ids.append(lead["id"])
    _report_duplicates(
        lead_ids,
        "ledger.undated_check_leads",
        "check lead",
        report,
    )
    _validate_unknowns(ledger.get("unknowns"), "ledger.unknowns", report)
    _validate_string_list(ledger.get("warnings"), "ledger.warnings", report)
    if audit.get("mode") == "DEGRADED":
        report.warning(
            "degraded_audit",
            "ledger.audit.mode",
            "coverage denominators are provisional",
        )
    return report


def validate_ledger(
    ledger: dict[str, Any],
    repo: Path | None,
) -> tuple[list[str], list[str]]:
    report = validate_ledger_report(ledger, repo)
    return report.errors, report.warnings


def _transaction(
    ledger: dict[str, Any],
    operation: Callable[[dict[str, Any]], None],
) -> None:
    candidate = copy.deepcopy(ledger)
    operation(candidate)
    ledger.clear()
    ledger.update(candidate)


def _edict_ids(ledger: dict[str, Any]) -> set[str]:
    return {
        edict["id"]
        for edict in ledger.get("edicts", [])
        if isinstance(edict, dict) and _is_non_empty_string(edict.get("id"))
    }


def _merge_checks(candidate: dict[str, Any], checks: list[dict[str, Any]]) -> None:
    existing = {
        item.get("id"): item
        for item in candidate.get("checks", [])
        if isinstance(item, dict) and item.get("id")
    }
    for check in checks:
        check_id = check["id"]
        if check_id in existing and existing[check_id] != check:
            raise LedgerError(f"conflicting check record: {check_id}")
        if check_id not in existing:
            candidate.setdefault("checks", []).append(copy.deepcopy(check))
            existing[check_id] = check
    candidate["checks"] = sorted(
        candidate.get("checks", []),
        key=lambda item: parse_time(str(item.get("executed_at", "")))
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:10]


def _merge_leads(candidate: dict[str, Any], leads: list[dict[str, Any]]) -> None:
    existing = {
        item.get("id"): item
        for item in candidate.get("undated_check_leads", [])
        if isinstance(item, dict) and item.get("id")
    }
    for lead in leads:
        lead_id = lead["id"]
        if lead_id in existing and existing[lead_id] != lead:
            raise LedgerError(f"conflicting undated check lead: {lead_id}")
        if lead_id not in existing:
            candidate.setdefault("undated_check_leads", []).append(
                copy.deepcopy(lead)
            )
            existing[lead_id] = lead


def merge_shard(ledger: dict[str, Any], shard: dict[str, Any]) -> None:
    fingerprint = (
        ledger.get("audit", {}).get("snapshot", {}).get("fingerprint")
    )
    report = validate_shard_report(
        shard,
        fingerprint,
        _edict_ids(ledger),
    )
    if report.errors:
        raise LedgerError("invalid shard:\n- " + "\n- ".join(report.errors))

    def apply(candidate: dict[str, Any]) -> None:
        run = copy.deepcopy(shard["agent_run"])
        run_id = run["id"]
        if any(
            isinstance(existing, dict) and existing.get("id") == run_id
            for existing in candidate.get("agent_runs", [])
        ):
            raise LedgerError(f"agent run id already merged: {run_id}")

        existing_observation_ids = {
            item.get("id")
            for item in candidate.get("observations", [])
            if isinstance(item, dict)
        }
        observations: list[dict[str, Any]] = []
        for index, observation in enumerate(shard.get("observations", [])):
            item = copy.deepcopy(observation)
            observation_id = item.get("id") or f"{run_id}:obs:{index + 1}"
            if observation_id in existing_observation_ids:
                raise LedgerError(
                    f"observation id already merged: {observation_id}"
                )
            item["id"] = observation_id
            item["agent_run_id"] = run_id
            item["method"] = run["method"]
            observations.append(item)
            existing_observation_ids.add(observation_id)

        candidate.setdefault("agent_runs", []).append(run)
        candidate.setdefault("observations", []).extend(observations)
        _merge_checks(candidate, shard.get("checks", []))
        _merge_leads(candidate, shard.get("undated_check_leads", []))
        for unknown in shard.get("unknowns", []):
            item = copy.deepcopy(unknown)
            if isinstance(item, dict):
                item.setdefault("agent_run_id", run_id)
            candidate.setdefault("unknowns", []).append(item)

    _transaction(ledger, apply)


def add_check_evidence(
    ledger: dict[str, Any],
    payload: dict[str, Any],
) -> None:
    checks = payload.get("checks", [])
    leads = payload.get("undated_check_leads", [])
    if not isinstance(checks, list) or not isinstance(leads, list):
        raise LedgerError("check-evidence payload fields must be lists")
    report = ValidationReport()
    edict_ids = _edict_ids(ledger)
    for index, check in enumerate(checks):
        _validate_check(
            check,
            f"payload.checks[{index}]",
            report,
            edict_ids=edict_ids,
        )
    for index, lead in enumerate(leads):
        _validate_lead(
            lead,
            f"payload.undated_check_leads[{index}]",
            report,
        )
    if report.errors:
        raise LedgerError(
            "invalid check evidence:\n- " + "\n- ".join(report.errors)
        )

    def apply(candidate: dict[str, Any]) -> None:
        _merge_checks(candidate, checks)
        _merge_leads(candidate, leads)

    _transaction(ledger, apply)


def seed_edicts(ledger: dict[str, Any], payload: dict[str, Any]) -> None:
    if ledger.get("edicts"):
        raise LedgerError(
            "ledger already contains edicts; seed is intentionally one-time"
        )
    edicts = payload.get("edicts")
    if not isinstance(edicts, list) or not edicts:
        raise LedgerError("seed payload requires a non-empty edicts list")
    candidate_edicts = copy.deepcopy(edicts)
    for edict in candidate_edicts:
        if isinstance(edict, dict):
            edict.setdefault("disposition", "UNASSESSED")
    report = ValidationReport()
    _validate_edicts(candidate_edicts, report, final=False)
    audit_candidate = copy.deepcopy(ledger.get("audit", {}))
    for key in ("mode", "finish_lines", "scope_boundary"):
        if key in payload:
            audit_candidate[key] = copy.deepcopy(payload[key])
    _validate_scope(audit_candidate, report, final=False)
    if report.errors:
        raise LedgerError("invalid edict seed:\n- " + "\n- ".join(report.errors))

    def apply(candidate: dict[str, Any]) -> None:
        candidate["edicts"] = candidate_edicts
        audit = candidate.setdefault("audit", {})
        for key in ("mode", "finish_lines", "scope_boundary"):
            if key in payload:
                audit[key] = copy.deepcopy(payload[key])

    _transaction(ledger, apply)


def adjudicate(ledger: dict[str, Any], payload: dict[str, Any]) -> None:
    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        raise LedgerError(
            "adjudication payload requires a non-empty decisions list"
        )
    by_id = {
        item.get("id"): item
        for item in ledger.get("edicts", [])
        if isinstance(item, dict) and item.get("id")
    }
    observation_edicts = {
        item.get("id"): item.get("edict_id")
        for item in ledger.get("observations", [])
        if isinstance(item, dict) and item.get("id")
    }
    seen: set[str] = set()
    prepared: list[dict[str, Any]] = []
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            raise LedgerError(f"decision {index} must be an object")
        edict_id = decision.get("edict_id")
        if edict_id not in by_id:
            raise LedgerError(f"decision references unknown edict: {edict_id}")
        if edict_id in seen:
            raise LedgerError(f"duplicate decision for edict: {edict_id}")
        seen.add(edict_id)
        disposition = decision.get("disposition")
        if disposition not in DISPOSITIONS - {"UNASSESSED"}:
            raise LedgerError(
                f"invalid final disposition for {edict_id}: {disposition}"
            )
        if not _is_non_empty_string(decision.get("reason")):
            raise LedgerError(f"decision {edict_id} requires a non-empty reason")
        obligations = decision.get("obligations")
        if not isinstance(obligations, dict):
            raise LedgerError(f"decision {edict_id} requires obligations")
        references = decision.get("observation_ids", [])
        if not isinstance(references, list) or any(
            not _is_non_empty_string(item) for item in references
        ):
            raise LedgerError(
                f"decision {edict_id}.observation_ids must be a list of strings"
            )
        for observation_id in references:
            if observation_id not in observation_edicts:
                raise LedgerError(
                    f"decision {edict_id} references unknown observation {observation_id}"
                )
            if observation_edicts[observation_id] != edict_id:
                raise LedgerError(
                    f"decision {edict_id} references observation for "
                    f"{observation_edicts[observation_id]}"
                )
        prepared.append(copy.deepcopy(decision))

    def apply(candidate: dict[str, Any]) -> None:
        candidate_by_id = {
            item.get("id"): item
            for item in candidate.get("edicts", [])
            if isinstance(item, dict) and item.get("id")
        }
        adjudicated_at = _now()
        for decision in prepared:
            edict_id = decision["edict_id"]
            target = candidate_by_id[edict_id]
            target["disposition"] = decision["disposition"]
            target["obligations"] = decision["obligations"]
            target["adjudication"] = {
                "reason": decision["reason"],
                "observation_ids": decision.get("observation_ids", []),
                "adjudicated_at": adjudicated_at,
            }
            for key in ("acceptance", "dependencies"):
                if key in decision:
                    target[key] = decision[key]
        report = ValidationReport()
        _validate_edicts(candidate.get("edicts"), report, final=False)
        if report.errors:
            raise LedgerError(
                "invalid adjudication:\n- " + "\n- ".join(report.errors)
            )

    _transaction(ledger, apply)


def _coverage_ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "ratio": None if denominator == 0 else round(numerator / denominator, 4),
    }


def _edict_methods(edict: dict[str, Any]) -> set[str]:
    methods: set[str] = set()
    obligations = edict.get("obligations", {})
    if isinstance(obligations, dict):
        for obligation in obligations.values():
            if isinstance(obligation, dict):
                methods.update(
                    str(item)
                    for item in obligation.get("methods", [])
                    if item
                )
    return methods


def summary(ledger: dict[str, Any]) -> dict[str, Any]:
    validation_report = validate_ledger_report(ledger, None)
    edicts = [
        edict
        for edict in ledger.get("edicts", [])
        if isinstance(edict, dict)
    ]
    disposition_counts = Counter(
        edict.get("disposition", "UNSET") for edict in edicts
    )
    risk_counts = Counter(edict.get("risk", "UNSET") for edict in edicts)
    dimension_counts: dict[str, Counter[str]] = {}
    cell_counts = Counter()
    implementation_traced = 0
    validated = 0
    high_risk_quorum = 0
    high_risk_total = 0
    blockers: list[str] = []

    for edict in edicts:
        dimension = str(edict.get("dimension", "UNSET"))
        dimension_counts.setdefault(dimension, Counter())[
            str(edict.get("disposition", "UNSET"))
        ] += 1
        obligations = edict.get("obligations", {})
        if not isinstance(obligations, dict):
            continue
        for obligation in obligations.values():
            if isinstance(obligation, dict):
                cell_counts[str(obligation.get("state", "UNSET"))] += 1
        trace_states = [
            obligations.get(cell, {}).get("state")
            for cell in ("CONTRACT", "MOUNT", "IMPLEMENT")
            if isinstance(obligations.get(cell), dict)
            and obligations.get(cell, {}).get("state") != "NA"
        ]
        if trace_states and all(state == "SATISFIED" for state in trace_states):
            implementation_traced += 1
        test_state = (
            obligations.get("TEST", {}).get("state")
            if isinstance(obligations.get("TEST"), dict)
            else None
        )
        if test_state in {"SATISFIED", "NA"}:
            validated += 1
        if edict.get("risk") in {"CRITICAL", "HIGH"}:
            high_risk_total += 1
            methods = _edict_methods(edict)
            if all(_method_quorum(methods)):
                high_risk_quorum += 1
        if edict.get("disposition") not in {
            "VERIFIED_COMPLETE",
            "OUT_OF_SCOPE",
            "SUPERSEDED",
        }:
            blockers.append(str(edict.get("id")))

    assessed = len(edicts) - disposition_counts.get("UNASSESSED", 0)
    completed = disposition_counts.get("VERIFIED_COMPLETE", 0)
    applicable_cells = sum(
        count
        for state, count in cell_counts.items()
        if state not in {"NA", "UNSET"}
    )
    satisfied_cells = cell_counts.get("SATISFIED", 0)
    ready = (
        not validation_report.errors
        and ledger.get("audit", {}).get("mode") == "FULL"
        and assessed == len(edicts)
        and not blockers
        and cell_counts.get("UNKNOWN", 0) == 0
        and cell_counts.get("UNSATISFIED", 0) == 0
        and high_risk_quorum == high_risk_total
        and not ledger.get("unknowns")
    )
    not_ready_reasons: list[str] = []
    if ledger.get("audit", {}).get("mode") != "FULL":
        not_ready_reasons.append("audit mode is not FULL")
    if assessed != len(edicts):
        not_ready_reasons.append("one or more edicts are unassessed")
    if blockers:
        not_ready_reasons.append("one or more edicts remain incomplete")
    if cell_counts.get("UNKNOWN", 0):
        not_ready_reasons.append("unknown proof-obligation cells remain")
    if cell_counts.get("UNSATISFIED", 0):
        not_ready_reasons.append("unsatisfied proof-obligation cells remain")
    if high_risk_quorum != high_risk_total:
        not_ready_reasons.append("critical/high independent quorum is incomplete")
    if ledger.get("unknowns"):
        not_ready_reasons.append("ledger unknowns remain")

    checks = [
        check
        for check in ledger.get("checks", [])
        if isinstance(check, dict)
    ]
    return {
        "engine_version": ledger.get("engine", {}).get("version"),
        "ledger_valid": not validation_report.errors,
        "validation_error_count": len(validation_report.errors),
        "validation_errors": validation_report.errors,
        "mode": ledger.get("audit", {}).get("mode"),
        "snapshot_fingerprint": ledger.get("audit", {})
        .get("snapshot", {})
        .get("fingerprint"),
        "edicts": len(edicts),
        "dispositions": dict(sorted(disposition_counts.items())),
        "risks": dict(sorted(risk_counts.items())),
        "dimensions": {
            dimension: dict(sorted(counts.items()))
            for dimension, counts in sorted(dimension_counts.items())
        },
        "proof_cells": dict(sorted(cell_counts.items())),
        "coverage": {
            "edict_disposition": _coverage_ratio(assessed, len(edicts)),
            "verified_complete": _coverage_ratio(completed, len(edicts)),
            "applicable_cells_satisfied": _coverage_ratio(
                satisfied_cells,
                applicable_cells,
            ),
            "implementation_trace": _coverage_ratio(
                implementation_traced,
                len(edicts),
            ),
            "current_validation": _coverage_ratio(validated, len(edicts)),
            "critical_high_independent_quorum": _coverage_ratio(
                high_risk_quorum,
                high_risk_total,
            ),
            "latest_ten": _coverage_ratio(len(checks), 10),
        },
        "critical_high_not_complete": [
            edict.get("id")
            for edict in edicts
            if edict.get("risk") in {"CRITICAL", "HIGH"}
            and edict.get("disposition") != "VERIFIED_COMPLETE"
        ],
        "remaining_edict_ids": blockers,
        "unknown_obligation_cells": cell_counts.get("UNKNOWN", 0),
        "contradictions": disposition_counts.get("CONTRADICTED", 0),
        "agent_runs": len(ledger.get("agent_runs", [])),
        "observations": len(ledger.get("observations", [])),
        "latest_checks": len(checks),
        "check_results": dict(
            sorted(Counter(check.get("result", "UNSET") for check in checks).items())
        ),
        "check_totality": dict(
            sorted(
                Counter(check.get("totality", "UNSET") for check in checks).items()
            )
        ),
        "undated_check_leads": len(ledger.get("undated_check_leads", [])),
        "unknowns": len(ledger.get("unknowns", [])),
        "ready_for_full_completion_claim": ready,
        "not_ready_reasons": [] if ready else not_ready_reasons,
    }


def schema_contract() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "engine_version": ENGINE_VERSION,
        "fingerprint_version": FINGERPRINT_VERSION,
        "cells": list(CELLS),
        "cell_states": sorted(CELL_STATES),
        "dispositions": sorted(DISPOSITIONS),
        "risks": sorted(RISKS),
        "check_results": sorted(RESULTS),
        "check_totalities": sorted(TOTALITIES),
        "confidence": sorted(CONFIDENCE),
        "commands": [
            "init",
            "fingerprint",
            "seed-edicts",
            "validate-shard",
            "merge-shard",
            "add-check-evidence",
            "adjudicate",
            "validate",
            "summary",
            "schema",
            "self-test",
        ],
    }


def _sample_obligations(
    state: str = "UNKNOWN",
    *,
    method: str = "",
    agent_id: str = "",
) -> dict[str, Any]:
    return {
        cell: {
            "state": state if cell == "IMPLEMENT" else "NA",
            "evidence": (
                [
                    {
                        "kind": "source",
                        "locator": "sample.txt:1",
                        "note": "Current source contains the sample requirement; it does not prove deployment.",
                    }
                ]
                if cell == "IMPLEMENT" and state in {"SATISFIED", "UNSATISFIED"}
                else []
            ),
            "counterevidence": [],
            "methods": [method] if cell == "IMPLEMENT" and method else [],
            "agent_ids": [agent_id] if cell == "IMPLEMENT" and agent_id else [],
        }
        for cell in CELLS
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="opium-self-test-") as directory:
        repo = Path(directory) / "repo"
        repo.mkdir()
        run_git(repo, "init", "-q")
        run_git(repo, "config", "user.email", "opium@example.invalid")
        run_git(repo, "config", "user.name", "Opium Self Test")
        (repo / "sample.txt").write_text("sample\n", encoding="utf-8")
        run_git(repo, "add", "sample.txt")
        run_git(repo, "commit", "-qm", "sample")

        ledger = new_ledger(repo)
        seed_edicts(
            ledger,
            {
                "mode": "DEGRADED",
                "finish_lines": ["current source behavior"],
                "scope_boundary": {
                    "included": ["sample.txt"],
                    "excluded": [],
                    "manifest_entries_total": 1,
                    "manifest_entries_read": 1,
                    "canonical_sources_exhausted": True,
                    "notes": ["self-test"],
                },
                "edicts": [
                    {
                        "id": "E-001",
                        "requirement": "Sample requirement",
                        "sources": [{"path": "sample.txt", "line": 1}],
                        "dimension": "runtime/source",
                        "risk": "LOW",
                        "dependencies": [],
                        "acceptance": ["sample exists"],
                        "obligations": _sample_obligations(),
                    }
                ],
            },
        )
        fingerprint = ledger["audit"]["snapshot"]["fingerprint"]
        shard = {
            "schema_version": SCHEMA_VERSION,
            "agent_run": {
                "id": "self-test",
                "snapshot_fingerprint": fingerprint,
                "model": "self-test",
                "reasoning_effort": "none",
                "scope": ["edict:E-001:IMPLEMENT"],
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
                    "evidence": [
                        {
                            "kind": "source",
                            "locator": "sample.txt:1",
                            "note": "The sample file exists on the captured tree.",
                        }
                    ],
                    "counterevidence": [],
                    "disconfirmation": "The source observation does not prove a deployed target.",
                    "confidence": "HIGH",
                }
            ],
            "checks": [],
            "undated_check_leads": [],
            "unknowns": [],
        }
        merge_shard(ledger, shard)
        observation_id = ledger["observations"][0]["id"]
        add_check_evidence(
            ledger,
            {
                "checks": [],
                "undated_check_leads": [
                    {
                        "id": "lead-1",
                        "claim": "reported sample check",
                        "evidence": [
                            {
                                "kind": "source",
                                "locator": "sample.txt:1",
                                "note": "A report exists, but has no execution provenance.",
                            }
                        ],
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
                        "obligations": _sample_obligations(
                            "SATISFIED",
                            method="source_trace",
                            agent_id="self-test",
                        ),
                        "reason": "Current source directly satisfies the bounded requirement.",
                        "observation_ids": [observation_id],
                    }
                ]
            },
        )
        report = validate_ledger_report(ledger, repo)
        if report.errors:
            raise LedgerError(
                "self-test validation failed:\n- " + "\n- ".join(report.errors)
            )
        if not report.warnings:
            raise LedgerError("self-test expected bounded-audit warnings")
        result = summary(ledger)
        if result["agent_runs"] != 1 or result["undated_check_leads"] != 1:
            raise LedgerError("self-test summary mismatch")

        before = copy.deepcopy(ledger)
        bad_shard = copy.deepcopy(shard)
        bad_shard["agent_run"]["id"] = "bad-shard"
        bad_shard["agent_run"]["snapshot_fingerprint"] = "stale"
        try:
            merge_shard(ledger, bad_shard)
        except LedgerError:
            pass
        else:
            raise LedgerError("self-test expected stale shard rejection")
        if ledger != before:
            raise LedgerError("failed shard merge mutated the ledger")
    print("audit_ledger.py self-test passed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize a ledger")
    init_parser.add_argument("--repo", type=Path, required=True)
    init_parser.add_argument("--out", type=Path, required=True)

    fingerprint_parser = subparsers.add_parser(
        "fingerprint",
        help="print a repository snapshot",
    )
    fingerprint_parser.add_argument("--repo", type=Path, required=True)

    merge_parser = subparsers.add_parser(
        "merge-shard",
        help="validate and atomically merge an agent shard",
    )
    merge_parser.add_argument("--ledger", type=Path, required=True)
    merge_parser.add_argument("--shard", type=Path, required=True)

    shard_parser = subparsers.add_parser(
        "validate-shard",
        help="validate a shard without mutating a ledger",
    )
    shard_parser.add_argument("--shard", type=Path, required=True)
    shard_parser.add_argument("--ledger", type=Path)
    shard_parser.add_argument("--json", action="store_true")

    seed_parser = subparsers.add_parser(
        "seed-edicts",
        help="seed the bounded edict universe once",
    )
    seed_parser.add_argument("--ledger", type=Path, required=True)
    seed_parser.add_argument("--input", type=Path, required=True)

    adjudicate_parser = subparsers.add_parser(
        "adjudicate",
        help="apply root-owned final edict decisions atomically",
    )
    adjudicate_parser.add_argument("--ledger", type=Path, required=True)
    adjudicate_parser.add_argument("--input", type=Path, required=True)

    checks_parser = subparsers.add_parser(
        "add-check-evidence",
        help="add ordered checks and undated leads atomically",
    )
    checks_parser.add_argument("--ledger", type=Path, required=True)
    checks_parser.add_argument("--input", type=Path, required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="validate a final ledger",
    )
    validate_parser.add_argument("--ledger", type=Path, required=True)
    validate_parser.add_argument("--repo", type=Path)
    validate_parser.add_argument("--json", action="store_true")

    summary_parser = subparsers.add_parser(
        "summary",
        help="print coverage and readiness summary",
    )
    summary_parser.add_argument("--ledger", type=Path, required=True)

    subparsers.add_parser("schema", help="print the engine schema contract")
    subparsers.add_parser("self-test", help="run deterministic smoke tests")
    return parser


def _print_report(report: ValidationReport, as_json: bool) -> int:
    if as_json:
        print(json.dumps(report.to_json(), indent=2, sort_keys=True))
    else:
        for warning in report.warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        for error in report.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if not report.errors:
            print("validation passed")
    return 2 if report.errors else 0


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            atomic_write(args.out, new_ledger(args.repo))
            print(args.out)
        elif args.command == "fingerprint":
            print(
                json.dumps(
                    repository_snapshot(args.repo),
                    indent=2,
                    sort_keys=True,
                )
            )
        elif args.command == "merge-shard":
            ledger = load_json(args.ledger)
            merge_shard(ledger, load_json(args.shard))
            atomic_write(args.ledger, ledger)
            print(args.ledger)
        elif args.command == "validate-shard":
            shard = load_json(args.shard)
            fingerprint = None
            edict_ids = None
            if args.ledger:
                ledger = load_json(args.ledger)
                fingerprint = (
                    ledger.get("audit", {})
                    .get("snapshot", {})
                    .get("fingerprint")
                )
                edict_ids = _edict_ids(ledger)
            return _print_report(
                validate_shard_report(shard, fingerprint, edict_ids),
                args.json,
            )
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
            return _print_report(
                validate_ledger_report(
                    load_json(args.ledger),
                    args.repo,
                ),
                args.json,
            )
        elif args.command == "summary":
            print(
                json.dumps(
                    summary(load_json(args.ledger)),
                    indent=2,
                    sort_keys=True,
                )
            )
        elif args.command == "schema":
            print(json.dumps(schema_contract(), indent=2, sort_keys=True))
        elif args.command == "self-test":
            self_test()
        return 0
    except LedgerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
