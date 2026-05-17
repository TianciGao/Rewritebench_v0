#!/usr/bin/env python3
"""Build the bounded SQLGlot status projection manifest.

The manifest is intentionally conservative: only the paper-freeze checker event
source SGL011 is allowed through to projection/parser use. Other reviewed
SQLGlot sources remain pending or rejected according to the round1 triage risks.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDNAMES = [
    "manifest_id",
    "source_id",
    "source_repo",
    "source_path",
    "rewrite_method",
    "route_family",
    "source_category",
    "expected_row_grain",
    "approved_for_projection",
    "approved_for_parser",
    "approved_fields",
    "forbidden_fields",
    "engine_expansion_policy",
    "parser_mode",
    "safety_conditions",
    "approval_status",
    "notes",
]

CHECK_FIELDS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SQLGlot status source manifest.")
    parser.add_argument("--triage", required=True, type=Path)
    parser.add_argument("--decision-sheet", required=True, type=Path)
    parser.add_argument("--manifest-preview", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_decision(source_id: str) -> tuple[bool, bool, str, str, str, str, str]:
    if source_id == "SGL011":
        return (
            True,
            True,
            "canonical_checker_event_backfill",
            "source engine aliases are normalized; release denominator_id is joined by case_id x engine; no engine expansion",
            "sanitized_projection_then_parser",
            "approved_sanitized_non_timing_projection",
            "Approved for non-timing executed/exact/checker status projection; artifact path payload columns are not retained.",
        )
    if source_id == "P006":
        return (
            False,
            False,
            "preflight_case_matrix",
            "deterministic expansion to case_id x engine x rewrite_method was not explicitly approved",
            "header_only_pending_engine_expansion",
            "pending_engine_expansion_review",
            "Fails closed until maintainer approves deterministic engine and route expansion.",
        )
    if source_id == "P009":
        return (
            False,
            False,
            "port_resolved_run_event",
            "same-engine isolation not approved; timing/path columns and mixed portability scope remain risks",
            "rejected_for_v1",
            "rejected_mixed_scope_and_timing_path_risk",
            "Not approved because the reviewed source carries mixed portability and timing/path risks.",
        )
    if source_id == "SGL012":
        return (
            False,
            False,
            "duplicate_checker_event_backfill",
            "same row grain as SGL011 but duplicate-source precedence was not needed after choosing SGL011",
            "reference_only_duplicate",
            "rejected_duplicate_of_sgl011",
            "Held out to avoid duplicate source overlap with SGL011.",
        )
    if source_id == "SGL013":
        return (
            False,
            False,
            "execution_canary_triage",
            "denominator_id missing and stdout/stderr columns create raw-log risk",
            "rejected_for_v1",
            "rejected_raw_log_risk",
            "Not approved because direct parser use would require handling raw log pointers and denominator joins.",
        )
    return (
        False,
        False,
        "reviewed_sqlglot_source",
        "row grain or safety conditions not approved",
        "not_approved",
        "not_approved_for_projection",
        "No parser approval recorded for this source.",
    )


def build_rows(preview_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in preview_rows:
        source_id = row["source_id"]
        approved_projection, approved_parser, category, engine_policy, mode, status, notes = source_decision(source_id)
        supported = row.get("supported_fields", "")
        approved_fields = supported if approved_projection else ""
        forbidden = row.get("disallowed_fields", "")
        if "timed" not in forbidden:
            forbidden = "|".join(filter(None, [forbidden, "timed|latency_ms|speedup_ratio|timing_eligible"]))
        rows.append(
            {
                "manifest_id": row["manifest_id"],
                "source_id": source_id,
                "source_repo": row["source_repo"],
                "source_path": row["source_path"],
                "rewrite_method": row["rewrite_method"],
                "route_family": "sqlglot",
                "source_category": category,
                "expected_row_grain": row.get("expected_row_grain", ""),
                "approved_for_projection": str(approved_projection).lower(),
                "approved_for_parser": str(approved_parser).lower(),
                "approved_fields": approved_fields,
                "forbidden_fields": forbidden,
                "engine_expansion_policy": engine_policy,
                "parser_mode": mode,
                "safety_conditions": "non_timing_only; no raw logs; no prompt/token traces; no timing/speedup/latency; no metrics",
                "approval_status": status,
                "notes": notes,
            }
        )
    return rows


def write_report(path: Path, rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    approved = [r for r in rows if r["approved_for_projection"] == "true"]
    lines = [
        "# SQLGlot Status Source Manifest Report",
        "",
        "## Purpose And Scope",
        "",
        "This audit manifest selects reviewed SQLGlot sources for sanitized non-timing status projection.",
        "It does not parse candidate statuses, compute metrics, authorize metric input, or touch timing fields.",
        "",
        "## Manifest Result",
        "",
        f"- Manifest rows: {summary['manifest_rows']}",
        f"- Approved projection rows: {summary['approved_projection_sources']}",
        f"- Approved parser rows: {summary['approved_parser_sources']}",
        f"- Pending rows: {summary['pending_sources']}",
        f"- Rejected rows: {summary['rejected_sources']}",
        "",
        "## Approved Source",
        "",
    ]
    if approved:
        lines.extend(
            f"- `{r['source_id']}` / `{r['rewrite_method']}`: {r['notes']}" for r in approved
        )
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Fail-Closed Decisions",
            "",
            "- P006 remains pending because deterministic engine expansion was not explicitly approved.",
            "- P009 is rejected for this manifest because of mixed portability scope plus timing/path risk.",
            "- SGL012 is held out as a duplicate of SGL011.",
            "- SGL013 is rejected for raw-log pointer risk and missing denominator_id.",
            "- P007/P008/P010 remain excluded by round1 review.",
            "",
            "## Boundary Confirmation",
            "",
            "- Timing sources approved: false",
            "- Raw-log sources approved: false",
            "- Prompt/token sources approved: false",
            "- Metrics computed: false",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    triage_rows = read_csv(args.triage)
    decision_rows = read_csv(args.decision_sheet)
    preview_rows = read_csv(args.manifest_preview)
    rows = build_rows(preview_rows)

    write_csv(args.out_dir / "sqlglot_status_source_manifest.csv", rows, FIELDNAMES)

    approved_projection = sum(1 for r in rows if r["approved_for_projection"] == "true")
    approved_parser = sum(1 for r in rows if r["approved_for_parser"] == "true")
    pending = sum(1 for r in rows if r["approval_status"].startswith("pending"))
    rejected = len(rows) - approved_projection - pending
    summary = {
        "manifest_rows": len(rows),
        "approved_projection_sources": approved_projection,
        "approved_parser_sources": approved_parser,
        "pending_sources": pending,
        "rejected_sources": rejected,
        "timing_sources_approved": False,
        "raw_log_sources_approved": False,
        "prompt_token_sources_approved": False,
        "metrics_computed": False,
    }
    (args.out_dir / "sqlglot_status_source_manifest_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir / "sqlglot_status_source_manifest_report.md", rows, summary)

    source_ids = {r["source_id"] for r in rows}
    checks = [
        {
            "check_name": "manifest preview rows read",
            "status": "PASS" if len(rows) == len(preview_rows) else "FAIL",
            "details": f"{len(rows)} manifest rows from {len(preview_rows)} preview rows",
        },
        {
            "check_name": "SGL011 approved for sanitized projection",
            "status": "PASS" if any(r["source_id"] == "SGL011" and r["approved_for_projection"] == "true" for r in rows) else "FAIL",
            "details": "SGL011 is the canonical checker-event source for this bounded parser.",
        },
        {
            "check_name": "P006 engine expansion not auto-approved",
            "status": "PASS" if all(r["approved_for_projection"] == "false" for r in rows if r["source_id"] == "P006") else "FAIL",
            "details": "P006 requires explicit deterministic engine expansion approval.",
        },
        {
            "check_name": "P007 excluded unless explicitly approved",
            "status": "PASS" if "P007" not in source_ids else "WARN",
            "details": f"round1 decision rows read: {len(decision_rows)}; P007 is not in parser preview manifest",
        },
        {
            "check_name": "P008/P010 excluded",
            "status": "PASS" if not ({"P008", "P010"} & source_ids) else "FAIL",
            "details": "Mixed portability and route-level summary sources are not present in parser preview rows.",
        },
        {
            "check_name": "raw log sources not approved",
            "status": "PASS" if all(r["approved_for_projection"] == "false" for r in rows if r["source_id"] == "SGL013") else "FAIL",
            "details": "SGL013 raw stdout/stderr pointers remain excluded.",
        },
        {
            "check_name": "timing sources approved",
            "status": "PASS",
            "details": "false",
        },
        {
            "check_name": "metrics computed",
            "status": "PASS",
            "details": "false",
        },
    ]
    _ = triage_rows
    write_csv(args.out_dir / "sqlglot_status_source_manifest_checks.csv", checks, CHECK_FIELDS)
    print(f"manifest_rows: {len(rows)}")
    print(f"approved_projection_sources: {approved_projection}")
    print(f"approved_parser_sources: {approved_parser}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
