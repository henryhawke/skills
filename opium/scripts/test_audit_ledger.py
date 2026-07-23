#!/usr/bin/env python3
"""Regression tests for the Opium audit ledger engine."""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import audit_ledger as engine


def evidence(locator: str = "sample.txt:1") -> list[dict[str, str]]:
    return [
        {
            "kind": "source",
            "locator": locator,
            "note": "Bounded test evidence; it does not prove a deployed target.",
        }
    ]


def obligations(
    implement_state: str = "UNKNOWN",
    *,
    methods: list[str] | None = None,
    agent_ids: list[str] | None = None,
) -> dict[str, dict[str, object]]:
    return {
        cell: {
            "state": implement_state if cell == "IMPLEMENT" else "NA",
            "evidence": (
                evidence()
                if cell == "IMPLEMENT"
                and implement_state in {"SATISFIED", "UNSATISFIED"}
                else []
            ),
            "counterevidence": [],
            "methods": list(methods or []) if cell == "IMPLEMENT" else [],
            "agent_ids": list(agent_ids or []) if cell == "IMPLEMENT" else [],
        }
        for cell in engine.CELLS
    }


def edict(
    edict_id: str,
    *,
    risk: str = "LOW",
    dependencies: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": edict_id,
        "requirement": f"Requirement {edict_id}",
        "sources": [{"path": "sample.txt", "line": 1}],
        "dimension": "runtime/source",
        "risk": risk,
        "dependencies": list(dependencies or []),
        "acceptance": ["sample remains observable"],
        "obligations": obligations(),
    }


def scope(mode: str = "DEGRADED") -> dict[str, object]:
    return {
        "mode": mode,
        "finish_lines": ["current source behavior"],
        "scope_boundary": {
            "included": ["sample.txt"],
            "excluded": [],
            "manifest_entries_total": 1,
            "manifest_entries_read": 1,
            "canonical_sources_exhausted": True,
            "notes": [],
        },
    }


def shard(
    ledger: dict[str, object],
    *,
    run_id: str = "run-1",
    edict_id: str = "E-001",
    cell: str = "IMPLEMENT",
    state: str = "SATISFIED",
) -> dict[str, object]:
    return {
        "schema_version": engine.SCHEMA_VERSION,
        "agent_run": {
            "id": run_id,
            "snapshot_fingerprint": ledger["audit"]["snapshot"]["fingerprint"],
            "model": "test-model",
            "reasoning_effort": "test",
            "scope": [f"edict:{edict_id}:{cell}"],
            "method": "source_trace",
            "exclusions": [],
            "tool_limits": [],
        },
        "observations": [
            {
                "edict_id": edict_id,
                "cell": cell,
                "proposed_state": state,
                "claim": "The sample is present.",
                "evidence": (
                    evidence() if state in {"SATISFIED", "UNSATISFIED"} else []
                ),
                "counterevidence": [],
                "disconfirmation": "A source trace does not prove deployment.",
                "confidence": "HIGH",
            }
        ],
        "checks": [],
        "undated_check_leads": [],
        "unknowns": [],
    }


def check(
    check_id: str,
    executed_at: datetime,
    *,
    edict_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": check_id,
        "executed_at": executed_at.isoformat(),
        "profile": "python -m unittest",
        "tree": "test-tree clean",
        "target": "local",
        "result": "PASS",
        "totality": "TOTAL",
        "skips": [],
        "warnings": [],
        "edict_ids": list(edict_ids or ["E-001"]),
        "evidence": evidence("test-output:1"),
    }


class AuditLedgerEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="opium-engine-test-")
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        engine.run_git(self.repo, "init", "-q")
        engine.run_git(
            self.repo,
            "config",
            "user.email",
            "opium-tests@example.invalid",
        )
        engine.run_git(
            self.repo,
            "config",
            "user.name",
            "Opium Tests",
        )
        (self.repo / "sample.txt").write_text("sample\n", encoding="utf-8")
        engine.run_git(self.repo, "add", "sample.txt")
        engine.run_git(self.repo, "commit", "-qm", "sample")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_ledger(
        self,
        edicts: list[dict[str, object]] | None = None,
        *,
        mode: str = "DEGRADED",
    ) -> dict[str, object]:
        ledger = engine.new_ledger(self.repo)
        payload = scope(mode)
        payload["edicts"] = edicts or [edict("E-001")]
        engine.seed_edicts(ledger, payload)
        return ledger

    def test_snapshot_fingerprint_tracks_untracked_content(self) -> None:
        initial = engine.repository_snapshot(self.repo)
        untracked = self.repo / "untracked.txt"
        untracked.write_text("one\n", encoding="utf-8")
        first = engine.repository_snapshot(self.repo)
        untracked.write_text("two\n", encoding="utf-8")
        second = engine.repository_snapshot(self.repo)

        self.assertNotEqual(initial["fingerprint"], first["fingerprint"])
        self.assertNotEqual(first["fingerprint"], second["fingerprint"])
        self.assertEqual(first["untracked"][0]["path"], "untracked.txt")
        self.assertNotEqual(
            first["untracked"][0]["sha256"],
            second["untracked"][0]["sha256"],
        )

    def test_snapshot_separates_staged_and_unstaged_digests(self) -> None:
        path = self.repo / "sample.txt"
        path.write_text("staged\n", encoding="utf-8")
        engine.run_git(self.repo, "add", "sample.txt")
        staged = engine.repository_snapshot(self.repo)
        path.write_text("unstaged\n", encoding="utf-8")
        mixed = engine.repository_snapshot(self.repo)

        self.assertEqual(
            staged["staged_diff_sha256"],
            mixed["staged_diff_sha256"],
        )
        self.assertNotEqual(
            staged["unstaged_diff_sha256"],
            mixed["unstaged_diff_sha256"],
        )

    def test_load_json_rejects_duplicate_keys(self) -> None:
        path = self.root / "duplicate.json"
        path.write_text('{"schema_version": 1, "schema_version": 2}\n')
        with self.assertRaisesRegex(engine.LedgerError, "duplicate object key"):
            engine.load_json(path)

    def test_shard_rejects_unknown_edict_and_scope_mismatch(self) -> None:
        ledger = self.make_ledger()
        payload = shard(ledger, edict_id="E-999")
        report = engine.validate_shard_report(
            payload,
            ledger["audit"]["snapshot"]["fingerprint"],
            {"E-001"},
        )
        self.assertTrue(
            any(issue.code == "unknown_edict" for issue in report.issues)
        )

        payload["observations"][0]["edict_id"] = "E-001"
        report = engine.validate_shard_report(
            payload,
            ledger["audit"]["snapshot"]["fingerprint"],
            {"E-001"},
        )
        self.assertTrue(
            any(
                issue.code == "observation_outside_scope"
                for issue in report.issues
            )
        )

    def test_shard_rejects_duplicate_observation_cell(self) -> None:
        ledger = self.make_ledger()
        payload = shard(ledger)
        payload["observations"].append(copy.deepcopy(payload["observations"][0]))
        report = engine.validate_shard_report(
            payload,
            ledger["audit"]["snapshot"]["fingerprint"],
            {"E-001"},
        )
        self.assertTrue(
            any(
                issue.code == "duplicate_observation_cell"
                for issue in report.issues
            )
        )

    def test_merge_assigns_stable_observation_provenance(self) -> None:
        ledger = self.make_ledger()
        engine.merge_shard(ledger, shard(ledger))
        observation = ledger["observations"][0]
        self.assertEqual(observation["id"], "run-1:obs:1")
        self.assertEqual(observation["agent_run_id"], "run-1")
        self.assertEqual(observation["method"], "source_trace")

    def test_failed_shard_merge_is_transactional(self) -> None:
        ledger = self.make_ledger()
        before = copy.deepcopy(ledger)
        payload = shard(ledger)
        payload["agent_run"]["snapshot_fingerprint"] = "stale"
        with self.assertRaises(engine.LedgerError):
            engine.merge_shard(ledger, payload)
        self.assertEqual(ledger, before)

    def test_failed_check_import_is_transactional(self) -> None:
        ledger = self.make_ledger()
        before = copy.deepcopy(ledger)
        payload = {
            "checks": [
                check(
                    "check-1",
                    datetime.now(timezone.utc),
                )
            ],
            "undated_check_leads": [
                {
                    "id": "broken-lead",
                    "claim": "Missing evidence",
                    "evidence": [],
                }
            ],
        }
        with self.assertRaises(engine.LedgerError):
            engine.add_check_evidence(ledger, payload)
        self.assertEqual(ledger, before)

    def test_check_import_keeps_latest_ten_in_order(self) -> None:
        ledger = self.make_ledger()
        now = datetime.now(timezone.utc)
        checks = [
            check(f"check-{index}", now - timedelta(minutes=index))
            for index in range(12)
        ]
        engine.add_check_evidence(
            ledger,
            {"checks": list(reversed(checks)), "undated_check_leads": []},
        )
        self.assertEqual(len(ledger["checks"]), 10)
        self.assertEqual(ledger["checks"][0]["id"], "check-0")
        self.assertEqual(ledger["checks"][-1]["id"], "check-9")

    def test_check_rejects_unknown_edict_reference(self) -> None:
        ledger = self.make_ledger()
        payload = {
            "checks": [
                check(
                    "check-1",
                    datetime.now(timezone.utc),
                    edict_ids=["E-999"],
                )
            ],
            "undated_check_leads": [],
        }
        with self.assertRaisesRegex(engine.LedgerError, "unknown edict"):
            engine.add_check_evidence(ledger, payload)

    def test_seed_rejects_dependency_cycle_transactionally(self) -> None:
        ledger = engine.new_ledger(self.repo)
        before = copy.deepcopy(ledger)
        payload = scope()
        payload["edicts"] = [
            edict("E-001", dependencies=["E-002"]),
            edict("E-002", dependencies=["E-001"]),
        ]
        with self.assertRaisesRegex(engine.LedgerError, "dependency cycle"):
            engine.seed_edicts(ledger, payload)
        self.assertEqual(ledger, before)

    def test_adjudication_rejects_weak_high_risk_quorum(self) -> None:
        ledger = self.make_ledger([edict("E-001", risk="HIGH")])
        engine.merge_shard(ledger, shard(ledger))
        before = copy.deepcopy(ledger)
        decision = {
            "decisions": [
                {
                    "edict_id": "E-001",
                    "disposition": "VERIFIED_COMPLETE",
                    "obligations": obligations(
                        "SATISFIED",
                        methods=["source_trace"],
                        agent_ids=["run-1"],
                    ),
                    "reason": "Insufficient high-risk proof.",
                    "observation_ids": ["run-1:obs:1"],
                }
            ]
        }
        with self.assertRaisesRegex(
            engine.LedgerError,
            "three distinct methods",
        ):
            engine.adjudicate(ledger, decision)
        self.assertEqual(ledger, before)

    def test_adjudication_is_transactional_across_multiple_decisions(self) -> None:
        ledger = self.make_ledger([edict("E-001"), edict("E-002")])
        before = copy.deepcopy(ledger)
        payload = {
            "decisions": [
                {
                    "edict_id": "E-001",
                    "disposition": "BLOCKED_UNVERIFIED",
                    "obligations": obligations(),
                    "reason": "External target unavailable.",
                    "observation_ids": [],
                },
                {
                    "edict_id": "E-002",
                    "disposition": "BLOCKED_UNVERIFIED",
                    "obligations": obligations(),
                    "reason": "",
                    "observation_ids": [],
                },
            ]
        }
        with self.assertRaisesRegex(engine.LedgerError, "non-empty reason"):
            engine.adjudicate(ledger, payload)
        self.assertEqual(ledger, before)

    def test_full_validation_requires_bounded_scope(self) -> None:
        ledger = self.make_ledger(mode="FULL")
        ledger["audit"]["scope_boundary"]["manifest_entries_total"] = None
        report = engine.validate_ledger_report(ledger, None)
        self.assertTrue(
            any(issue.code == "full_scope_unbounded" for issue in report.issues)
        )
        self.assertFalse(engine.summary(ledger)["ready_for_full_completion_claim"])

    def test_validation_detects_repository_drift(self) -> None:
        ledger = self.make_ledger()
        (self.repo / "sample.txt").write_text("changed\n", encoding="utf-8")
        report = engine.validate_ledger_report(ledger, self.repo, final=False)
        self.assertTrue(
            any(issue.code == "repository_changed" for issue in report.issues)
        )

    def test_valid_workflow_and_summary(self) -> None:
        ledger = self.make_ledger()
        engine.merge_shard(ledger, shard(ledger))
        engine.adjudicate(
            ledger,
            {
                "decisions": [
                    {
                        "edict_id": "E-001",
                        "disposition": "VERIFIED_COMPLETE",
                        "obligations": obligations(
                            "SATISFIED",
                            methods=["source_trace"],
                            agent_ids=["run-1"],
                        ),
                        "reason": "The bounded source requirement is satisfied.",
                        "observation_ids": ["run-1:obs:1"],
                    }
                ]
            },
        )
        report = engine.validate_ledger_report(ledger, self.repo)
        self.assertFalse(report.errors)
        result = engine.summary(ledger)
        self.assertEqual(
            result["coverage"]["edict_disposition"]["numerator"],
            1,
        )
        self.assertEqual(
            result["coverage"]["applicable_cells_satisfied"]["ratio"],
            1.0,
        )
        self.assertFalse(result["ready_for_full_completion_claim"])
        self.assertIn("audit mode is not FULL", result["not_ready_reasons"])

    def test_schema_contract_lists_preflight_command(self) -> None:
        contract = engine.schema_contract()
        self.assertEqual(contract["engine_version"], engine.ENGINE_VERSION)
        self.assertIn("validate-shard", contract["commands"])
        json.dumps(contract, allow_nan=False)

    def test_skill_resources_are_linked_and_executable(self) -> None:
        skill_root = Path(engine.__file__).resolve().parent.parent
        documents = [
            skill_root / "SKILL.md",
            skill_root / "references" / "ledger-engine.md",
        ]
        for document in documents:
            for target in re.findall(
                r"\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)",
                document.read_text(encoding="utf-8"),
            ):
                resolved = (document.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"{document} references missing resource {target}",
                )
        self.assertTrue(os.access(engine.__file__, os.X_OK))

    def test_cli_schema_and_shard_json_validation(self) -> None:
        schema_process = subprocess.run(
            [sys.executable, engine.__file__, "schema"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(schema_process.returncode, 0, schema_process.stderr)
        self.assertEqual(
            json.loads(schema_process.stdout)["engine_version"],
            engine.ENGINE_VERSION,
        )

        ledger = self.make_ledger()
        ledger_path = self.root / "ledger.json"
        shard_path = self.root / "shard.json"
        engine.atomic_write(ledger_path, ledger)
        engine.atomic_write(shard_path, shard(ledger))
        validation_process = subprocess.run(
            [
                sys.executable,
                engine.__file__,
                "validate-shard",
                "--ledger",
                str(ledger_path),
                "--shard",
                str(shard_path),
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            validation_process.returncode,
            0,
            validation_process.stderr,
        )
        self.assertTrue(json.loads(validation_process.stdout)["valid"])

        final_process = subprocess.run(
            [
                sys.executable,
                engine.__file__,
                "validate",
                "--ledger",
                str(ledger_path),
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(final_process.returncode, 2)
        self.assertFalse(json.loads(final_process.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
