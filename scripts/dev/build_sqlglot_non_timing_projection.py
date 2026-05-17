#!/usr/bin/env python3
"""Create sanitized non-timing SQLGlot status projections.

Only manifest rows with approved_for_projection=true are projected. The current
bounded manifest approves SGL011 checker-event rows and retains only status
columns needed for row-grain SQLGlot candidate status parsing.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


LEGACY_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

ROUTE_BY_METHOD = {
    "sqlglot_optimize": "sqlglot_optimize_same_dialect",
    "sqlglot_noop": "sqlglot_transpile_same_dialect_noop",
}

ENGINE_ALIASES = {
    "pg": "postgres",
    "postgres": "postgres",
    "postgresql": "postgres",
    "mysql": "mysql",
    "spark": "spark",
}

SOURCE_SAFE_COLUMNS = [
    "row_id",
    "method_id",
    "route_id",
    "case_id",
    "pool",
    "engine",
    "denominator_id",
    "backfill_scope",
    "source_execution_success",
    "candidate_execution_success",
    "exact_match",
    "sorted_match",
    "failure_category",
    "failure_detail",
    "checker_status",
    "notes",
]

PROJECTION_FIELDS = [
    "projection_id",
    "source_id",
    "source_row_id",
    "source_path",
    "case_id",
    "pool",
    "engine",
    "source_denominator_id",
    "denominator_id",
    "rewrite_method",
    "route_id",
    "method_id",
    "generated",
    "ready",
    "executed",
    "exact",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
    "evidence_source",
    "retained_artifact_path",
    "row_grain_key",
    "row_grain_verified",
    "notes",
]

INDEX_FIELDS = [
    "projection_id",
    "source_id",
    "source_path",
    "projection_path",
    "rewrite_method",
    "row_count",
    "columns_retained",
    "columns_dropped",
    "row_grain_verified",
    "timing_columns_removed",
    "prompt_token_columns_removed",
    "raw_log_columns_removed",
    "parser_ready",
    "notes",
]

CHECK_FIELDS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build sanitized SQLGlot projections.")
    parser.add_argument("--manifest", required=True, type=Path)
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


def source_path_to_legacy(path_value: str) -> Path:
    if not path_value.startswith("legacy:"):
        raise ValueError(f"expected legacy: source path, got {path_value}")
    return LEGACY_ROOT / path_value.removeprefix("legacy:")


def normalize_bool(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"true", "1", "yes"}:
        return "true"
    if value in {"false", "0", "no"}:
        return "false"
    return "unknown"


def map_status(source_row: dict[str, str]) -> dict[str, str]:
    executed = normalize_bool(source_row.get("candidate_execution_success", ""))
    exact = normalize_bool(source_row.get("exact_match", ""))

    failure_category = (source_row.get("failure_category") or "").strip()
    if executed == "true" and exact == "true":
        result_status = "exact"
        failure_stage = "not_applicable"
        failure_type = "not_applicable"
    elif executed == "true" and exact == "false":
        result_status = "mismatch"
        failure_stage = "checker"
        failure_type = failure_category if failure_category and failure_category != "none" else "result_mismatch"
    elif executed == "false":
        result_status = "failed"
        failure_stage = "execution"
        failure_type = failure_category if failure_category and failure_category != "none" else "execution_failed"
    else:
        result_status = "unknown"
        failure_stage = "unknown"
        failure_type = failure_category if failure_category and failure_category != "none" else "unknown"

    return {
        "generated": "requires_production_retained_evidence",
        "ready": "requires_production_retained_evidence",
        "executed": executed,
        "exact": exact,
        "result_status": result_status,
        "failure_stage": failure_stage,
        "failure_type": failure_type,
        "parse_status": "requires_production_retained_evidence",
        "checker_status": (source_row.get("checker_status") or "unknown").strip() or "unknown",
    }


def project_source(manifest_row: dict[str, str], out_dir: Path) -> tuple[dict[str, str], list[dict[str, str]], list[str]]:
    source_id = manifest_row["source_id"]
    rewrite_method = manifest_row["rewrite_method"]
    source_path_value = manifest_row["source_path"]
    source_path = source_path_to_legacy(source_path_value)
    rows, fieldnames = read_csv(source_path)
    missing = [column for column in SOURCE_SAFE_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(f"{source_id} missing safe columns: {missing}")

    route = ROUTE_BY_METHOD[rewrite_method]
    projected: list[dict[str, str]] = []
    for source_row in rows:
        safe = {column: source_row.get(column, "") for column in SOURCE_SAFE_COLUMNS}
        if safe["route_id"] != route:
            continue
        engine = ENGINE_ALIASES.get(safe["engine"].strip().lower(), safe["engine"].strip().lower())
        denominator_id = f"track_a_same_engine:{safe['case_id']}:{engine}"
        status = map_status(safe)
        projection_id = f"projection_{source_id}_{rewrite_method}"
        row_grain_key = "|".join([safe["case_id"], engine, rewrite_method, denominator_id])
        projected.append(
            {
                "projection_id": projection_id,
                "source_id": source_id,
                "source_row_id": safe["row_id"],
                "source_path": source_path_value,
                "case_id": safe["case_id"],
                "pool": safe["pool"],
                "engine": engine,
                "source_denominator_id": safe["denominator_id"],
                "denominator_id": denominator_id,
                "rewrite_method": rewrite_method,
                "route_id": safe["route_id"],
                "method_id": safe["method_id"],
                "generated": status["generated"],
                "ready": status["ready"],
                "executed": status["executed"],
                "exact": status["exact"],
                "result_status": status["result_status"],
                "failure_stage": status["failure_stage"],
                "failure_type": status["failure_type"],
                "parse_status": status["parse_status"],
                "checker_status": status["checker_status"],
                "evidence_source": f"sanitized_sqlglot_projection:{source_id}",
                "retained_artifact_path": f"{source_path_value}#row_id={safe['row_id']}",
                "row_grain_key": row_grain_key,
                "row_grain_verified": "true",
                "notes": "sanitized non-timing checker event projection; generated/ready not inferred from checker paths",
            }
        )

    grain_counts = Counter(row["row_grain_key"] for row in projected)
    row_grain_verified = all(count == 1 for count in grain_counts.values())
    for row in projected:
        row["row_grain_verified"] = str(row_grain_verified).lower()

    output_name = f"projection_{source_id}_{rewrite_method}_non_timing.csv"
    output_path = out_dir / output_name
    write_csv(output_path, projected, PROJECTION_FIELDS)

    retained = SOURCE_SAFE_COLUMNS
    dropped = [column for column in fieldnames if column not in retained]
    timing_removed = any(
        token in column.lower()
        for column in dropped
        for token in ("runtime", "latency", "speedup", "timing", "duration")
    )
    prompt_removed = any(
        token in column.lower() for column in dropped for token in ("prompt", "token", "api", "model")
    )
    raw_removed = any(token in column.lower() for column in dropped for token in ("stdout", "stderr", "log"))
    index_row = {
        "projection_id": f"projection_{source_id}_{rewrite_method}",
        "source_id": source_id,
        "source_path": source_path_value,
        "projection_path": str(output_path),
        "rewrite_method": rewrite_method,
        "row_count": str(len(projected)),
        "columns_retained": "|".join(PROJECTION_FIELDS),
        "columns_dropped": "|".join(dropped),
        "row_grain_verified": str(row_grain_verified).lower(),
        "timing_columns_removed": str(timing_removed).lower(),
        "prompt_token_columns_removed": str(prompt_removed).lower(),
        "raw_log_columns_removed": str(raw_removed).lower(),
        "parser_ready": str(bool(projected) and row_grain_verified).lower(),
        "notes": "projection contains only sanitized non-timing status fields; artifact payload path columns are dropped",
    }
    return index_row, projected, dropped


def write_report(path: Path, index_rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    lines = [
        "# SQLGlot Non-Timing Projection Report",
        "",
        "## Purpose And Scope",
        "",
        "This audit step projects approved SQLGlot status evidence into sanitized non-timing CSV files.",
        "It does not fill candidate ledgers, compute metrics, authorize metric input, or read artifact payloads.",
        "",
        "## Projection Summary",
        "",
        f"- Projections created: {summary['projections_created']}",
        f"- Projection rows total: {summary['projection_rows_total']}",
        f"- Parser-ready projections: {summary['parser_ready_projection_count']}",
        "",
        "## Projection Index",
        "",
    ]
    lines.extend(
        f"- `{row['projection_id']}`: {row['row_count']} rows, parser_ready={row['parser_ready']}"
        for row in index_rows
    )
    lines.extend(
        [
            "",
            "## Boundary Confirmation",
            "",
            "- Timing/speedup/latency fields are not retained.",
            "- Raw logs, stdout/stderr payloads, prompts, tokens, and model traces are not opened or retained.",
            "- Generated/ready are not inferred from checker artifact path presence.",
            "- Metrics computed: false",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows, _ = read_csv(args.manifest)
    approved = [row for row in manifest_rows if row.get("approved_for_projection") == "true"]
    index_rows: list[dict[str, str]] = []
    total_rows = 0
    any_timing_removed = False
    any_prompt_removed = False
    any_raw_removed = False
    for manifest_row in approved:
        index_row, projected, dropped = project_source(manifest_row, args.out_dir)
        index_rows.append(index_row)
        total_rows += len(projected)
        any_timing_removed = any_timing_removed or index_row["timing_columns_removed"] == "true"
        any_prompt_removed = any_prompt_removed or index_row["prompt_token_columns_removed"] == "true"
        any_raw_removed = any_raw_removed or index_row["raw_log_columns_removed"] == "true"
        _ = dropped

    write_csv(args.out_dir / "sqlglot_non_timing_projection_index.csv", index_rows, INDEX_FIELDS)
    parser_ready_count = sum(1 for row in index_rows if row["parser_ready"] == "true")
    summary = {
        "projections_created": len(index_rows),
        "projection_rows_total": total_rows,
        "parser_ready_projection_count": parser_ready_count,
        "timing_columns_removed": any_timing_removed,
        "prompt_token_columns_removed": any_prompt_removed,
        "raw_log_columns_removed": any_raw_removed,
        "metrics_computed": False,
        "reports_changed": False,
        "results_changed": False,
    }
    (args.out_dir / "sqlglot_non_timing_projection_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir / "sqlglot_non_timing_projection_report.md", index_rows, summary)
    checks = [
        {
            "check_name": "only approved manifest rows projected",
            "status": "PASS",
            "details": f"{len(approved)} approved manifest rows produced {len(index_rows)} projections",
        },
        {
            "check_name": "row grain verified",
            "status": "PASS" if all(row["row_grain_verified"] == "true" for row in index_rows) else "FAIL",
            "details": "case_id x engine x rewrite_method x release denominator_id is unique within each projection",
        },
        {
            "check_name": "timing fields retained",
            "status": "PASS",
            "details": "false",
        },
        {
            "check_name": "prompt/token fields retained",
            "status": "PASS",
            "details": "false",
        },
        {
            "check_name": "raw log fields retained",
            "status": "PASS",
            "details": "false",
        },
        {
            "check_name": "metrics computed",
            "status": "PASS",
            "details": "false",
        },
    ]
    write_csv(args.out_dir / "sqlglot_non_timing_projection_checks.csv", checks, CHECK_FIELDS)
    print(f"projections_created: {len(index_rows)}")
    print(f"projection_rows_total: {total_rows}")
    print(f"parser_ready_projection_count: {parser_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
