#!/usr/bin/env python3
"""Parse SQLGlot candidate statuses from sanitized non-timing projections."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


SQLGLOT_METHODS = {"sqlglot_optimize", "sqlglot_noop"}

LEDGER_FIELDS = [
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

SOURCE_LOG_FIELDS = [
    "projection_id",
    "source_id",
    "rewrite_method",
    "projection_rows",
    "matched_scaffold_rows",
    "fields_filled",
    "timing_fields_filled",
    "metrics_computed",
    "notes",
]

CHECK_FIELDS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse SQLGlot candidate status projection rows.")
    parser.add_argument("--scaffold", required=True, type=Path)
    parser.add_argument("--projection-index", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def projection_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.exists():
        return path
    root = Path(__file__).resolve().parents[2]
    return root / path


def load_projections(index_rows: list[dict[str, str]]) -> tuple[dict[tuple[str, str, str], dict[str, str]], list[dict[str, str]]]:
    by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    source_logs: list[dict[str, str]] = []
    for index_row in index_rows:
        if index_row.get("parser_ready") != "true":
            continue
        rows, _ = read_csv(projection_path(index_row["projection_path"]))
        matched = 0
        for row in rows:
            key = (row["case_id"], row["engine"], row["rewrite_method"])
            by_key[key] = row
            matched += 1
        source_logs.append(
            {
                "projection_id": index_row["projection_id"],
                "source_id": index_row["source_id"],
                "rewrite_method": index_row["rewrite_method"],
                "projection_rows": str(len(rows)),
                "matched_scaffold_rows": "0",
                "fields_filled": "executed|exact|result_status|failure_stage|failure_type|parse_status|checker_status|evidence_source|retained_artifact_path",
                "timing_fields_filled": "0",
                "metrics_computed": "false",
                "notes": "sanitized projection rows loaded; scaffold matching is counted after parse",
            }
        )
    return by_key, source_logs


def make_unresolved(scaffold: dict[str, str]) -> dict[str, str]:
    return {
        "generated": "N.A.",
        "ready": "N.A.",
        "executed": "N.A.",
        "exact": "N.A.",
        "result_status": "evidence_not_adapted_yet",
        "failure_stage": "N.A.",
        "failure_type": "N.A.",
        "parse_status": "N.A.",
        "checker_status": "N.A.",
        "evidence_source": "sqlglot_sanitized_projection_not_matched",
        "retained_artifact_path": "",
        "parser_status": "unresolved_no_sanitized_projection_match",
        "parser_input_manifest_id": "",
        "row_grain_verified": "false",
        "notes": "No parser-ready sanitized SQLGlot projection row matched this scaffold row.",
    }


def build_ledger_row(scaffold: dict[str, str], projection: dict[str, str] | None) -> dict[str, str]:
    status = make_unresolved(scaffold) if projection is None else {
        "generated": projection["generated"],
        "ready": projection["ready"],
        "executed": projection["executed"],
        "exact": projection["exact"],
        "result_status": projection["result_status"],
        "failure_stage": projection["failure_stage"],
        "failure_type": projection["failure_type"],
        "parse_status": projection["parse_status"],
        "checker_status": projection["checker_status"],
        "evidence_source": projection["evidence_source"],
        "retained_artifact_path": projection["retained_artifact_path"],
        "parser_status": "row_level_status_filled",
        "parser_input_manifest_id": projection["projection_id"],
        "row_grain_verified": projection["row_grain_verified"],
        "notes": "SQLGlot executed/exact status parsed from sanitized non-timing checker-event projection; generated/ready remain source-unobserved.",
    }
    return {
        "record_id": f"sqlglot_candidate_status_parser_v1:{scaffold['record_id']}",
        "record_type": "rewrite_candidate_cell",
        "adapter_name": "sqlglot_candidate_status_parser_v1",
        "adapter_scope": "sanitized_non_timing_projection_only",
        "parser_name": "sqlglot_candidate_status_parser_v1",
        "parser_scope": "sanitized_non_timing_projection_only",
        "source_scaffold_record_id": scaffold["record_id"],
        "case_id": scaffold["case_id"],
        "pool": scaffold["pool"],
        "case_set": scaffold["case_set"],
        "denominator_id": scaffold["denominator_id"],
        "engine": scaffold["engine"],
        "rewrite_method": scaffold["rewrite_method"],
        "rewrite_method_display_name": scaffold.get("rewrite_method_display_name", ""),
        "route": scaffold["route"],
        "route_family": scaffold["route_family"],
        "method_role": scaffold["method_role"],
        "candidate_id": scaffold["candidate_id"],
        "source_sql_path": scaffold.get("source_sql_path", ""),
        "candidate_sql_path": "",
        "planned": "true",
        "generated": status["generated"],
        "ready": status["ready"],
        "executed": status["executed"],
        "exact": status["exact"],
        "timed": "N.A.",
        "result_status": status["result_status"],
        "failure_stage": status["failure_stage"],
        "failure_type": status["failure_type"],
        "parse_status": status["parse_status"],
        "checker_status": status["checker_status"],
        "plan_available": "N.A.",
        "plan_artifact_path": "",
        "latency_ms": "",
        "speedup_ratio": "",
        "timing_eligible": "N.A.",
        "evidence_source": status["evidence_source"],
        "retained_artifact_path": status["retained_artifact_path"],
        "status": "N.A.",
        "na_reason": "requires_production_retained_evidence",
        "parser_status": status["parser_status"],
        "parser_input_manifest_id": status["parser_input_manifest_id"],
        "row_grain_verified": status["row_grain_verified"],
        "metric_input_authorized": "false",
        "metrics_computed": "false",
        "production_retained_evidence_parsed": "false",
        "legacy_repo_read": "false",
        "reports_changed": "false",
        "results_changed": "false",
        "denominator_changed": "false",
        "paper_results_changed": "false",
        "notes": status["notes"],
    }


def write_report(path: Path, summary: dict[str, object], method_counts: Counter[str]) -> None:
    lines = [
        "# SQLGlot Candidate Status Parser v1 Report",
        "",
        "## Purpose And Scope",
        "",
        "This parser emits audit-only SQLGlot rewrite_candidate_cell rows from sanitized non-timing projections.",
        "It reads no raw logs, timing arrays, prompt/token traces, or artifact payloads.",
        "",
        "## Parser Summary",
        "",
        f"- SQLGlot scaffold rows expected: {summary['scaffold_sqlglot_rows_expected']}",
        f"- Rows emitted: {summary['rows_emitted']}",
        f"- Row-level status rows filled: {summary['row_level_status_rows_filled']}",
        f"- Unresolved SQLGlot rows: {summary['unresolved_sqlglot_rows']}",
        f"- Methods covered: {', '.join(summary['methods_covered'])}",
        "",
        "## Method Coverage",
        "",
    ]
    lines.extend(f"- `{method}`: {count} filled rows" for method, count in sorted(method_counts.items()))
    lines.extend(
        [
            "",
            "## Boundary Confirmation",
            "",
            "- Timing fields filled: 0",
            "- metric_input_authorized rows: 0",
            "- Metrics computed: false",
            "- Reports/results changed: false",
            "",
            "## Limitation",
            "",
            "SGL011 supports executed/exact/checker outcome fields only. Generated and ready are not inferred from checker artifact path existence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# SQLGlot Candidate Status Parser v1 Limitations",
                "",
                "- Audit-only parser output; not an official benchmark result.",
                "- Only sanitized non-timing projection rows are used.",
                "- Generated and ready are not inferred from checker-event artifact paths.",
                "- Timing, latency, speedup, and timing eligibility fields remain blank or N.A.",
                "- Rows without a case_id x engine x rewrite_method projection match remain unresolved.",
                "- SQLGlot metric-input authorization is not created by this task.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    scaffold_rows, _ = read_csv(args.scaffold)
    index_rows, _ = read_csv(args.projection_index)
    projection_by_key, source_logs = load_projections(index_rows)
    sqlglot_scaffold = [row for row in scaffold_rows if row.get("rewrite_method") in SQLGLOT_METHODS]

    ledger_rows: list[dict[str, str]] = []
    matched_by_projection = Counter()
    method_counts: Counter[str] = Counter()
    for scaffold in sqlglot_scaffold:
        key = (scaffold["case_id"], scaffold["engine"], scaffold["rewrite_method"])
        projection = projection_by_key.get(key)
        ledger_row = build_ledger_row(scaffold, projection)
        ledger_rows.append(ledger_row)
        if projection is not None:
            matched_by_projection[projection["projection_id"]] += 1
            method_counts[scaffold["rewrite_method"]] += 1

    for row in source_logs:
        row["matched_scaffold_rows"] = str(matched_by_projection.get(row["projection_id"], 0))

    output = args.out_dir / "sqlglot_candidate_status_ledger_v1.csv"
    write_csv(output, ledger_rows, LEDGER_FIELDS)
    write_csv(args.out_dir / "sqlglot_candidate_status_parser_v1_source_use_log.csv", source_logs, SOURCE_LOG_FIELDS)

    filled = sum(1 for row in ledger_rows if row["parser_status"] == "row_level_status_filled")
    unresolved = len(ledger_rows) - filled
    summary = {
        "parser_name": "sqlglot_candidate_status_parser_v1",
        "scaffold_sqlglot_rows_expected": 240,
        "rows_emitted": len(ledger_rows),
        "row_level_status_rows_filled": filled,
        "unresolved_sqlglot_rows": unresolved,
        "methods_covered": sorted(method_counts),
        "timing_fields_filled": 0,
        "metric_input_authorized_rows": 0,
        "metrics_computed": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    (args.out_dir / "sqlglot_candidate_status_parser_v1_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir / "sqlglot_candidate_status_parser_v1_report.md", summary, method_counts)
    write_limitations(args.out_dir / "sqlglot_candidate_status_parser_v1_limitations.md")
    checks = [
        {
            "check_name": "SQLGlot scaffold rows emitted",
            "status": "PASS" if len(ledger_rows) == 240 else "FAIL",
            "details": f"{len(ledger_rows)} rows emitted",
        },
        {
            "check_name": "non-timing status rows filled",
            "status": "PASS" if filled > 0 else "WARN",
            "details": f"{filled} rows filled from sanitized projections",
        },
        {
            "check_name": "unmatched rows left unresolved",
            "status": "PASS",
            "details": f"{unresolved} SQLGlot rows remain unresolved",
        },
        {
            "check_name": "timing fields filled",
            "status": "PASS" if all(row["latency_ms"] == "" and row["speedup_ratio"] == "" and row["timed"] == "N.A." for row in ledger_rows) else "FAIL",
            "details": "0 timing/speedup values filled",
        },
        {
            "check_name": "metric_input_authorized rows",
            "status": "PASS" if all(row["metric_input_authorized"] == "false" for row in ledger_rows) else "FAIL",
            "details": "0",
        },
        {
            "check_name": "metrics computed",
            "status": "PASS" if all(row["metrics_computed"] == "false" for row in ledger_rows) else "FAIL",
            "details": "false",
        },
    ]
    write_csv(args.out_dir / "sqlglot_candidate_status_parser_v1_checks.csv", checks, CHECK_FIELDS)
    print(f"rows_emitted: {len(ledger_rows)}")
    print(f"row_level_status_rows_filled: {filled}")
    print(f"unresolved_sqlglot_rows: {unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
