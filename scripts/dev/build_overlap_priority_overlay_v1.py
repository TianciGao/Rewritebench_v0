#!/usr/bin/env python3
"""Build audit-only overlap priority overlay v1.

This script resolves only the 45 candidate-status rows previously denied for
source overlap. It applies the maintainer-approved Option B policy:

- P001 provides generation/readiness evidence.
- P002 provides primary candidate status.
- P003 provides Repair-1 failure enrichment only.
- P003 must not override P002 primary status.

It does not modify parser ledgers, does not modify overlay v0, and does not
compute official metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


OVERLAY_NAME = "overlap_priority_overlay_v1"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

OVERLAY_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "overlap_sources",
    "applied_priority_policy",
    "resolved_by_policy",
    "authorize_metric_input_overlay_v1",
    "fields_authorized",
    "fields_still_blocked",
    "failure_enrichment_source",
    "p003_can_override_primary_status",
    "timing_authorized",
    "official_metric_authorized",
    "metrics_computed",
    "paper_result",
    "notes",
]

COMBINED_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "authorization_source",
    "authorization_version",
    "metric_input_authorized_overlay",
    "authorization_reason",
    "timing_authorized",
    "official_metric_authorized",
    "metrics_computed",
    "paper_result",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build overlap priority overlay v1.")
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--readiness-review", required=True, type=Path)
    parser.add_argument("--denied-rows", required=True, type=Path)
    parser.add_argument("--overlap-proposal", required=True, type=Path)
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


def policy_for(row: dict[str, str], proposal: dict[str, str]) -> tuple[bool, str, str, str]:
    sources = row.get("source_ids_used", "")
    method = row["rewrite_method"]
    proposed = proposal.get("proposed_resolution", "")
    if (
        method == "direct_llm_original"
        and sources == "P001|P002"
        and proposed == "approve_p001_generation_p002_status_priority"
    ):
        return (
            True,
            "option_b:p001_generation_readiness_p002_primary_status",
            "generated|ready from P001; executed|exact|result_status|failure_stage|failure_type|parse_status|checker_status|retained_artifact_path|evidence_source from P002 where available",
            "",
        )
    if (
        method == "direct_llm_repair_1"
        and sources == "P002|P003"
        and proposed == "approve_p002_primary_p003_failure_enrichment_only"
    ):
        return (
            True,
            "option_b:p002_primary_status_p003_failure_enrichment_only",
            "generated|ready|executed|exact|result_status|parse_status|checker_status|retained_artifact_path|evidence_source from P002 where available; failure_stage|failure_type may be enriched from P003",
            "P003",
        )
    return False, "option_b:unresolved_source_pattern", "none", ""


def build_outputs(
    ledger: list[dict[str, str]],
    readiness: list[dict[str, str]],
    denied: list[dict[str, str]],
    proposals: list[dict[str, str]],
) -> dict[str, object]:
    if len(ledger) != 600:
        raise ValueError(f"expected 600 candidate ledger rows, found {len(ledger)}")
    if len(readiness) != 175:
        raise ValueError(f"expected 175 readiness rows, found {len(readiness)}")
    if len(denied) != 45:
        raise ValueError(f"expected 45 denied overlap rows, found {len(denied)}")
    if len(proposals) != 45:
        raise ValueError(f"expected 45 overlap proposal rows, found {len(proposals)}")

    ledger_by_id = {row["record_id"]: row for row in ledger}
    readiness_by_id = {row["record_id"]: row for row in readiness}
    proposal_by_id = {row["record_id"]: row for row in proposals}
    denied_ids = {row["record_id"] for row in denied}
    ready_ids = {
        row["record_id"]
        for row in readiness
        if row.get("readiness_label") == "ready_candidate_status_only"
        and row.get("metric_input_authorized_current") == "false"
    }
    overlap_ids = {
        row["record_id"]
        for row in readiness
        if row.get("readiness_label") == "needs_source_overlap_review"
    }
    if len(ready_ids) != 130:
        raise ValueError(f"expected 130 ready rows, found {len(ready_ids)}")
    if overlap_ids != denied_ids:
        raise ValueError("denied rows must exactly match readiness overlap rows")

    overlay_rows: list[dict[str, object]] = []
    resolved_ids: set[str] = set()
    blocked_ids: set[str] = set()
    blocked_fields = (
        "timed|latency_ms|speedup_ratio|timing_eligible|plan_available|plan_artifact_path|"
        "paper_table_fields|reports_results_update|denominator_update|official_metrics"
    )
    for record_id in sorted(denied_ids):
        row = readiness_by_id[record_id]
        proposal = proposal_by_id.get(record_id)
        if proposal is None:
            raise ValueError(f"missing overlap proposal for {record_id}")
        resolved, policy, fields, failure_source = policy_for(row, proposal)
        if resolved:
            resolved_ids.add(record_id)
        else:
            blocked_ids.add(record_id)
        overlay_rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "overlap_sources": row.get("source_ids_used", ""),
                "applied_priority_policy": policy,
                "resolved_by_policy": "true" if resolved else "false",
                "authorize_metric_input_overlay_v1": "true" if resolved else "false",
                "fields_authorized": fields if resolved else "none",
                "fields_still_blocked": blocked_fields,
                "failure_enrichment_source": failure_source,
                "p003_can_override_primary_status": "false",
                "timing_authorized": "false",
                "official_metric_authorized": "false",
                "metrics_computed": "false",
                "paper_result": "false",
                "notes": "audit-only overlap resolution overlay; original parser and v0 authorization overlays are unchanged",
            }
        )

    combined_rows: list[dict[str, object]] = []
    for record_id in sorted(ready_ids):
        row = readiness_by_id[record_id]
        combined_rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "authorization_source": "metric_input_authorization_overlay_v0",
                "authorization_version": "combined_metric_input_authorization_overlay_v1",
                "metric_input_authorized_overlay": "true",
                "authorization_reason": "carried forward from v0 ready_candidate_status_only authorization",
                "timing_authorized": "false",
                "official_metric_authorized": "false",
                "metrics_computed": "false",
                "paper_result": "false",
                "notes": "existing v0 authorized row carried forward without rewriting v0",
            }
        )
    for record_id in sorted(resolved_ids | blocked_ids):
        row = readiness_by_id[record_id]
        authorized = record_id in resolved_ids
        combined_rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "authorization_source": OVERLAY_NAME,
                "authorization_version": "combined_metric_input_authorization_overlay_v1",
                "metric_input_authorized_overlay": "true" if authorized else "false",
                "authorization_reason": "resolved by Option B overlap priority policy"
                if authorized
                else "still blocked after Option B overlap priority policy",
                "timing_authorized": "false",
                "official_metric_authorized": "false",
                "metrics_computed": "false",
                "paper_result": "false",
                "notes": "overlap row included in combined overlay; unresolved denominator rows are summarized elsewhere",
            }
        )

    unresolved_rows = [
        row
        for row in ledger
        if row["record_id"] not in readiness_by_id
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    ]
    if len(unresolved_rows) != 425:
        raise ValueError(f"expected 425 unresolved rows, found {len(unresolved_rows)}")

    checks = [
        ("overlap rows reviewed = 45", len(overlay_rows) == 45, f"overlap rows={len(overlay_rows)}"),
        ("no original parser ledger modified", True, "script reads parser-v1 ledger and writes only audit outputs"),
        ("no v0 overlay modified", True, "script does not write metric_input_authorization_overlay_v0"),
        (
            "P003 cannot override primary status",
            all(row["p003_can_override_primary_status"] == "false" for row in overlay_rows),
            "P003 is failure enrichment only",
        ),
        (
            "timing_authorized=false",
            all(row["timing_authorized"] == "false" for row in overlay_rows + combined_rows),
            "timing remains unauthorized",
        ),
        (
            "official_metrics_computed=false",
            all(row["metrics_computed"] == "false" for row in overlay_rows + combined_rows),
            "no official metrics computed",
        ),
        (
            "paper_result=false",
            all(row["paper_result"] == "false" for row in overlay_rows + combined_rows),
            "no paper results",
        ),
        ("reports/results unchanged", True, "script writes only under audits/overlap_priority_overlay_v1"),
        ("denominator unchanged", True, "denominator files are not written"),
    ]

    return {
        "overlay_rows": overlay_rows,
        "combined_rows": combined_rows,
        "check_rows": [
            {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
            for name, passed, details in checks
        ],
        "overlap_rows_resolved": len(resolved_ids),
        "overlap_rows_still_blocked": len(blocked_ids),
        "combined_authorized_rows": sum(
            1 for row in combined_rows if row["metric_input_authorized_overlay"] == "true"
        ),
        "combined_unauthorized_overlap_rows": sum(
            1 for row in combined_rows if row["metric_input_authorized_overlay"] == "false"
        ),
        "unresolved_rows_remain": len(unresolved_rows),
    }


def write_report(out_dir: Path, summary: dict[str, object]) -> None:
    report = f"""# overlap_priority_overlay_v1 Report

## Purpose And Scope

This audit-only overlay applies the maintainer-approved Option B policy to the 45 candidate-status rows previously blocked by source overlap.

## Option B Policy

- P001 provides generation/readiness evidence.
- P002 provides primary candidate status.
- P003 provides Repair-1 failure enrichment only.
- P003 must not override P002 primary status.

## Rows Resolved

- Overlap rows reviewed: 45.
- Rows resolved by policy: {summary['overlap_rows_resolved']}.
- Rows still blocked: {summary['overlap_rows_still_blocked']}.
- Combined authorized rows in overlay v1: {summary['combined_authorized_rows']}.

## Why P003 Cannot Override P002 Primary Status

P003 was approved only as Repair-1 failure enrichment. The overlay therefore records `p003_can_override_primary_status=false` for every row. P002 remains the primary candidate-status source for Repair-1 rows.

## Timing And Metrics Boundary

Timing fields remain unauthorized. No official metrics, paper results, reports/results updates, denominator changes, or paper-result changes are created by this overlay.

## Next Safe Action

Run the overlap normalization refresh and normalized status-only dry-run v3 from the combined overlay. Keep official metrics and timing adapter work separate.
"""
    (out_dir / "overlap_priority_overlay_v1_report.md").write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    for path in [args.candidate_ledger, args.readiness_review, args.denied_rows, args.overlap_proposal]:
        ensure_allowed_input(path)
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    result = build_outputs(
        read_csv(args.candidate_ledger),
        read_csv(args.readiness_review),
        read_csv(args.denied_rows),
        read_csv(args.overlap_proposal),
    )
    write_csv(args.out_dir / "overlap_priority_overlay_v1.csv", result["overlay_rows"], OVERLAY_COLUMNS)
    write_csv(
        args.out_dir / "combined_metric_input_authorization_overlay_v1.csv",
        result["combined_rows"],
        COMBINED_COLUMNS,
    )
    write_csv(args.out_dir / "overlap_priority_overlay_v1_checks.csv", result["check_rows"], CHECK_COLUMNS)

    summary = {
        "overlay_name": OVERLAY_NAME,
        "overlap_rows_reviewed": 45,
        "overlap_rows_resolved": result["overlap_rows_resolved"],
        "overlap_rows_still_blocked": result["overlap_rows_still_blocked"],
        "combined_authorized_rows": result["combined_authorized_rows"],
        "combined_unauthorized_overlap_rows": result["combined_unauthorized_overlap_rows"],
        "unresolved_rows_remain": result["unresolved_rows_remain"],
        "timing_authorized": False,
        "official_metrics_computed": False,
        "audit_only_overlay_created": True,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    (args.out_dir / "overlap_priority_overlay_v1_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir, summary)

    if any(row["status"] == "FAIL" for row in result["check_rows"]):
        return 1
    print(
        f"wrote {OVERLAY_NAME}: resolved={result['overlap_rows_resolved']} "
        f"still_blocked={result['overlap_rows_still_blocked']} "
        f"combined_authorized={result['combined_authorized_rows']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
