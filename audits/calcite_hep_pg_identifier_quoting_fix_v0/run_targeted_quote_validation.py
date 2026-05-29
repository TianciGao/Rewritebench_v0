#!/usr/bin/env python3
"""Targeted Calcite HEP PostgreSQL identifier-quoting validation helper.

This helper is audit-local. It invokes the D035-compliant Calcite adapter only
for the rows classified as identifier-quoting blockers, then executes/checks
only rows with generated candidate SQL. Runtime artifacts are written under the
caller-provided /tmp root; committed outputs are limited to audit CSV/JSON.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.adapter_runner import run_adapter_for_case  # noqa: E402
from sql_rewrite_bench.case_package_resolver import resolve_case_package  # noqa: E402
from sql_rewrite_bench.case_selection import resolve_common_core_selection  # noqa: E402
from sql_rewrite_bench.local_result_checker import run_local_checker  # noqa: E402
from sql_rewrite_bench.postgres_execution import execute_postgres_case  # noqa: E402


AUDIT_DIR = Path(__file__).resolve().parent
FRONTIER_CSV = REPO_ROOT / "audits/calcite_hep_pg_frontier_blocker_triage_v0/frontier_inventory.csv"
PRIOR_GENERATION_CSV = (
    REPO_ROOT / "audits/calcite_hep_pg_bounded_candidate_generation_v0/per_row_candidate_status.csv"
)
PRIOR_EXECUTION_CSV = (
    REPO_ROOT
    / "audits/calcite_hep_pg_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv"
)
ADAPTER = REPO_ROOT / "baselines/calcite_hep_fail_closed/adapter.py"
TARGET_CASES = [
    "PORT_0003",
    "PORT_0005",
    "PORT_0008",
    "PORT_0012",
    "CONS_0036",
    "CONS_0037",
    "LONGTAIL_0011",
    "LONGTAIL_0012",
    "LONGTAIL_0013",
]


TARGET_FIELDS = [
    "case_id",
    "pool",
    "prior_stage_status",
    "candidate_origin",
    "primary_category",
    "secondary_category",
    "safe_next_action",
    "targeted_action",
    "validation_scope",
]

STATUS_FIELDS = [
    "case_id",
    "pool",
    "prior_stage_status",
    "prior_generation_status",
    "prior_candidate_executable",
    "prior_checker_status",
    "prior_exact",
    "after_generation_status",
    "after_candidate_origin",
    "after_candidate_generated",
    "generated_sql_changed_by_postprocess",
    "postprocess_replacement_count",
    "postprocess_replacement_identifiers",
    "after_source_executable",
    "after_candidate_executable",
    "after_checker_attempted",
    "after_checker_status",
    "after_exact",
    "after_mismatch",
    "after_failure_bucket",
    "after_candidate_sql_sha256",
    "after_candidate_sql_path",
    "checker_output_trace",
    "mismatch_artifact_path",
    "improvement_status",
    "regressed",
    "local_only",
    "official_metric_input",
    "paper_result",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _sha256(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _parse_key_value_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    parsed: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _load_status(workspace: Path) -> dict[str, object]:
    path = workspace / "calcite_hep_status.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _after_origin(stdout_payload: dict[str, str], generated: bool) -> str:
    if not generated:
        return "no_candidate"
    if stdout_payload.get("emission_mode") == "calcite_parse_only":
        return "calcite_parse_only_schema_fallback"
    return "calcite_rel_to_sql"


def _improvement_status(
    *,
    prior: dict[str, str],
    after_generated: bool,
    after_candidate_executable: bool,
    after_exact: bool,
    after_failure_bucket: str,
) -> str:
    prior_stage = prior.get("prior_stage_status", "")
    prior_exact = prior.get("prior_exact", "false") == "true"
    prior_candidate_executable = prior.get("prior_candidate_executable", "false") == "true"
    if after_exact and not prior_exact:
        return "improved_to_exact"
    if after_candidate_executable and not prior_candidate_executable:
        return "improved_to_candidate_executable"
    if not after_generated and "no_candidate" in prior_stage:
        return "unchanged_no_candidate"
    if after_failure_bucket != "none":
        return f"still_blocked_{after_failure_bucket}"
    return "unchanged"


def _summary(rows: list[dict[str, str]], *, run_id: str, output_root: Path) -> dict[str, object]:
    after_generated = sum(row["after_candidate_generated"] == "true" for row in rows)
    after_source_ok = sum(row["after_source_executable"] == "true" for row in rows)
    after_candidate_ok = sum(row["after_candidate_executable"] == "true" for row in rows)
    after_exact = sum(row["after_exact"] == "true" for row in rows)
    improved_exact = sum(row["improvement_status"] == "improved_to_exact" for row in rows)
    improved_candidate = sum(
        row["improvement_status"] == "improved_to_candidate_executable" for row in rows
    )
    return {
        "schema_version": "calcite_pg_identifier_quoting_fix_validation_summary_v0",
        "run_id": run_id,
        "output_root": output_root.as_posix(),
        "target_rows": len(rows),
        "after_candidate_generated_rows": after_generated,
        "after_source_executable_rows": after_source_ok,
        "after_candidate_executable_rows": after_candidate_ok,
        "after_exact_rows": after_exact,
        "improved_to_exact_rows": improved_exact,
        "improved_to_candidate_executable_rows": improved_candidate,
        "regressed_rows": sum(row["regressed"] == "true" for row in rows),
        "after_failure_bucket_counts": dict(
            sorted(Counter(row["after_failure_bucket"] for row in rows).items())
        ),
        "improvement_status_counts": dict(
            sorted(Counter(row["improvement_status"] for row in rows).items())
        ),
        "timing_collected": False,
        "verifier_run": False,
        "official_metric_input": False,
        "paper_result": False,
        "local_only": True,
    }


def run(args: argparse.Namespace) -> int:
    frontier_rows = {row["case_id"]: row for row in _read_csv(FRONTIER_CSV)}
    generation_rows = {row["case_id"]: row for row in _read_csv(PRIOR_GENERATION_CSV)}
    execution_rows = {row["case_id"]: row for row in _read_csv(PRIOR_EXECUTION_CSV)}
    selected_rows = {
        row.case_id: row
        for row in resolve_common_core_selection(
            repo_root=REPO_ROOT,
            case_set="common_core_v0",
            pool="all",
            engine="postgres",
            case_list=None,
            smoke=False,
        )
    }

    result_root = args.output_root / "output" / "results" / args.run_id
    log_root = args.output_root / "output" / "logs" / args.run_id
    report_root = args.output_root / "output" / "reports" / args.run_id
    for path in (result_root, log_root, report_root):
        path.mkdir(parents=True, exist_ok=True)

    target_rows: list[dict[str, str]] = []
    status_rows: list[dict[str, str]] = []
    for case_id in TARGET_CASES:
        frontier = frontier_rows[case_id]
        target_rows.append(
            {
                "case_id": case_id,
                "pool": frontier["pool"],
                "prior_stage_status": frontier["prior_stage_status"],
                "candidate_origin": frontier["candidate_origin"],
                "primary_category": frontier["primary_category"],
                "secondary_category": frontier["secondary_category"],
                "safe_next_action": frontier["safe_next_action"],
                "targeted_action": "postgres_identifier_quote_postprocess",
                "validation_scope": "generation_and_execution_checker_if_generated",
            }
        )

        row = selected_rows[case_id]
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        adapter_result = run_adapter_for_case(
            run_id=args.run_id,
            row=row,
            resolved_package=resolved,
            adapter_command=f"{sys.executable} {ADAPTER}",
            repo_root=REPO_ROOT,
            out_dir=result_root,
            timeout=args.adapter_timeout_sec,
        )
        workspace = adapter_result.workspace_dir
        status = _load_status(workspace)
        stdout_payload = _parse_key_value_file(workspace / "calcite_hep_runtime_stdout.txt")
        postprocess = status.get("candidate_postprocess")
        if not isinstance(postprocess, dict):
            postprocess = {}

        execution = None
        checker = None
        failure_bucket = adapter_result.failure_bucket_hint
        if adapter_result.candidate_generated and adapter_result.candidate_sql_path is not None:
            execution = execute_postgres_case(
                repo_root=REPO_ROOT,
                run_id=args.run_id,
                row=row,
                candidate_sql_path=adapter_result.candidate_sql_path,
                workspace_dir=workspace,
                timeout_sec=args.execution_timeout_sec,
                schema_prefix=args.db_schema_prefix,
                dsn_env=args.postgres_dsn_env,
            )
            failure_bucket = execution.failure_bucket
            if (
                execution.source_result_path is not None
                and execution.candidate_result_path is not None
                and execution.failure_bucket == "none"
            ):
                checker = run_local_checker(
                    case_dir=REPO_ROOT / row.case_path,
                    source_result_path=execution.source_result_path,
                    candidate_result_path=execution.candidate_result_path,
                    checker_dir=workspace / "checker",
                    enable_cross_dialect_normalization=False,
                    enable_mixed_numeric_equivalence=False,
                )
                failure_bucket = checker.failure_bucket

        source_status = execution.source_execution_status if execution else "not_attempted"
        candidate_status = execution.candidate_execution_status if execution else "not_attempted"
        checker_status = checker.checker_status if checker else "not_attempted"
        after_source_ok = source_status == "source_execution_success"
        after_candidate_ok = candidate_status == "candidate_execution_success"
        after_exact = checker is not None and checker.exact_status == "exact"
        after_mismatch = checker is not None and checker.exact_status == "mismatch"
        prior_execution = execution_rows.get(case_id, {})
        prior = {
            "prior_stage_status": frontier["prior_stage_status"],
            "prior_exact": prior_execution.get("exact", "false"),
            "prior_candidate_executable": prior_execution.get("candidate_executable", "false"),
        }
        improvement = _improvement_status(
            prior=prior,
            after_generated=adapter_result.candidate_generated,
            after_candidate_executable=after_candidate_ok,
            after_exact=after_exact,
            after_failure_bucket=failure_bucket,
        )
        regressed = (
            prior_execution.get("exact") == "true" and not after_exact
        ) or (
            prior_execution.get("candidate_executable") == "true"
            and not after_candidate_ok
            and adapter_result.candidate_generated
        )
        replacements = postprocess.get("replacement_identifiers", {})
        status_rows.append(
            {
                "case_id": case_id,
                "pool": frontier["pool"],
                "prior_stage_status": frontier["prior_stage_status"],
                "prior_generation_status": generation_rows.get(case_id, {}).get(
                    "candidate_generated", "false"
                ),
                "prior_candidate_executable": prior_execution.get("candidate_executable", "false"),
                "prior_checker_status": prior_execution.get("checker_status", "not_attempted"),
                "prior_exact": prior_execution.get("exact", "false"),
                "after_generation_status": status.get("preflight_status", adapter_result.adapter_status),
                "after_candidate_origin": _after_origin(
                    stdout_payload, adapter_result.candidate_generated
                ),
                "after_candidate_generated": _bool(adapter_result.candidate_generated),
                "generated_sql_changed_by_postprocess": _bool(bool(postprocess.get("changed"))),
                "postprocess_replacement_count": str(postprocess.get("replacement_count", 0)),
                "postprocess_replacement_identifiers": json.dumps(
                    replacements, sort_keys=True, separators=(",", ":")
                ),
                "after_source_executable": _bool(after_source_ok),
                "after_candidate_executable": _bool(after_candidate_ok),
                "after_checker_attempted": _bool(checker is not None),
                "after_checker_status": checker_status,
                "after_exact": _bool(after_exact),
                "after_mismatch": _bool(after_mismatch),
                "after_failure_bucket": failure_bucket,
                "after_candidate_sql_sha256": _sha256(adapter_result.candidate_sql_path),
                "after_candidate_sql_path": _rel(adapter_result.candidate_sql_path),
                "checker_output_trace": _rel(workspace / "checker" / "checker_result.json")
                if checker
                else "",
                "mismatch_artifact_path": _rel(checker.mismatch_artifact_path)
                if checker and checker.mismatch_artifact_path
                else "",
                "improvement_status": improvement,
                "regressed": _bool(regressed),
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )

    _write_csv(AUDIT_DIR / "target_rows.csv", target_rows, TARGET_FIELDS)
    _write_csv(AUDIT_DIR / "before_after_status.csv", status_rows, STATUS_FIELDS)
    summary = _summary(status_rows, run_id=args.run_id, output_root=args.output_root)
    (AUDIT_DIR / "targeted_validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (log_root / "run_config.json").write_text(
        json.dumps(vars(args), indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    (report_root / "README.md").write_text(
        "# Calcite HEP PostgreSQL identifier quoting validation\n\n"
        "Runtime artifacts for this local diagnostic helper only.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--run-id", default="calcite_hep_pg_identifier_quoting_fix")
    parser.add_argument("--adapter-timeout-sec", type=int, default=40)
    parser.add_argument("--execution-timeout-sec", type=int, default=40)
    parser.add_argument("--db-schema-prefix", default="sqlrb_calcite_quote_fix")
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
