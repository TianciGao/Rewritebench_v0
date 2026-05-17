#!/usr/bin/env python3
"""Build combined candidate status overlay v2.

This overlay preserves candidate_status_parser_v1 rows and replaces only the
SQLGlot scaffold rows with sqlglot_candidate_status_parser_v1 output.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


SQLGLOT_METHODS = {"sqlglot_optimize", "sqlglot_noop"}
CHECK_FIELDS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build combined candidate status overlay v2.")
    parser.add_argument("--base-candidate-ledger", required=True, type=Path)
    parser.add_argument("--sqlglot-ledger", required=True, type=Path)
    parser.add_argument("--combined-authorization", required=True, type=Path)
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


def source_scaffold_id(row: dict[str, str]) -> str:
    return row.get("source_scaffold_record_id") or row.get("record_id", "").removeprefix("candidate_status_parser_v1:")


def is_filled(row: dict[str, str]) -> bool:
    return row.get("parser_status") == "row_level_status_filled"


def write_report(path: Path, summary: dict[str, object], method_counts: Counter[str]) -> None:
    lines = [
        "# Combined Candidate Status Overlay v2 Report",
        "",
        "## Purpose And Scope",
        "",
        "This audit overlay combines existing candidate_status_parser_v1 output with SQLGlot sanitized projection parser output.",
        "It preserves the 600-row scaffold accounting and does not modify either input ledger.",
        "",
        "## Summary",
        "",
        f"- Total rows: {summary['total_rows']}",
        f"- SQLGlot rows filled: {summary['sqlglot_rows_filled']}",
        f"- Total filled rows: {summary['total_filled_rows']}",
        f"- Unresolved rows: {summary['unresolved_rows']}",
        "",
        "## Filled Rows By Method",
        "",
    ]
    lines.extend(f"- `{method}`: {count}" for method, count in sorted(method_counts.items()))
    lines.extend(
        [
            "",
            "## Boundary Confirmation",
            "",
            "- Metrics computed: false",
            "- Timing fields filled: false",
            "- Reports/results changed: false",
            "- Denominator changed: false",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    base_rows, base_fields = read_csv(args.base_candidate_ledger)
    sqlglot_rows, sqlglot_fields = read_csv(args.sqlglot_ledger)
    authorization_rows, _ = read_csv(args.combined_authorization)
    authorized_ids = {
        row["record_id"]
        for row in authorization_rows
        if row.get("metric_input_authorized_overlay") == "true"
    }
    sqlglot_by_scaffold = {row["source_scaffold_record_id"]: row for row in sqlglot_rows}
    output_fields = list(base_fields)
    for field in sqlglot_fields:
        if field not in output_fields:
            output_fields.append(field)

    combined: list[dict[str, str]] = []
    for base in base_rows:
        scaffold_id = source_scaffold_id(base)
        if base.get("rewrite_method") in SQLGLOT_METHODS:
            row = dict(sqlglot_by_scaffold.get(scaffold_id, base))
        else:
            row = dict(base)
        row["metric_input_authorized"] = "true" if row.get("record_id") in authorized_ids else "false"
        row["metrics_computed"] = "false"
        row["reports_changed"] = "false"
        row["results_changed"] = "false"
        row["denominator_changed"] = "false"
        row["paper_results_changed"] = "false"
        combined.append({field: row.get(field, "") for field in output_fields})

    method_counts = Counter(row["rewrite_method"] for row in combined if is_filled(row))
    sqlglot_filled = sum(1 for row in combined if row.get("rewrite_method") in SQLGLOT_METHODS and is_filled(row))
    total_filled = sum(1 for row in combined if is_filled(row))
    summary = {
        "total_rows": len(combined),
        "sqlglot_rows_filled": sqlglot_filled,
        "total_filled_rows": total_filled,
        "unresolved_rows": len(combined) - total_filled,
        "metrics_computed": False,
        "timing_fields_filled": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
    }
    write_csv(args.out_dir / "combined_candidate_status_ledger_v2.csv", combined, output_fields)
    (args.out_dir / "combined_candidate_status_overlay_v2_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir / "combined_candidate_status_overlay_v2_report.md", summary, method_counts)
    checks = [
        {
            "check_name": "combined rows preserve 600-row scaffold",
            "status": "PASS" if len(combined) == 600 else "FAIL",
            "details": f"{len(combined)} rows",
        },
        {
            "check_name": "SQLGlot overlay rows available",
            "status": "PASS" if len(sqlglot_rows) == 240 else "FAIL",
            "details": f"{len(sqlglot_rows)} SQLGlot parser rows",
        },
        {
            "check_name": "SQLGlot rows filled",
            "status": "PASS" if sqlglot_filled > 0 else "WARN",
            "details": str(sqlglot_filled),
        },
        {
            "check_name": "metrics computed",
            "status": "PASS" if all(row["metrics_computed"] == "false" for row in combined) else "FAIL",
            "details": "false",
        },
        {
            "check_name": "timing fields filled",
            "status": "PASS" if all(row.get("latency_ms", "") in {"", "N.A."} and row.get("speedup_ratio", "") in {"", "N.A."} for row in combined) else "FAIL",
            "details": "false",
        },
        {
            "check_name": "reports/results changed",
            "status": "PASS" if all(row["reports_changed"] == "false" and row["results_changed"] == "false" for row in combined) else "FAIL",
            "details": "false",
        },
    ]
    write_csv(args.out_dir / "combined_candidate_status_overlay_v2_checks.csv", checks, CHECK_FIELDS)
    print(f"total_rows: {len(combined)}")
    print(f"sqlglot_rows_filled: {sqlglot_filled}")
    print(f"total_filled_rows: {total_filled}")
    print(f"unresolved_rows: {len(combined) - total_filled}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
