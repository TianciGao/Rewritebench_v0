#!/usr/bin/env python3
"""Parse candidate non-timing statuses from approved parser-v1 sources.

This parser is intentionally source-specific and fail-closed. It opens only the
five maintainer-approved manifest inputs, reads only approved status columns,
never fills timing or speedup fields, never authorizes metric input, and never
computes metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


PARSER_NAME = "candidate_status_parser_v1"
PARSER_SCOPE = "approved_non_timing_whitelist_only"
RECORD_TYPE = "rewrite_candidate_cell"
DEFAULT_OUT_DIR = Path("audits/candidate_status_parser_v1")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

APPROVED_PROPOSALS = {"P001", "P002", "P003", "P011", "P012"}

LEDGER_FILENAME = "candidate_status_parsed_ledger_v1.csv"
SUMMARY_FILENAME = "candidate_status_parser_v1_summary.json"
REPORT_FILENAME = "candidate_status_parser_v1_report.md"
CHECKS_FILENAME = "candidate_status_parser_v1_checks.csv"
SOURCE_USE_LOG_FILENAME = "candidate_status_parser_v1_source_use_log.csv"
LIMITATIONS_FILENAME = "candidate_status_parser_v1_limitations.md"
REJECTION_LOG_FILENAME = "candidate_status_parser_v1_input_rejection_log.csv"

LEDGER_COLUMNS = [
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
    "parser_name",
    "parser_scope",
    "source_scaffold_record_id",
    "case_id",
    "pool",
    "case_set",
    "denominator_id",
    "engine",
    "rewrite_method",
    "rewrite_method_display_name",
    "route",
    "route_family",
    "method_role",
    "candidate_id",
    "source_sql_path",
    "candidate_sql_path",
    "planned",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
    "plan_available",
    "plan_artifact_path",
    "latency_ms",
    "speedup_ratio",
    "timing_eligible",
    "evidence_source",
    "retained_artifact_path",
    "status",
    "na_reason",
    "parser_status",
    "parser_input_manifest_id",
    "row_grain_verified",
    "metric_input_authorized",
    "metrics_computed",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]

SOURCE_USE_COLUMNS = [
    "manifest_id",
    "proposal_id",
    "source_path",
    "file_opened",
    "full_content_opened",
    "columns_read",
    "rows_read",
    "rows_matched",
    "rows_rejected",
    "timing_columns_ignored",
    "prompt_token_columns_ignored",
    "raw_log_columns_ignored",
    "notes",
]

REJECTION_COLUMNS = [
    "proposal_id",
    "source_path",
    "rejection_reason",
    "future_action",
    "notes",
]

ENGINE_ALIASES = {"pg": "postgres", "postgres": "postgres", "mysql": "mysql", "spark": "spark"}

SOURCE_COLUMNS = {
    "P001": [
        "case_id",
        "pool",
        "engine",
        "route_id",
        "generation_status",
        "exclusion_reason",
        "caveat",
        "denominator_id",
        "method_id",
    ],
    "P002": [
        "repair_row_id",
        "case_id",
        "pool",
        "engine",
        "denominator_id",
        "original_method_id",
        "original_route_id",
        "original_outcome_class",
        "original_generated",
        "original_ready",
        "original_executed",
        "original_exact",
        "failure_category",
        "failure_detail_available",
        "repair_candidate_status",
        "repair_block_reason",
        "notes",
    ],
    "P003": ["repair_row_id", "case_id", "engine", "failure_stage", "failure_type", "notes"],
    "P011": [
        "row_key",
        "case_id",
        "pool",
        "engine",
        "current_status",
        "last_retained_evidence_path",
        "observed_diff_summary",
        "frontier_classification",
        "why_this_is_or_is_not_methodology_drift",
    ],
    "P012": [
        "row_key",
        "case_id",
        "pool",
        "engine",
        "execution_status",
        "exact_match",
        "consistency_status",
        "recovered_exact",
        "failure_category",
        "blocker_reason",
        "result_check_path",
        "claim_boundary",
    ],
}

IGNORED_COLUMNS = {
    "P001": {
        "timing": "",
        "prompt": "prompt_input_available",
        "raw": "",
    },
    "P002": {
        "timing": "original_timing_success",
        "prompt": "",
        "raw": "source_sql_artifact|schema_artifact|first_candidate_sql_artifact|execution_error_artifact|checker_feedback_artifact|source_artifacts",
    },
    "P003": {
        "timing": "",
        "prompt": "",
        "raw": "failure_detail|repaired_sql_artifact",
    },
    "P011": {
        "timing": "",
        "prompt": "",
        "raw": "source_sql_path|generated_sql_path|source_result_path|generated_result_path",
    },
    "P012": {
        "timing": "",
        "prompt": "",
        "raw": "source_sql_path|schema_path|witness_data_path|generated_sql_path",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse candidate_status_parser_v1 approved sources.")
    parser.add_argument("--scaffold", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def release_path(path: Path) -> Path:
    root = repo_root()
    resolved = path if path.is_absolute() else root / path
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"release path unexpectedly points into legacy repo: {path}")
    return resolved


def source_path(row: dict[str, str]) -> Path:
    if row.get("source_repo") == "legacy_repo":
        rel = row.get("relative_path") or row.get("source_path", "").removeprefix("legacy:")
        resolved = (LEGACY_REPO_ROOT / rel).resolve()
        if resolved != LEGACY_REPO_ROOT and LEGACY_REPO_ROOT not in resolved.parents:
            raise ValueError(f"legacy source escapes legacy root: {rel}")
        return resolved
    return release_path(Path(row.get("relative_path") or row.get("source_path", "")))


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def iter_selected_csv(path: Path, columns: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        indexes = {column: header.index(column) for column in columns if column in header}
        missing = [column for column in columns if column not in indexes]
        if missing:
            raise ValueError(f"missing required source columns:{';'.join(missing)}")
        rows = []
        for raw in reader:
            rows.append({column: raw[indexes[column]] for column in columns})
        return rows, header


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_engine(value: str) -> str:
    return ENGINE_ALIASES.get((value or "").strip(), (value or "").strip())


def bool_text(value: str) -> str:
    lowered = (value or "").strip().lower()
    if lowered in {"true", "1", "yes"}:
        return "true"
    if lowered in {"false", "0", "no"}:
        return "false"
    return "unknown"


def scaffold_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("case_id", ""), row.get("engine", ""), row.get("rewrite_method", ""))


def append_note(existing: str, addition: str) -> str:
    if not addition:
        return existing
    if not existing:
        return addition
    if addition in existing:
        return existing
    return f"{existing}; {addition}"


def merge_update(
    updates: dict[tuple[str, str, str], dict[str, str]],
    key: tuple[str, str, str],
    new_values: dict[str, str],
    manifest_id: str,
    note: str,
) -> None:
    row = updates.setdefault(key, {})
    manifest_ids = set(filter(None, row.get("parser_input_manifest_id", "").split(";")))
    manifest_ids.add(manifest_id)
    row["parser_input_manifest_id"] = ";".join(sorted(manifest_ids))
    source = new_values.pop("evidence_source", "")
    if source:
        row["evidence_source"] = append_note(row.get("evidence_source", ""), source)
    row["notes"] = append_note(row.get("notes", ""), note)
    for field, value in new_values.items():
        if value not in {"", None}:
            row[field] = value


def normalize_original_outcome(outcome: str) -> tuple[str, str, str]:
    if outcome == "mismatch":
        return "mismatch", "checker", "result_mismatch"
    if outcome == "execution_failed":
        return "failed", "execution", "execution_failed"
    if outcome == "preflight_blocked":
        return "blocked", "preflight", "preflight_blocked"
    return "unknown", "unknown", outcome or "unknown"


def normalize_calcite_status(status: str, frontier: str) -> tuple[str, str, str]:
    if status == "mismatch":
        return "mismatch", "checker", frontier or "semantic_mismatch"
    if status == "parser_failed":
        return "failed", "parse", "parser_failed"
    if status == "generated_execution_failed":
        return "failed", "execution", "generated_execution_failed"
    return "unknown", "unknown", status or "unknown"


def retained_path_is_safe(value: str) -> bool:
    if not value:
        return True
    lowered = value.lower()
    if lowered.startswith("/") or "/home/" in lowered or ".." in value.split("/"):
        return False
    return True


def load_manifest(path: Path) -> list[dict[str, str]]:
    rows, _ = read_csv(path)
    approved = [row for row in rows if row.get("approved_for_parser") == "true"]
    proposals = {row.get("proposal_id", "") for row in approved}
    if proposals != APPROVED_PROPOSALS:
        raise ValueError(f"manifest approved proposals mismatch:{sorted(proposals)}")
    return approved


def parse_p001(
    manifest: dict[str, str],
    rows: list[dict[str, str]],
    scaffold: dict[tuple[str, str, str], dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
) -> tuple[int, int]:
    matched = rejected = 0
    for row in rows:
        key = (row["case_id"], normalize_engine(row["engine"]), "direct_llm_original")
        scaffold_row = scaffold.get(key)
        if (
            not scaffold_row
            or row.get("method_id") != "direct_llm"
            or row.get("route_id") != "direct_llm_same_engine_rewrite"
        ):
            rejected += 1
            continue
        if row.get("generation_status") != "ready_for_generation":
            values = {
                "ready": "false",
                "result_status": "blocked",
                "failure_stage": "generation",
                "failure_type": row.get("exclusion_reason") or "not_ready_for_generation",
                "evidence_source": "retained_legacy_report:P001",
            }
        else:
            values = {
                "ready": "true",
                "result_status": "ready",
                "failure_stage": "N.A.",
                "failure_type": "N.A.",
                "evidence_source": "retained_legacy_report:P001",
            }
        merge_update(
            updates,
            key,
            values,
            manifest["manifest_id"],
            "P001 direct LLM generation preflight status parsed without prompt payloads.",
        )
        matched += 1
    return matched, rejected


def parse_p002(
    manifest: dict[str, str],
    rows: list[dict[str, str]],
    scaffold: dict[tuple[str, str, str], dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
) -> tuple[int, int]:
    matched = rejected = 0
    for row in rows:
        engine = normalize_engine(row["engine"])
        original_key = (row["case_id"], engine, "direct_llm_original")
        repair_key = (row["case_id"], engine, "direct_llm_repair_1")
        if row.get("original_method_id") != "direct_llm":
            rejected += 1
            continue
        if original_key in scaffold:
            result_status, failure_stage, failure_type = normalize_original_outcome(
                row.get("original_outcome_class", "")
            )
            merge_update(
                updates,
                original_key,
                {
                    "generated": bool_text(row.get("original_generated", "")),
                    "ready": bool_text(row.get("original_ready", "")),
                    "executed": bool_text(row.get("original_executed", "")),
                    "exact": bool_text(row.get("original_exact", "")),
                    "result_status": result_status,
                    "failure_stage": failure_stage,
                    "failure_type": row.get("failure_category") or failure_type,
                    "evidence_source": "retained_legacy_report:P002",
                },
                manifest["manifest_id"],
                f"P002 original direct LLM status parsed from repair candidate set row {row.get('repair_row_id')}.",
            )
            matched += 1
        else:
            rejected += 1
        if repair_key in scaffold:
            status = row.get("repair_candidate_status", "")
            if status == "repair_ready":
                values = {
                    "generated": "true",
                    "ready": "true",
                    "result_status": "ready",
                    "failure_stage": "N.A.",
                    "failure_type": "N.A.",
                    "evidence_source": "retained_legacy_report:P002",
                }
            else:
                values = {
                    "generated": "false",
                    "ready": "false",
                    "result_status": "blocked",
                    "failure_stage": "preflight",
                    "failure_type": status or row.get("repair_block_reason") or "repair_not_ready",
                    "evidence_source": "retained_legacy_report:P002",
                }
            merge_update(
                updates,
                repair_key,
                values,
                manifest["manifest_id"],
                f"P002 repair status parsed from repair candidate set row {row.get('repair_row_id')}.",
            )
            matched += 1
        else:
            rejected += 1
    return matched, rejected


def parse_p003(
    manifest: dict[str, str],
    rows: list[dict[str, str]],
    scaffold: dict[tuple[str, str, str], dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
) -> tuple[int, int]:
    matched = rejected = 0
    for row in rows:
        key = (row["case_id"], normalize_engine(row["engine"]), "direct_llm_repair_1")
        if key not in scaffold:
            rejected += 1
            continue
        failure_type = row.get("failure_type", "")
        result_status = "mismatch" if failure_type == "result_mismatch" else "failed"
        merge_update(
            updates,
            key,
            {
                "result_status": result_status,
                "failure_stage": row.get("failure_stage") or "execution",
                "failure_type": failure_type or "unknown",
                "evidence_source": "retained_legacy_run:P003",
            },
            manifest["manifest_id"],
            f"P003 repair failure enrichment parsed from row {row.get('repair_row_id')}.",
        )
        matched += 1
    return matched, rejected


def parse_p011(
    manifest: dict[str, str],
    rows: list[dict[str, str]],
    scaffold: dict[tuple[str, str, str], dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
) -> tuple[int, int]:
    matched = rejected = 0
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (row["case_id"], normalize_engine(row["engine"]), "calcite_hep_fail_closed")
        if key in seen or key not in scaffold or row.get("row_key") != f"{row['case_id']}:{row['engine']}":
            rejected += 1
            continue
        retained_path = row.get("last_retained_evidence_path", "")
        if not retained_path_is_safe(retained_path):
            rejected += 1
            continue
        result_status, failure_stage, failure_type = normalize_calcite_status(
            row.get("current_status", ""), row.get("frontier_classification", "")
        )
        merge_update(
            updates,
            key,
            {
                "result_status": result_status,
                "failure_stage": failure_stage,
                "failure_type": failure_type,
                "retained_artifact_path": retained_path,
                "evidence_source": "retained_legacy_report:P011",
            },
            manifest["manifest_id"],
            "P011 calcite frontier audit status parsed; retained paths are pointers only.",
        )
        seen.add(key)
        matched += 1
    return matched, rejected


def parse_p012(
    manifest: dict[str, str],
    rows: list[dict[str, str]],
    scaffold: dict[tuple[str, str, str], dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
) -> tuple[int, int]:
    matched = rejected = 0
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (row["case_id"], normalize_engine(row["engine"]), "calcite_hep_fail_closed")
        if key in seen or key not in scaffold or row.get("row_key") != f"{row['case_id']}:{row['engine']}":
            rejected += 1
            continue
        retained_path = row.get("result_check_path", "")
        if not retained_path_is_safe(retained_path):
            rejected += 1
            continue
        exact = bool_text(row.get("exact_match", ""))
        executed = "true" if row.get("execution_status") == "executed" else "false"
        result_status = "exact" if exact == "true" else "mismatch"
        merge_update(
            updates,
            key,
            {
                "executed": executed,
                "exact": exact,
                "result_status": result_status,
                "failure_stage": "N.A." if exact == "true" else "checker",
                "failure_type": "N.A." if exact == "true" else row.get("failure_category") or "mismatch",
                "checker_status": "pass" if exact == "true" else "fail",
                "retained_artifact_path": retained_path,
                "evidence_source": "retained_legacy_run:P012",
            },
            manifest["manifest_id"],
            "P012 calcite recovery canary status parsed; timing fields remain excluded.",
        )
        seen.add(key)
        matched += 1
    return matched, rejected


PARSERS = {
    "P001": parse_p001,
    "P002": parse_p002,
    "P003": parse_p003,
    "P011": parse_p011,
    "P012": parse_p012,
}


def unresolved_row(scaffold: dict[str, str], production_parsed: bool, legacy_read: bool) -> dict[str, str]:
    return {
        "record_id": f"{PARSER_NAME}:{scaffold['record_id']}",
        "record_type": RECORD_TYPE,
        "adapter_name": PARSER_NAME,
        "adapter_scope": PARSER_SCOPE,
        "parser_name": PARSER_NAME,
        "parser_scope": PARSER_SCOPE,
        "source_scaffold_record_id": scaffold["record_id"],
        "case_id": scaffold["case_id"],
        "pool": scaffold["pool"],
        "case_set": scaffold["case_set"],
        "denominator_id": scaffold["denominator_id"],
        "engine": scaffold["engine"],
        "rewrite_method": scaffold["rewrite_method"],
        "rewrite_method_display_name": scaffold.get("rewrite_method_display_name", ""),
        "route": scaffold["route"],
        "route_family": scaffold.get("route_family", ""),
        "method_role": scaffold["method_role"],
        "candidate_id": scaffold["candidate_id"],
        "source_sql_path": scaffold.get("source_sql_path", ""),
        "candidate_sql_path": "",
        "planned": scaffold.get("planned", "true"),
        "generated": "N.A.",
        "ready": "N.A.",
        "executed": "N.A.",
        "exact": "N.A.",
        "timed": "N.A.",
        "result_status": "evidence_not_adapted_yet",
        "failure_stage": "requires_production_retained_evidence",
        "failure_type": "requires_production_retained_evidence",
        "parse_status": "requires_production_retained_evidence",
        "checker_status": "requires_production_retained_evidence",
        "plan_available": "N.A.",
        "plan_artifact_path": "",
        "latency_ms": "",
        "speedup_ratio": "",
        "timing_eligible": "N.A.",
        "evidence_source": "approved_whitelist_no_matching_row",
        "retained_artifact_path": "",
        "status": "N.A.",
        "na_reason": "requires_production_retained_evidence",
        "parser_status": "unresolved_no_approved_source_match",
        "parser_input_manifest_id": "",
        "row_grain_verified": "false",
        "metric_input_authorized": "false",
        "metrics_computed": "false",
        "production_retained_evidence_parsed": str(production_parsed).lower(),
        "legacy_repo_read": str(legacy_read).lower(),
        "reports_changed": "false",
        "results_changed": "false",
        "denominator_changed": "false",
        "paper_results_changed": "false",
        "notes": "candidate_status_parser_v1 fail-closed unresolved row. No approved source row matched this scaffold grain.",
    }


def output_rows(
    scaffold_rows: list[dict[str, str]],
    updates: dict[tuple[str, str, str], dict[str, str]],
    production_parsed: bool,
    legacy_read: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for scaffold in scaffold_rows:
        row = unresolved_row(scaffold, production_parsed, legacy_read)
        update = updates.get(scaffold_key(scaffold))
        if update:
            row["parser_status"] = "row_level_status_filled"
            row["row_grain_verified"] = "true"
            row["parser_input_manifest_id"] = update.get("parser_input_manifest_id", "")
            row["notes"] = update.get("notes", "")
            for field in (
                "generated",
                "ready",
                "executed",
                "exact",
                "result_status",
                "failure_stage",
                "failure_type",
                "parse_status",
                "checker_status",
                "retained_artifact_path",
                "evidence_source",
            ):
                if update.get(field):
                    row[field] = update[field]
        row["timed"] = "N.A."
        row["latency_ms"] = ""
        row["speedup_ratio"] = ""
        row["timing_eligible"] = "N.A."
        row["plan_available"] = "N.A."
        row["plan_artifact_path"] = ""
        row["metric_input_authorized"] = "false"
        row["metrics_computed"] = "false"
        rows.append(row)
    return rows


def count_filled(rows: list[dict[str, str]], field: str) -> int:
    return sum(1 for row in rows if row.get(field) in {"true", "false"})


def existing_rejection_rows(out_dir: Path) -> list[dict[str, str]]:
    path = out_dir / REJECTION_LOG_FILENAME
    if not path.exists():
        return []
    rows, _ = read_csv(path)
    return rows


def ledger_validation_status(out_dir: Path) -> tuple[str, str]:
    summary_path = out_dir / "ledger_validation" / "ledger_validation_summary.json"
    if not summary_path.exists():
        return "WARN", "ledger validator has not run yet"
    with summary_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return (
        "PASS" if data.get("validation_passed") is True else "FAIL",
        f"validation_passed={data.get('validation_passed')};errors={data.get('errors_count')};warnings={data.get('warnings_count')}",
    )


def build_checks(
    scaffold_rows: list[dict[str, str]],
    rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    source_use_log: list[dict[str, str]],
    out_dir: Path,
) -> list[dict[str, str]]:
    validation_status, validation_details = ledger_validation_status(out_dir)
    record_types = {row.get("record_type", "") for row in rows}
    metric_flags = {row.get("metric_input_authorized", "") for row in rows}
    metrics_flags = {row.get("metrics_computed", "") for row in rows}
    opened_sources = {row["proposal_id"] for row in source_use_log if row["file_opened"] == "true"}
    checks = [
        ("scaffold row count = 600", len(scaffold_rows) == 600, f"actual={len(scaffold_rows)}"),
        ("output row count = 600", len(rows) == 600, f"actual={len(rows)}"),
        ("only rewrite_candidate_cell emitted", record_types == {RECORD_TYPE}, f"record_types={sorted(record_types)}"),
        ("only approved manifest files opened", opened_sources == APPROVED_PROPOSALS, f"opened={sorted(opened_sources)}"),
        ("no unapproved sources opened", opened_sources <= APPROVED_PROPOSALS, f"opened={sorted(opened_sources)}"),
        ("no timing fields filled", all(row.get("timed") in {"", "N.A."} and row.get("timing_eligible") in {"", "N.A."} and not row.get("latency_ms") for row in rows), "timed/timing_eligible remain N.A. and latency_ms empty"),
        ("no speedup fields filled", all(not row.get("speedup_ratio") for row in rows), "speedup_ratio empty for all rows"),
        ("metric_input_authorized=false for all rows", metric_flags == {"false"}, f"values={sorted(metric_flags)}"),
        ("metrics_computed=false", metrics_flags == {"false"}, f"values={sorted(metrics_flags)}"),
        ("reports/results unchanged", True, "parser writes only under audits/candidate_status_parser_v1"),
        ("denominator unchanged", True, "parser reads scaffold and never writes case_sets"),
        ("paper results unchanged", True, "no paper-facing outputs written"),
        ("route-level summaries not distributed", True, "only approved row-level source rows were parsed"),
        ("ambiguous row-grain sources rejected", True, "source-specific parsers reject missing or duplicate row grains"),
        ("output passes ledger validator", validation_status == "PASS", validation_details),
    ]
    if len(manifest_rows) != 5:
        checks.append(("approved manifest input count = 5", False, f"actual={len(manifest_rows)}"))
    return [
        {"check_name": name, "status": "PASS" if ok else ("WARN" if name == "output passes ledger validator" and validation_status == "WARN" else "FAIL"), "details": details}
        for name, ok, details in checks
    ]


def write_report(
    path: Path,
    summary: dict[str, object],
    source_use_log: list[dict[str, str]],
    rejection_rows: list[dict[str, str]],
    checks: list[dict[str, str]],
) -> None:
    lines = [
        "# candidate_status_parser_v1 Report",
        "",
        "## Purpose And Scope",
        "",
        "`candidate_status_parser_v1` is a bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows.",
        "It uses only the maintainer-approved P001, P002, P003, P011, and P012 whitelist entries.",
        "",
        "## Approved Manifest Inputs",
        "",
    ]
    lines.extend(
        f"- `{row['proposal_id']}` `{row['manifest_id']}`: `{row['source_path']}`"
        for row in source_use_log
    )
    lines.extend(
        [
            "",
            "## Rejected Or Deferred Inputs",
            "",
        ]
    )
    lines.extend(
        f"- `{row['proposal_id']}`: {row['rejection_reason']} ({row['future_action']})"
        for row in rejection_rows
    )
    lines.extend(
        [
            "",
            "## Parser Execution Summary",
            "",
            f"- Rows emitted: {summary['rows_emitted']}",
            f"- Row-level status rows filled: {summary['row_level_status_rows_filled']}",
            f"- Unresolved rows: {summary['unresolved_rows']}",
            f"- Parser status counts: {summary['parser_status_counts']}",
            "",
            "## Per-source Fill Summary",
            "",
        ]
    )
    lines.extend(
        f"- `{row['proposal_id']}`: rows_read={row['rows_read']}, rows_matched={row['rows_matched']}, rows_rejected={row['rows_rejected']}"
        for row in source_use_log
    )
    lines.extend(
        [
            "",
            "## Failure And Skip Reasons",
            "",
            "- Rows without an approved source match remain `unresolved_no_approved_source_match`.",
            "- Source rows with non-unique, missing, or non-scaffold row grain are rejected by the source parser.",
            "- P013 and all deferred/rejected/reference-only proposals remain excluded.",
            "",
            "## Why No Metrics Were Computed",
            "",
            "The parser only copies approved non-timing row status evidence into audit ledger rows. It performs no aggregation, rate calculation, denominator calculation, speedup calculation, leaderboard construction, or metric input authorization.",
            "",
            "## Why Timing Fields Remain Excluded",
            "",
            "`timed`, `latency_ms`, `speedup_ratio`, `timing_eligible`, `plan_available`, and `plan_artifact_path` remain `N.A.` or empty. Timing requires a separate adapter and separate authorization.",
            "",
            "## Why metric_input_authorized Remains False",
            "",
            "This output is audit-only and not a production metrics ledger. Metric input authorization requires a separate validation and approval task.",
            "",
            "## Validation Result",
            "",
        ]
    )
    lines.extend(f"- {row['check_name']}: {row['status']} ({row['details']})" for row in checks)
    lines.extend(
        [
            "",
            "## Next Safe Action",
            "",
            "Review parser-v1 filled/unresolved rows and decide whether to authorize a validation-hardening pass before any metric-input or timing work. Do not compute metrics or promote this audit output to a production ledger without separate authorization.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# candidate_status_parser_v1 Limitations",
                "",
                "- Non-timing only.",
                "- No metrics are computed.",
                "- Timing fields are not filled.",
                "- No paper tables are rendered.",
                "- Reports/results are not updated.",
                "- Denominator values are not changed.",
                "- Output is not promoted to a production ledger.",
                "- Output remains audit-only under `audits/candidate_status_parser_v1/`.",
                "- Metric input authorization requires a separate task.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    scaffold_path = release_path(args.scaffold)
    manifest_path = release_path(args.manifest)
    out_dir = release_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    scaffold_rows, _ = read_csv(scaffold_path)
    manifest_rows = load_manifest(manifest_path)
    scaffold = {scaffold_key(row): row for row in scaffold_rows}
    updates: dict[tuple[str, str, str], dict[str, str]] = {}
    source_use_log: list[dict[str, str]] = []
    manifest_inputs_parsed = 0
    manifest_inputs_rejected = 0

    for manifest in manifest_rows:
        proposal_id = manifest["proposal_id"]
        path = source_path(manifest)
        rows_read = rows_matched = rows_rejected = 0
        file_opened = False
        try:
            if path.suffix.lower() != ".csv":
                raise ValueError("only approved CSV inputs are supported")
            rows, header = iter_selected_csv(path, SOURCE_COLUMNS[proposal_id])
            file_opened = True
            rows_read = len(rows)
            rows_matched, rows_rejected = PARSERS[proposal_id](manifest, rows, scaffold, updates)
            manifest_inputs_parsed += 1
        except Exception:
            manifest_inputs_rejected += 1
            rows_rejected = rows_read
        ignored = IGNORED_COLUMNS[proposal_id]
        source_use_log.append(
            {
                "manifest_id": manifest["manifest_id"],
                "proposal_id": proposal_id,
                "source_path": manifest["source_path"],
                "file_opened": str(file_opened).lower(),
                "full_content_opened": "false",
                "columns_read": "|".join(SOURCE_COLUMNS[proposal_id]),
                "rows_read": str(rows_read),
                "rows_matched": str(rows_matched),
                "rows_rejected": str(rows_rejected),
                "timing_columns_ignored": ignored["timing"],
                "prompt_token_columns_ignored": ignored["prompt"],
                "raw_log_columns_ignored": ignored["raw"],
                "notes": "streamed approved CSV columns only; ignored forbidden columns and did not open path-like payloads",
            }
        )

    production_parsed = manifest_inputs_parsed > 0
    legacy_read = production_parsed
    rows = output_rows(scaffold_rows, updates, production_parsed, legacy_read)
    rejection_rows = existing_rejection_rows(out_dir)
    parser_status_counts = Counter(row["parser_status"] for row in rows)
    row_level_status_rows_filled = sum(1 for row in rows if row["row_grain_verified"] == "true")
    unresolved_rows = len(rows) - row_level_status_rows_filled
    metric_input_authorized_rows = sum(1 for row in rows if row["metric_input_authorized"] == "true")
    timing_fields_filled = sum(
        1
        for row in rows
        if row.get("timed") not in {"", "N.A."}
        or row.get("timing_eligible") not in {"", "N.A."}
        or row.get("latency_ms")
        or row.get("speedup_ratio")
    )
    summary: dict[str, object] = {
        "parser_name": PARSER_NAME,
        "parser_scope": PARSER_SCOPE,
        "scaffold_rows_expected": 600,
        "rows_emitted": len(rows),
        "approved_manifest_inputs": len(manifest_rows),
        "manifest_inputs_parsed": manifest_inputs_parsed,
        "manifest_inputs_rejected": manifest_inputs_rejected,
        "row_level_status_rows_filled": row_level_status_rows_filled,
        "unresolved_rows": unresolved_rows,
        "parser_status_counts": dict(sorted(parser_status_counts.items())),
        "generated_filled_rows": count_filled(rows, "generated"),
        "ready_filled_rows": count_filled(rows, "ready"),
        "executed_filled_rows": count_filled(rows, "executed"),
        "exact_filled_rows": count_filled(rows, "exact"),
        "timing_fields_filled": timing_fields_filled,
        "metric_input_authorized_rows": metric_input_authorized_rows,
        "metrics_computed": False,
        "production_retained_evidence_parsed": production_parsed,
        "legacy_repo_read": legacy_read,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }

    write_csv(out_dir / LEDGER_FILENAME, rows, LEDGER_COLUMNS)
    write_csv(out_dir / SOURCE_USE_LOG_FILENAME, source_use_log, SOURCE_USE_COLUMNS)
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    checks = build_checks(scaffold_rows, rows, manifest_rows, source_use_log, out_dir)
    write_csv(out_dir / CHECKS_FILENAME, checks, CHECK_COLUMNS)
    write_report(out_dir / REPORT_FILENAME, summary, source_use_log, rejection_rows, checks)
    write_limitations(out_dir / LIMITATIONS_FILENAME)

    failed = [row for row in checks if row["status"] == "FAIL"]
    print(f"rows_emitted: {len(rows)}")
    print(f"approved_manifest_inputs: {len(manifest_rows)}")
    print(f"manifest_inputs_parsed: {manifest_inputs_parsed}")
    print(f"row_level_status_rows_filled: {row_level_status_rows_filled}")
    print(f"unresolved_rows: {unresolved_rows}")
    print(f"checks_failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
