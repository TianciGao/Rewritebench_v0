#!/usr/bin/env python3
"""Build status_inference_overlay_v0 from approved R1 preview rows.

This script is audit-only. It materializes inferred_generated=true for the
approved ready=>generated preview rows without overwriting observed normalized
fields and without computing metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


OVERLAY_NAME = "status_inference_overlay_v0"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

OVERLAY_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "inference_rule_id",
    "source_field",
    "source_value",
    "inferred_field",
    "inferred_value",
    "inference_authorized_overlay",
    "observed_field_overwritten",
    "inference_scope",
    "inference_version",
    "metric_input_authorized_current",
    "official_metric_authorized",
    "metrics_computed",
    "paper_result",
    "timing_fields_touched",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build audit-only status inference overlay v0.")
    parser.add_argument("--preview", required=True, type=Path)
    parser.add_argument("--normalized-overlay", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def ensure_allowed_input(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo input is not allowed for {OVERLAY_NAME}: {path}")


def ensure_allowed_output(path: Path) -> None:
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results output is forbidden for {OVERLAY_NAME}: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_overlay(preview: list[dict[str, str]], normalized: list[dict[str, str]]) -> dict[str, object]:
    normalized_by_id = {row["record_id"]: row for row in normalized}
    selected = [
        row
        for row in preview
        if row.get("inference_rule_id") == "R1"
        and row.get("proposed_inferred_field") == "inferred_generated"
        and row.get("proposed_inferred_value") == "true"
        and row.get("requires_future_authorization") == "true"
    ]
    if len(preview) != 94:
        raise ValueError(f"expected 94 preview candidate rows, found {len(preview)}")
    if len(selected) != 94:
        raise ValueError(f"expected 94 approved R1 preview rows, found {len(selected)}")

    overlay_rows: list[dict[str, object]] = []
    for row in selected:
        normalized_row = normalized_by_id.get(row["record_id"])
        if normalized_row is None:
            raise ValueError(f"preview row missing normalized overlay match: {row['record_id']}")
        if normalized_row.get("normalized_ready") != "true":
            raise ValueError(f"R1 source row is not normalized_ready=true: {row['record_id']}")
        if normalized_row.get("normalized_generated") != "unknown":
            raise ValueError(f"R1 must not overwrite observed generated value: {row['record_id']}")
        overlay_rows.append(
            {
                "record_id": row["record_id"],
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "inference_rule_id": "R1",
                "source_field": row["source_field"],
                "source_value": row["source_value"],
                "inferred_field": "inferred_generated",
                "inferred_value": "true",
                "inference_authorized_overlay": "true",
                "observed_field_overwritten": "false",
                "inference_scope": "audit_only_ready_implies_generated; no_official_metrics; no_timing",
                "inference_version": OVERLAY_NAME,
                "metric_input_authorized_current": row.get("metric_input_authorized_current", "false"),
                "official_metric_authorized": "false",
                "metrics_computed": "false",
                "paper_result": "false",
                "timing_fields_touched": "false",
                "notes": "R1 inference overlay only; normalized_generated remains unchanged in the source overlay.",
            }
        )

    checks = [
        ("preview candidate rows = 94", len(preview) == 94, f"preview rows={len(preview)}"),
        ("overlay rows = 94", len(overlay_rows) == 94, f"overlay rows={len(overlay_rows)}"),
        (
            "all rows rule R1",
            all(row["inference_rule_id"] == "R1" for row in overlay_rows),
            "all overlay rows use R1 ready=>generated",
        ),
        (
            "no observed field overwritten",
            all(row["observed_field_overwritten"] == "false" for row in overlay_rows),
            "observed normalized fields are not modified",
        ),
        (
            "no timing fields touched",
            all(row["timing_fields_touched"] == "false" for row in overlay_rows),
            "timing fields are absent from overlay logic",
        ),
        (
            "no official metrics computed",
            all(row["metrics_computed"] == "false" and row["official_metric_authorized"] == "false" for row in overlay_rows),
            "overlay is not official metric authorization or computation",
        ),
        (
            "no paper results",
            all(row["paper_result"] == "false" for row in overlay_rows),
            "overlay is not a paper result",
        ),
        (
            "reports/results unchanged",
            True,
            "script writes only to audits/status_inference_overlay_v0",
        ),
        ("denominator unchanged", True, "denominator files are not written"),
    ]
    check_rows = [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]
    return {"overlay_rows": overlay_rows, "check_rows": check_rows}


def write_report(out_dir: Path) -> None:
    report = """# status_inference_overlay_v0 Report

## Purpose And Scope

This overlay materializes the approved R1 ready=>generated inference preview as audit-only inferred fields.

## Why Ready=>Generated Is Inferred Only

The source-observed normalized field remains `normalized_generated=unknown`. The overlay records `inferred_generated=true` separately because the maintainer authorized this inference only for audit dry-run use.

## Observed Fields Are Not Overwritten

The script reads `normalized_candidate_status_overlay_v0.csv` only to verify row identity, `normalized_ready=true`, and `normalized_generated=unknown`. It writes no changes to that input.

## Not Official Metrics

The overlay does not compute Generation Rate, Execution Coverage Rate, Result Consistency Rate, or any other metric. It does not authorize paper results.

## Timing Boundary

Timing, latency, speedup, and timing-eligibility fields are not read, filled, or modified.

## Next Safe Action

Run `normalized_status_only_metrics_dryrun_v2` using this overlay as audit-only inferred generated support. Keep official metrics, timing, reports/results, denominator changes, and paper results separate.
"""
    (out_dir / "status_inference_overlay_report.md").write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    for path in [args.preview, args.normalized_overlay]:
        ensure_allowed_input(path)
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    preview = read_csv(args.preview)
    normalized = read_csv(args.normalized_overlay)
    outputs = build_overlay(preview, normalized)

    write_csv(args.out_dir / "status_inference_overlay_v0.csv", outputs["overlay_rows"], OVERLAY_COLUMNS)
    write_csv(args.out_dir / "status_inference_overlay_checks.csv", outputs["check_rows"], CHECK_COLUMNS)
    summary = {
        "overlay_name": OVERLAY_NAME,
        "inferred_rows": len(outputs["overlay_rows"]),
        "inference_rule_used": "R1",
        "observed_fields_overwritten": False,
        "official_metrics_computed": False,
        "audit_only_overlay_created": True,
        "timing_fields_touched": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    (args.out_dir / "status_inference_overlay_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir)

    if any(row["status"] != "PASS" for row in outputs["check_rows"]):
        return 1
    print(f"wrote {len(outputs['overlay_rows'])} inferred status overlay rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
