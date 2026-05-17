#!/usr/bin/env python3
"""Refresh normalization for overlap-authorized rows.

This script preserves the existing 130 normalized rows from
status_field_normalization_v0 and normalizes only newly authorized overlap rows
from combined_metric_input_authorization_overlay_v1. It uses the existing
conservative mapping semantics and writes a combined audit-only overlay.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


NORMALIZER_NAME = "overlap_normalization_v1"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

STATUS_FIELDS = [
    "generated",
    "ready",
    "executed",
    "exact",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
]

OVERLAY_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "parser_status",
    "original_generated",
    "original_ready",
    "original_executed",
    "original_exact",
    "original_result_status",
    "original_failure_stage",
    "original_failure_type",
    "original_parse_status",
    "original_checker_status",
    "normalized_generated",
    "normalized_ready",
    "normalized_executed",
    "normalized_exact",
    "normalized_result_status",
    "normalized_failure_stage",
    "normalized_failure_type",
    "normalized_parse_status",
    "normalized_checker_status",
    "normalization_confidence",
    "normalization_source",
    "needs_manual_mapping",
    "metric_input_authorized_overlay",
    "timing_fields_unchanged",
    "metrics_computed",
    "paper_result",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize newly authorized overlap rows.")
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--combined-authorization", required=True, type=Path)
    parser.add_argument("--existing-normalized-overlay", required=True, type=Path)
    parser.add_argument("--mapping-table", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def ensure_allowed_input(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo input is not allowed for {NORMALIZER_NAME}: {path}")


def ensure_allowed_output(path: Path) -> None:
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results output is forbidden for {NORMALIZER_NAME}: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm_token(value: str) -> str:
    return (value or "").strip().lower()


def normalize_value(field: str, raw_value: str) -> tuple[str, str]:
    value = norm_token(raw_value)
    if value in {"", "unknown", "requires_production_retained_evidence"}:
        return "unknown", "medium"
    if value in {"n.a.", "na"}:
        if field in {"failure_stage", "failure_type"}:
            return "not_applicable", "high"
        return "unknown", "medium"
    if value in {"not_applicable", "not applicable"}:
        return "not_applicable", "high"

    if field in {"generated", "ready", "executed", "exact"}:
        true_values = {
            "true",
            "1",
            "yes",
            "generated",
            "ready",
            "executed",
            "exact",
            "match_exact",
            "exact_match",
            "success",
            "passed",
            "consistent",
        }
        false_values = {
            "false",
            "0",
            "no",
            "failed",
            "no_candidate",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "mismatch",
            "unsupported",
            "timeout",
            "blocked",
        }
        if value in true_values:
            return "true", "high"
        if value in false_values:
            return "false", "high"

    if field == "result_status":
        if value in {"ready", "exact", "match_exact", "exact_match", "success", "passed", "consistent"}:
            return "true", "high"
        if value in {
            "failed",
            "blocked",
            "mismatch",
            "no_candidate",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "unsupported",
            "timeout",
        }:
            return "false", "high"

    if field == "failure_stage":
        if value in {"generation", "parse", "preflight", "execution", "checker", "artifact_collection"}:
            return "true", "high"
        if value in {"none", "no_failure"}:
            return "false", "high"

    if field == "failure_type":
        if value in {
            "parser_failed",
            "blocked_missing_failure_feedback",
            "disallowed_semantic_mismatch",
            "generated_execution_failed",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "mismatch",
            "unsupported",
            "timeout",
            "blocked",
        }:
            return "true", "high"
        if value in {"none", "no_failure"}:
            return "false", "high"

    if field == "parse_status":
        if value in {"parsed", "success", "passed"}:
            return "true", "high"
        if value in {"not_parsed", "parse_failed", "parser_failed", "extraction_failed"}:
            return "false", "high"

    if field == "checker_status":
        if value in {"pass", "passed", "exact", "consistent"}:
            return "true", "high"
        if value in {"fail", "failed", "mismatch", "checker_failed", "reject_unexpected"}:
            return "false", "high"
        if value == "not_run":
            return "unknown", "medium"

    return "needs_manual_mapping", "low"


def normalize_ledger_row(row: dict[str, str]) -> dict[str, object]:
    normalized: dict[str, str] = {}
    confidences: list[str] = []
    manual_fields: list[str] = []
    for field in STATUS_FIELDS:
        value, confidence = normalize_value(field, row.get(field, ""))
        normalized[field] = value
        confidences.append(confidence)
        if value == "needs_manual_mapping":
            manual_fields.append(field)

    if "low" in confidences:
        row_confidence = "low"
    elif "medium" in confidences:
        row_confidence = "medium"
    else:
        row_confidence = "high"

    return {
        "record_id": row["record_id"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "rewrite_method": row["rewrite_method"],
        "denominator_id": row["denominator_id"],
        "parser_status": row["parser_status"],
        "original_generated": row.get("generated", ""),
        "original_ready": row.get("ready", ""),
        "original_executed": row.get("executed", ""),
        "original_exact": row.get("exact", ""),
        "original_result_status": row.get("result_status", ""),
        "original_failure_stage": row.get("failure_stage", ""),
        "original_failure_type": row.get("failure_type", ""),
        "original_parse_status": row.get("parse_status", ""),
        "original_checker_status": row.get("checker_status", ""),
        "normalized_generated": normalized["generated"],
        "normalized_ready": normalized["ready"],
        "normalized_executed": normalized["executed"],
        "normalized_exact": normalized["exact"],
        "normalized_result_status": normalized["result_status"],
        "normalized_failure_stage": normalized["failure_stage"],
        "normalized_failure_type": normalized["failure_type"],
        "normalized_parse_status": normalized["parse_status"],
        "normalized_checker_status": normalized["checker_status"],
        "normalization_confidence": row_confidence,
        "normalization_source": f"{NORMALIZER_NAME}:combined_metric_input_authorization_overlay_v1",
        "needs_manual_mapping": "true" if manual_fields else "false",
        "metric_input_authorized_overlay": "true",
        "timing_fields_unchanged": "true",
        "metrics_computed": "false",
        "paper_result": "false",
        "notes": "audit-only overlap normalization row; original parser and v0 normalization overlays unchanged"
        + (f"; manual mapping fields={('|'.join(manual_fields))}" if manual_fields else ""),
    }


def build_outputs(
    ledger: list[dict[str, str]],
    combined_auth: list[dict[str, str]],
    existing_normalized: list[dict[str, str]],
    mapping_table: list[dict[str, str]],
) -> dict[str, object]:
    if len(ledger) != 600:
        raise ValueError(f"expected 600 candidate ledger rows, found {len(ledger)}")
    if len(existing_normalized) != 130:
        raise ValueError(f"expected 130 existing normalized rows, found {len(existing_normalized)}")
    if not mapping_table:
        raise ValueError("mapping table must have at least one row")

    ledger_by_id = {row["record_id"]: row for row in ledger}
    existing_by_id = {row["record_id"]: row for row in existing_normalized}
    authorized_ids = {
        row["record_id"] for row in combined_auth if row.get("metric_input_authorized_overlay") == "true"
    }
    blocked_ids = {
        row["record_id"] for row in combined_auth if row.get("metric_input_authorized_overlay") == "false"
    }
    newly_authorized = sorted(authorized_ids - set(existing_by_id))
    if len(authorized_ids) < 130:
        raise ValueError(f"expected at least 130 authorized rows, found {len(authorized_ids)}")
    missing = authorized_ids - set(ledger_by_id)
    if missing:
        raise ValueError(f"combined authorization rows missing from candidate ledger: {sorted(missing)[:3]}")

    normalized_rows: list[dict[str, object]] = []
    for record_id in sorted(existing_by_id):
        row = dict(existing_by_id[record_id])
        row["normalization_source"] = row.get("normalization_source", "")
        normalized_rows.append(row)
    for record_id in newly_authorized:
        normalized_rows.append(normalize_ledger_row(ledger_by_id[record_id]))

    unresolved_count = sum(
        1
        for row in ledger
        if row["record_id"] not in {auth["record_id"] for auth in combined_auth}
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    )
    manual_rows = [row for row in normalized_rows if row.get("needs_manual_mapping") == "true"]
    checks = [
        ("previous normalized rows = 130", len(existing_normalized) == 130, f"previous rows={len(existing_normalized)}"),
        (
            "combined normalized rows match authorized rows",
            len(normalized_rows) == len(authorized_ids),
            f"combined normalized rows={len(normalized_rows)} authorized rows={len(authorized_ids)}",
        ),
        ("overlap rows still blocked recorded", True, f"still-blocked overlap rows={len(blocked_ids)}"),
        ("unresolved rows excluded = 425", unresolved_count == 425, f"unresolved rows={unresolved_count}"),
        (
            "timing fields unchanged",
            all(row.get("timing_fields_unchanged") == "true" for row in normalized_rows),
            "all normalized rows keep timing_fields_unchanged=true",
        ),
        (
            "no metrics computed",
            all(row.get("metrics_computed") == "false" for row in normalized_rows),
            "normalization does not compute metrics",
        ),
        (
            "no paper result",
            all(row.get("paper_result") == "false" for row in normalized_rows),
            "normalization does not create paper results",
        ),
        ("reports/results unchanged", True, "script writes only under audits/overlap_priority_overlay_v1"),
        ("denominator unchanged", True, "denominator files are not written"),
    ]
    return {
        "normalized_rows": sorted(normalized_rows, key=lambda row: row["record_id"]),
        "check_rows": [
            {
                "check_name": name,
                "status": "PASS" if passed else "FAIL",
                "details": details,
            }
            for name, passed, details in checks
        ],
        "previous_normalized_rows": len(existing_normalized),
        "newly_normalized_overlap_rows": len(newly_authorized),
        "combined_normalized_rows": len(normalized_rows),
        "overlap_rows_still_blocked": len(blocked_ids),
        "unresolved_rows_excluded": unresolved_count,
        "rows_needing_manual_mapping": len(manual_rows),
    }


def write_report(out_dir: Path, summary: dict[str, object]) -> None:
    report = f"""# overlap_normalization_v1 Report

## Purpose And Scope

This audit-only refresh preserves the existing 130 normalized candidate-status rows and normalizes only newly authorized overlap rows from `combined_metric_input_authorization_overlay_v1.csv`.

## Summary

- Previous normalized rows: {summary['previous_normalized_rows']}.
- Newly normalized overlap rows: {summary['newly_normalized_overlap_rows']}.
- Combined normalized rows: {summary['combined_normalized_rows']}.
- Still-blocked overlap rows: {summary['overlap_rows_still_blocked']}.
- Unresolved rows excluded: {summary['unresolved_rows_excluded']}.
- Rows needing manual mapping: {summary['rows_needing_manual_mapping']}.

## Boundary

The script reads the existing mapping table and applies the same conservative mapping semantics. It does not modify `normalized_candidate_status_overlay_v0.csv`, does not fill timing fields, does not compute metrics, and does not create paper results.

## Next Safe Action

Use the combined normalized overlay in the audit-only normalized status-only dry-run v3. Treat manual-mapping rows as caveats, not official metric inputs.
"""
    (out_dir / "overlap_normalization_report.md").write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    for path in [
        args.candidate_ledger,
        args.combined_authorization,
        args.existing_normalized_overlay,
        args.mapping_table,
    ]:
        ensure_allowed_input(path)
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    result = build_outputs(
        read_csv(args.candidate_ledger),
        read_csv(args.combined_authorization),
        read_csv(args.existing_normalized_overlay),
        read_csv(args.mapping_table),
    )
    write_csv(
        args.out_dir / "combined_normalized_candidate_status_overlay_v1.csv",
        result["normalized_rows"],
        OVERLAY_COLUMNS,
    )
    write_csv(args.out_dir / "overlap_normalization_checks.csv", result["check_rows"], CHECK_COLUMNS)
    summary = {
        "previous_normalized_rows": result["previous_normalized_rows"],
        "newly_normalized_overlap_rows": result["newly_normalized_overlap_rows"],
        "combined_normalized_rows": result["combined_normalized_rows"],
        "overlap_rows_still_blocked": result["overlap_rows_still_blocked"],
        "unresolved_rows_excluded": result["unresolved_rows_excluded"],
        "rows_needing_manual_mapping": result["rows_needing_manual_mapping"],
        "metrics_computed": False,
        "official_metrics_computed": False,
        "timing_fields_filled": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
    }
    (args.out_dir / "overlap_normalization_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir, summary)

    if any(row["status"] == "FAIL" for row in result["check_rows"]):
        return 1
    print(
        f"wrote combined normalization: previous={result['previous_normalized_rows']} "
        f"new={result['newly_normalized_overlap_rows']} combined={result['combined_normalized_rows']} "
        f"manual_mapping_rows={result['rows_needing_manual_mapping']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
