"""Temporary Repair-1 route assembly wrapper for the canonical local diagnostic.

This wrapper is intentionally scoped to the audit packet. It implements the
approved route assembly policy without changing baseline adapter source:

- original exact rows replay the Direct LLM original candidate;
- original mismatch/candidate-execution-failed rows invoke Repair-1 once;
- original unsupported rows preserve the unsupported boundary without a repair
  call.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ORIGINAL_RUN_ID = "direct_llm_original_track_a_120_canonical_v0"
ROUTE_ID = "direct_llm_repair_1"
METHOD_ID = "direct_llm_repair_1"
ORIGINAL_ROUTE_ID = "direct_llm_original"
ORIGINAL_METHOD_ID = "direct_llm_original"
REPAIR_PROMPT_TEMPLATE_ID = "direct_llm_repair_1_feedback_sql_only_v0"
EXTRACTION_POLICY_ID = "single_sql_candidate_repair_v0"
REPAIRABLE_BUCKETS = {"mismatch", "candidate_execution_failed"}
UNSUPPORTED_BUCKET = "unsupported_engine"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _repo_root() -> Path:
    return Path.cwd()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing required env: {name}")
    return value


def _original_ledger_row(repo_root: Path, case_id: str, engine: str) -> dict[str, str]:
    ledger_path = repo_root / "runs" / "user" / f"{ORIGINAL_RUN_ID}__{engine}" / "ledger.csv"
    if not ledger_path.exists():
        raise RuntimeError(f"original Direct LLM ledger missing: {ledger_path}")
    matches = [
        row
        for row in _read_csv(ledger_path)
        if row.get("case_id") == case_id and row.get("engine") == engine
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one original ledger row for {case_id}/{engine}, found {len(matches)}")
    return matches[0]


def _status_base(env: dict[str, str], original_row: dict[str, str], original_candidate_path: Path) -> dict[str, Any]:
    return {
        "schema_version": "direct_llm_repair_1_route_assembly_status_v0",
        "created_at_utc": _utc_now_iso(),
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        "original_route_id": ORIGINAL_ROUTE_ID,
        "original_method_id": ORIGINAL_METHOD_ID,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "original_run_id": ORIGINAL_RUN_ID,
        "original_candidate_id": _original_candidate_id(env["SQLRB_CASE_ID"], env["SQLRB_ENGINE"]),
        "original_candidate_path": original_candidate_path.as_posix(),
        "original_candidate_sql_sha256": _sha256_file(original_candidate_path)
        if original_candidate_path.exists()
        else "",
        "original_failure_bucket": original_row.get("failure_bucket", ""),
        "original_exact_status": original_row.get("exact_status", ""),
        "repair_attempted": False,
        "live_call": False,
        "feedback_type": "",
        "repair_prompt_template_id": REPAIR_PROMPT_TEMPLATE_ID,
        "repaired_candidate_id": "",
        "repaired_candidate_generated": False,
        "final_candidate_source": "",
        "final_status": "",
        "extraction_policy": EXTRACTION_POLICY_ID,
        "extraction_status": "not_attempted",
        "failure_bucket": "none",
        "failure_reason": "",
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
        "secret_redaction_policy": "no secrets written",
    }


def _original_candidate_id(case_id: str, engine: str) -> str:
    return f"{ORIGINAL_RUN_ID}:{case_id}:{engine}:direct_llm_original"


def _copy_candidate(src: Path, dst: Path) -> None:
    if not src.exists() or not src.read_text(encoding="utf-8").strip():
        raise RuntimeError(f"candidate SQL missing or empty: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def _bool_text(value: str) -> bool | None:
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    return None


def _feedback_type(original_bucket: str) -> str:
    if original_bucket == "mismatch":
        return "checker_mismatch_feedback"
    if original_bucket == "candidate_execution_failed":
        return "candidate_execution_error_feedback"
    if original_bucket == "unsupported_engine":
        return "unsupported_engine_boundary_feedback"
    return original_bucket


def _feedback_summary(row: dict[str, str]) -> str:
    bucket = row.get("failure_bucket", "")
    if bucket == "mismatch":
        return (
            "Original Direct LLM candidate executed successfully but failed the local result checker. "
            f"checker_status={row.get('checker_status', '')}; exact_status={row.get('exact_status', '')}; "
            f"mismatch_artifact_path={row.get('mismatch_artifact_path', '') or '<unavailable>'}."
        )
    if bucket == "candidate_execution_failed":
        return (
            "Original Direct LLM candidate failed local candidate execution before checker comparison. "
            f"execution_status={row.get('execution_status', '')}; "
            f"candidate_execution_status={row.get('candidate_execution_status', '')}; "
            f"execution_failure_class={row.get('execution_failure_class', '') or '<unavailable>'}."
        )
    if bucket == "unsupported_engine":
        return "Original row is an unsupported-engine boundary row and is excluded from Repair-1 attempts."
    return f"Original Direct LLM failure bucket: {bucket or '<none>'}."


def _write_feedback(workspace: Path, env: dict[str, str], original_row: dict[str, str]) -> Path:
    bucket = original_row.get("failure_bucket", "")
    payload = {
        "schema_version": "direct_llm_repair_1_feedback_v0",
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "original_run_id": ORIGINAL_RUN_ID,
        "original_candidate_id": _original_candidate_id(env["SQLRB_CASE_ID"], env["SQLRB_ENGINE"]),
        "feedback_type": _feedback_type(bucket),
        "failure_bucket": bucket,
        "source_executable": _bool_text(original_row.get("source_execution_status") == "source_execution_success"),
        "candidate_executable": _bool_text(original_row.get("candidate_execution_status") == "candidate_execution_success"),
        "checker_attempted": original_row.get("checker_status") not in {"", "checker_not_enabled", "non_db"},
        "exact_status": original_row.get("exact_status", ""),
        "checker_or_error_summary": _feedback_summary(original_row),
        "normalized_execution_error_class": original_row.get("execution_failure_class", ""),
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result": False,
    }
    feedback_path = workspace / "repair1_feedback.json"
    _write_json(feedback_path, payload)
    return feedback_path


def _run_repair_adapter(env: dict[str, str], original_candidate_path: Path, feedback_path: Path) -> int:
    child_env = dict(os.environ)
    child_env.update(
        {
            "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH": original_candidate_path.as_posix(),
            "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID": _original_candidate_id(
                env["SQLRB_CASE_ID"], env["SQLRB_ENGINE"]
            ),
            "SQLRB_REPAIR1_ORIGINAL_RUN_ID": ORIGINAL_RUN_ID,
            "SQLRB_REPAIR1_FEEDBACK_PATH": feedback_path.as_posix(),
        }
    )
    child_env.pop("SQLRB_LLM_FAKE_RESPONSE", None)
    child_env.pop("SQLRB_REPAIR1_FAKE_RESPONSE", None)
    completed = subprocess.run(
        [sys.executable, "baselines/direct_llm_repair_1/adapter.py"],
        cwd=_repo_root(),
        env=child_env,
        text=True,
        capture_output=True,
        timeout=float(os.environ.get("SQLRB_REPAIR1_CHILD_TIMEOUT", "120")),
        check=False,
    )
    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    (workspace / "repair1_child_stdout.txt").write_text(completed.stdout or "", encoding="utf-8")
    (workspace / "repair1_child_stderr.txt").write_text(completed.stderr or "", encoding="utf-8")
    if completed.stdout:
        print(completed.stdout.strip())
    if completed.returncode != 0:
        status = {
            "schema_version": "direct_llm_repair_1_route_assembly_status_v0",
            "created_at_utc": _utc_now_iso(),
            "route_id": ROUTE_ID,
            "method_id": METHOD_ID,
            "case_id": env["SQLRB_CASE_ID"],
            "engine": env["SQLRB_ENGINE"],
            "repair_attempted": True,
            "live_call": True,
            "final_candidate_source": "fail_closed",
            "final_status": "repair_adapter_failed",
            "failure_bucket": "adapter_failed",
            "failure_reason": "Repair-1 child adapter exited non-zero; stderr captured in workspace.",
            "local_diagnostic_only": True,
            "official_metric_input": False,
            "paper_result": False,
        }
        _write_json(workspace / "direct_llm_repair_1_route_assembly_status.json", status)
    return completed.returncode


def main() -> int:
    env = {name: _env(name) for name in [
        "SQLRB_RUN_ID",
        "SQLRB_CASE_ID",
        "SQLRB_POOL",
        "SQLRB_ENGINE",
        "SQLRB_SOURCE_SQL_PATH",
        "SQLRB_WORKSPACE_DIR",
        "SQLRB_CANDIDATE_SQL_PATH",
    ]}
    repo_root = _repo_root()
    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    workspace.mkdir(parents=True, exist_ok=True)
    original_row = _original_ledger_row(repo_root, env["SQLRB_CASE_ID"], env["SQLRB_ENGINE"])
    original_candidate_rel = original_row.get("candidate_sql_path", "")
    original_candidate_path = repo_root / original_candidate_rel
    status = _status_base(env, original_row, original_candidate_path)
    original_bucket = original_row.get("failure_bucket", "")
    original_exact = original_row.get("exact_status", "")
    candidate_dst = Path(env["SQLRB_CANDIDATE_SQL_PATH"])

    if original_bucket == "none" and original_exact == "exact":
        _copy_candidate(original_candidate_path, candidate_dst)
        status.update(
            {
                "final_candidate_source": "original",
                "final_status": "original_exact_replayed",
                "candidate_generated": True,
                "extraction_status": "original_candidate_replayed",
            }
        )
        _write_json(workspace / "direct_llm_repair_1_route_assembly_status.json", status)
        print(f"{ROUTE_ID}: replayed original exact candidate for {env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}")
        return 0

    if original_bucket in REPAIRABLE_BUCKETS:
        feedback_path = _write_feedback(workspace, env, original_row)
        status.update(
            {
                "repair_attempted": True,
                "live_call": True,
                "feedback_type": _feedback_type(original_bucket),
                "repaired_candidate_id": f"{_original_candidate_id(env['SQLRB_CASE_ID'], env['SQLRB_ENGINE'])}:repair_1",
                "final_candidate_source": "repaired",
                "final_status": "repair_attempt_dispatched",
            }
        )
        _write_json(workspace / "direct_llm_repair_1_route_assembly_status.json", status)
        return _run_repair_adapter(env, original_candidate_path, feedback_path)

    if original_bucket == UNSUPPORTED_BUCKET:
        # Preserve a candidate artifact so the user facade reaches the
        # unsupported diagnostic mode and records unsupported_engine, while row
        # metadata keeps the final source categorized as unsupported_or_none.
        _copy_candidate(original_candidate_path, candidate_dst)
        status.update(
            {
                "final_candidate_source": "unsupported_or_none",
                "final_status": "unsupported_engine_boundary_preserved",
                "candidate_generated": True,
                "extraction_status": "unsupported_boundary_artifact_replayed",
                "failure_bucket": "unsupported_engine",
                "failure_reason": "Repair-1 not attempted for unsupported_engine boundary row.",
            }
        )
        _write_json(workspace / "direct_llm_repair_1_route_assembly_status.json", status)
        print(f"{ROUTE_ID}: preserved unsupported boundary for {env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}")
        return 0

    status.update(
        {
            "final_candidate_source": "fail_closed",
            "final_status": "unsupported_original_bucket",
            "failure_bucket": original_bucket or "no_candidate_sql",
            "failure_reason": "Original Direct LLM row is not eligible for Repair-1 under the approved policy.",
        }
    )
    _write_json(workspace / "direct_llm_repair_1_route_assembly_status.json", status)
    print(f"{ROUTE_ID}: fail closed for {env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
