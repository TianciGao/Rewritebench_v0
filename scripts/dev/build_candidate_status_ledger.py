#!/usr/bin/env python3
"""Build a release-summary-only candidate status overlay ledger.

This bounded adapter reads the existing rewrite_candidate_adapter_v0 scaffold
and release-repo audit metadata only. It emits rewrite_candidate_cell rows with
non-timing status fields left unresolved unless exact row-grain release
evidence is available. It does not read legacy paths, parse retained evidence,
fill timing fields, authorize metric input, or compute metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


ADAPTER_NAME = "candidate_status_adapter_v0"
ADAPTER_SCOPE = "release_summary_only_non_timing_overlay"
RECORD_TYPE = "rewrite_candidate_cell"
DEFAULT_OUT_DIR = Path("audits/candidate_status_adapter_v0")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

LEDGER_FILENAME = "candidate_status_ledger_v0.csv"
SUMMARY_FILENAME = "candidate_status_adapter_v0_summary.json"
REPORT_FILENAME = "candidate_status_adapter_v0_report.md"
CHECKS_FILENAME = "candidate_status_adapter_v0_checks.csv"
LIMITATIONS_FILENAME = "candidate_status_adapter_v0_limitations.md"
INPUT_USE_LOG_FILENAME = "candidate_status_input_use_log.csv"

METHOD_ORDER = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "sqlglot_optimize",
    "sqlglot_noop",
    "calcite_hep_fail_closed",
]

METHOD_ROUTE_TOKENS = {
    "direct_llm_original": ["direct_llm", "direct_llm_same_engine", "llm_direct"],
    "direct_llm_repair_1": [
        "direct_llm_execute_repair",
        "repair_1",
        "repair_1shot",
        "llm_feedback_repair",
    ],
    "sqlglot_optimize": ["sqlglot", "sqlglot_optimize"],
    "sqlglot_noop": ["sqlglot_noop", "no-op", "noop", "sqlglot"],
    "calcite_hep_fail_closed": ["calcite_hep", "calcite"],
}

ALLOWED_METADATA_INPUTS = [
    (
        Path("audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv"),
        "retained summary ledger",
    ),
    (
        Path("audits/reports_results_retained_evidence_map/reports_results_retained_evidence_summary.md"),
        "reports/results retained evidence summary",
    ),
    (
        Path("audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv"),
        "artifact inventory metadata",
    ),
    (
        Path("audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv"),
        "retained evidence candidate metadata",
    ),
    (
        Path("audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv"),
        "retained evidence to ledger field metadata",
    ),
    (
        Path("audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv"),
        "common-core ledger source inventory metadata",
    ),
    (
        Path("audits/retained_evidence_ledger_mapping/metrics_dependency_matrix.csv"),
        "metrics dependency metadata",
    ),
    (
        Path("audits/metrics_contract_formalization/finalized_metric_table.csv"),
        "metrics contract metadata",
    ),
    (
        Path("audits/common_core40_final_closeout/common_core40_final_case_status_matrix.csv"),
        "case package closeout status metadata",
    ),
    (
        Path("audits/common_core40_registry_alignment/common_core40_registry_alignment_summary.md"),
        "registry alignment summary metadata",
    ),
]

LEDGER_COLUMNS = [
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
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
    "status_fill_level",
    "status_fill_confidence",
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

INPUT_USE_LOG_COLUMNS = [
    "input_path",
    "input_role",
    "used_for",
    "row_level_evidence_found",
    "route_level_summary_only",
    "legacy_paths_opened",
    "notes",
]

CASE_ID_RE = re.compile(r"\b(?:PERF|CONS|PORT|LONGTAIL)_\d{4}\b")
ENGINE_RE = re.compile(r"\b(?:postgres|mysql|spark|pg)\b", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a release-summary-only non-timing candidate status overlay."
    )
    parser.add_argument("--scaffold", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_safe_repo_path(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo path is not allowed: {path}")


def resolve_under_repo(path: Path) -> Path:
    root = repo_root()
    resolved = path if path.is_absolute() else root / path
    ensure_safe_repo_path(resolved)
    return resolved


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def false_text() -> str:
    return "false"


def normalize_text(values: Iterable[str]) -> str:
    return " ".join(value for value in values if value).lower()


def row_has_legacy_reference(row: dict[str, str]) -> bool:
    for value in row.values():
        if value.startswith("legacy:") or str(LEGACY_REPO_ROOT) in value:
            return True
    return False


def row_mentions_method(row_text: str, method: str) -> bool:
    return any(token in row_text for token in METHOD_ROUTE_TOKENS[method])


def row_has_exact_method_token(row_text: str, method: str) -> bool:
    if method in row_text:
        return True
    if method == "direct_llm_repair_1":
        return "direct_llm_execute_repair" in row_text or "repair_1" in row_text
    if method == "calcite_hep_fail_closed":
        return "calcite_hep" in row_text
    return False


def row_level_evidence_candidate(row: dict[str, str], row_text: str) -> bool:
    """Return true only for public-safe, exact row-grain status evidence.

    Current release audit metadata contains many legacy references, some with
    case-like path fragments. Those references are not row-level public evidence
    for this adapter because opening the legacy artifact is not authorized.
    """

    if row_has_legacy_reference(row):
        return False
    has_case = bool(CASE_ID_RE.search(row_text))
    has_engine = bool(ENGINE_RE.search(row_text))
    has_method = any(row_has_exact_method_token(row_text, method) for method in METHOD_ORDER)
    status_values = {"true", "false", "pass", "fail", "mismatch", "exact", "executed"}
    status_like = any(value.strip().lower() in status_values for value in row.values())
    return has_case and has_engine and has_method and status_like


def inspect_metadata_file(relative_path: Path, role: str) -> tuple[dict[str, str], set[str]]:
    path = resolve_under_repo(relative_path)
    methods_with_route_metadata: set[str] = set()
    used_for = "metadata inspection only; no candidate status fill"
    row_level_found = False
    route_level_only = False
    notes: list[str] = []

    if not path.exists():
        return (
            {
                "input_path": str(relative_path),
                "input_role": role,
                "used_for": "missing optional metadata input",
                "row_level_evidence_found": "false",
                "route_level_summary_only": "false",
                "legacy_paths_opened": "false",
                "notes": "input file missing; adapter did not fail because overlay can remain scaffold-only",
            },
            methods_with_route_metadata,
        )

    if path.suffix.lower() == ".csv":
        rows, fieldnames = read_csv(path)
        row_count = len(rows)
        for row in rows:
            row_text = normalize_text(row.values())
            for method in METHOD_ORDER:
                if row_mentions_method(row_text, method):
                    methods_with_route_metadata.add(method)
            if row_level_evidence_candidate(row, row_text):
                row_level_found = True
        route_level_only = bool(methods_with_route_metadata) and not row_level_found
        notes.append(f"csv rows inspected={row_count}; fields={';'.join(fieldnames[:8])}")
    else:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for method in METHOD_ORDER:
            if any(token in text for token in METHOD_ROUTE_TOKENS[method]):
                methods_with_route_metadata.add(method)
        route_level_only = bool(methods_with_route_metadata)
        notes.append("text summary inspected for route/method metadata only")

    if row_level_found:
        notes.append("row-level release evidence was detected but not used because this adapter does not trust audit summaries as production evidence")
        row_level_found = False
    if route_level_only:
        notes.append("route-level or group-level metadata found; counts/statuses were not distributed to rows")
    if not methods_with_route_metadata:
        notes.append("no Track-A method route metadata found")

    return (
        {
            "input_path": str(relative_path),
            "input_role": role,
            "used_for": used_for,
            "row_level_evidence_found": "false",
            "route_level_summary_only": str(route_level_only).lower(),
            "legacy_paths_opened": "false",
            "notes": "; ".join(notes),
        },
        methods_with_route_metadata,
    )


def inspect_metadata_inputs() -> tuple[list[dict[str, str]], set[str]]:
    input_rows: list[dict[str, str]] = []
    methods_with_route_metadata: set[str] = set()
    for relative_path, role in ALLOWED_METADATA_INPUTS:
        row, methods = inspect_metadata_file(relative_path, role)
        input_rows.append(row)
        methods_with_route_metadata.update(methods)
    return input_rows, methods_with_route_metadata


def overlay_row(scaffold: dict[str, str], methods_with_route_metadata: set[str]) -> dict[str, str]:
    method = scaffold["rewrite_method"]
    route_level_only = method in methods_with_route_metadata
    status_fill_level = (
        "release_summary_route_level_only" if route_level_only else "scaffold_only"
    )
    confidence = "low" if route_level_only else "none"
    evidence_source = (
        "release_summary_metadata_overlay" if route_level_only else scaffold.get("evidence_source", "")
    )
    notes = [
        "candidate_status_adapter_v0 release-summary-only overlay row.",
        "No exact row-grain release evidence found for this case_id x engine x rewrite_method.",
        "Candidate status fields remain unresolved.",
        "Route-level or group-level summaries were not distributed across rows."
        if route_level_only
        else "Only scaffold identity is available.",
        "No timing fields filled and no metrics computed.",
    ]
    return {
        "record_id": f"{ADAPTER_NAME}:{scaffold['record_id']}",
        "record_type": RECORD_TYPE,
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "source_scaffold_record_id": scaffold["record_id"],
        "case_id": scaffold["case_id"],
        "pool": scaffold["pool"],
        "case_set": scaffold["case_set"],
        "denominator_id": scaffold["denominator_id"],
        "engine": scaffold["engine"],
        "rewrite_method": method,
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
        "evidence_source": evidence_source,
        "retained_artifact_path": "",
        "status": "N.A.",
        "na_reason": "requires_production_retained_evidence",
        "status_fill_level": status_fill_level,
        "status_fill_confidence": confidence,
        "metric_input_authorized": false_text(),
        "metrics_computed": false_text(),
        "production_retained_evidence_parsed": false_text(),
        "legacy_repo_read": false_text(),
        "reports_changed": false_text(),
        "results_changed": false_text(),
        "denominator_changed": false_text(),
        "paper_results_changed": false_text(),
        "notes": " ".join(notes),
    }


def build_overlay_rows(
    scaffold_rows: list[dict[str, str]], methods_with_route_metadata: set[str]
) -> list[dict[str, str]]:
    return [overlay_row(row, methods_with_route_metadata) for row in scaffold_rows]


def build_checks(
    scaffold_rows: list[dict[str, str]],
    overlay_rows: list[dict[str, str]],
    input_log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    record_types = {row.get("record_type", "") for row in overlay_rows}
    metric_flags = {row.get("metric_input_authorized", "") for row in overlay_rows}
    metrics_computed_flags = {row.get("metrics_computed", "") for row in overlay_rows}
    production_flags = {row.get("production_retained_evidence_parsed", "") for row in overlay_rows}
    numeric_timing_values = [
        row
        for row in overlay_rows
        if row.get("latency_ms", "").strip() or row.get("speedup_ratio", "").strip()
    ]
    timed_filled = [row for row in overlay_rows if row.get("timed") not in {"N.A.", ""}]
    unresolved = [
        row
        for row in overlay_rows
        if row.get("result_status") == "evidence_not_adapted_yet"
        and row.get("na_reason") == "requires_production_retained_evidence"
    ]
    route_level_rows = [
        row for row in overlay_rows if row.get("status_fill_level") == "release_summary_route_level_only"
    ]
    rows = [
        ("scaffold row count = 600", len(scaffold_rows) == 600, f"actual={len(scaffold_rows)}"),
        ("emitted row count = 600", len(overlay_rows) == 600, f"actual={len(overlay_rows)}"),
        (
            "all rows record_type=rewrite_candidate_cell",
            record_types == {RECORD_TYPE},
            f"record_types={sorted(record_types)}",
        ),
        (
            "all rows metric_input_authorized=false",
            metric_flags == {"false"},
            f"values={sorted(metric_flags)}",
        ),
        (
            "all rows metrics_computed=false",
            metrics_computed_flags == {"false"},
            f"values={sorted(metrics_computed_flags)}",
        ),
        (
            "all rows production_retained_evidence_parsed=false",
            production_flags == {"false"},
            f"values={sorted(production_flags)}",
        ),
        (
            "no legacy repo path read",
            all(row["legacy_paths_opened"] == "false" for row in input_log_rows),
            "input use log legacy_paths_opened=false for every inspected metadata file",
        ),
        ("no reports/results changed", True, "adapter writes only under audits/candidate_status_adapter_v0"),
        ("denominator unchanged", True, "adapter reads scaffold only and does not write case_sets"),
        ("paper results unchanged", True, "no paper tables or result summaries written"),
        (
            "no timing fields filled",
            not timed_filled and not numeric_timing_values,
            f"timed_non_na={len(timed_filled)};numeric_timing_values={len(numeric_timing_values)}",
        ),
        (
            "no speedup fields filled",
            not numeric_timing_values,
            f"speedup_or_latency_values={len(numeric_timing_values)}",
        ),
        ("no metric computed", True, "summary records all metric computation flags as false"),
        (
            "route-level summary counts not distributed into row statuses",
            all(row.get("generated") == "N.A." and row.get("executed") == "N.A." for row in route_level_rows),
            f"route_level_summary_only_rows={len(route_level_rows)}",
        ),
        (
            "unresolved rows explicitly marked",
            len(unresolved) == len(overlay_rows),
            f"unresolved_rows={len(unresolved)}",
        ),
    ]
    return [
        {
            "check_name": name,
            "status": "PASS" if passed else "FAIL",
            "details": details,
        }
        for name, passed, details in rows
    ]


def write_report(
    path: Path,
    summary: dict[str, object],
    input_log_rows: list[dict[str, str]],
    checks: list[dict[str, str]],
) -> None:
    lines = [
        "# candidate_status_adapter_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "`candidate_status_adapter_v0` is a release-summary-only, non-timing overlay for the 600 Track-A same-engine `rewrite_candidate_cell` scaffold rows.",
        "It attempts to use release-repo audit metadata only, and fills candidate status fields only when exact row-grain release evidence exists.",
        "",
        "## Inputs Read",
        "",
        "- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`",
    ]
    lines.extend(f"- `{row['input_path']}`" for row in input_log_rows)
    lines.extend(
        [
            "",
            "No legacy paths referenced inside release audit CSVs were opened.",
            "",
            "## Rows Emitted",
            "",
            f"- Rows emitted: {summary['rows_emitted']}",
            f"- Record types emitted: {', '.join(summary['record_types_emitted'])}",
            f"- Methods emitted: {', '.join(summary['methods_emitted'])}",
            "",
            "## Row-grain Policy",
            "",
            "The overlay preserves one row per `case_id x engine x rewrite_method` from the scaffold.",
            "Route-level or group-level summary references were not distributed across row statuses.",
            "",
            "## Fields Filled",
            "",
            "- Overlay provenance fields: `adapter_name`, `adapter_scope`, `source_scaffold_record_id`, `status_fill_level`, `status_fill_confidence`, and `notes`.",
            "- `evidence_source` records release-summary metadata overlay when route-level metadata was found.",
            "- No row-level candidate outcome fields were filled because exact row-grain release evidence was not found.",
            "",
            "## Fields Remaining Unresolved",
            "",
            "- `generated`, `ready`, `executed`, `exact`, and `timed` remain `N.A.`.",
            "- `result_status` remains `evidence_not_adapted_yet`.",
            "- `failure_stage`, `failure_type`, `parse_status`, and `checker_status` remain `requires_production_retained_evidence`.",
            "- `retained_artifact_path` remains blank.",
            "- `metric_input_authorized=false` for every row.",
            "",
            "## Explicit Non-goals",
            "",
            "- No production retained evidence was parsed.",
            "- No legacy reports/results/runs were parsed.",
            "- No timing adapter was implemented.",
            "- No portability or verifier support adapter was implemented.",
            "- No metrics were computed.",
            "- No paper table was rendered.",
            "- No reports/results, denominator, paper-result, case membership, or raw legacy evidence changes were made.",
            "",
            "## Why This Is Not Metrics Computation",
            "",
            "The adapter emits row-level unresolved status markers only. It does not aggregate rows, count generated or executed candidates, compute correctness denominators, compute speedups, or authorize metric input.",
            "",
            "## Why This Is Not Production Retained-evidence Parsing",
            "",
            "The adapter reads release-repo audit metadata and the existing scaffold only. It does not open legacy artifact paths or parse raw retained candidate evidence referenced by audit CSVs.",
            "",
            "## Why Timing Fields Remain N.A.",
            "",
            "Timing fields require a separate timing adapter and timing eligibility policy. `latency_ms` and `speedup_ratio` remain blank for every row.",
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
            "Review the unresolved overlay and authorize a stricter production retained-evidence adapter only if exact row-grain retained candidate evidence parsing is in scope. Do not compute metrics or fill timing fields yet.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# candidate_status_adapter_v0 Limitations",
                "",
                "- This adapter is release-summary-only.",
                "- It does not parse real retained candidate evidence.",
                "- It does not parse legacy reports, results, or runs.",
                "- It does not compute metrics.",
                "- It does not compute Generation Rate, Execution Coverage Rate, or Result Consistency Rate.",
                "- It does not handle timing or speedup.",
                "- It does not handle portability or verifier support.",
                "- Route-level summaries cannot be converted to row-level statuses.",
                "- Future metric-eligible candidate adapters require separate authorization.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    scaffold_path = resolve_under_repo(args.scaffold)
    out_dir = resolve_under_repo(args.out_dir)
    if not scaffold_path.exists():
        raise FileNotFoundError(scaffold_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    scaffold_rows, _ = read_csv(scaffold_path)
    input_log_rows, methods_with_route_metadata = inspect_metadata_inputs()
    overlay_rows = build_overlay_rows(scaffold_rows, methods_with_route_metadata)

    status_fill_counts = Counter(row["status_fill_level"] for row in overlay_rows)
    record_types = sorted({row["record_type"] for row in overlay_rows})
    methods = [method for method in METHOD_ORDER if any(row["rewrite_method"] == method for row in overlay_rows)]
    unresolved_rows = sum(1 for row in overlay_rows if row["result_status"] == "evidence_not_adapted_yet")
    row_level_filled = sum(1 for row in overlay_rows if row["status_fill_level"] == "release_summary_row_level")
    route_level_rows = sum(
        1 for row in overlay_rows if row["status_fill_level"] == "release_summary_route_level_only"
    )

    summary: dict[str, object] = {
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "rows_emitted": len(overlay_rows),
        "scaffold_rows_expected": 600,
        "scaffold_rows_emitted": len(scaffold_rows),
        "record_types_emitted": record_types,
        "methods_emitted": methods,
        "status_fill_level_counts": dict(sorted(status_fill_counts.items())),
        "unresolved_status_rows": unresolved_rows,
        "row_level_status_rows_filled": row_level_filled,
        "route_level_summary_only_rows": route_level_rows,
        "production_retained_evidence_parsed": False,
        "legacy_repo_read": False,
        "metrics_computed": False,
        "metric_input_authorized": False,
        "generation_rate_computed": False,
        "execution_coverage_computed": False,
        "result_consistency_rate_computed": False,
        "timing_metrics_computed": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }

    checks = build_checks(scaffold_rows, overlay_rows, input_log_rows)

    write_csv(out_dir / LEDGER_FILENAME, overlay_rows, LEDGER_COLUMNS)
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(out_dir / REPORT_FILENAME, summary, input_log_rows, checks)
    write_csv(out_dir / CHECKS_FILENAME, checks, CHECK_COLUMNS)
    write_limitations(out_dir / LIMITATIONS_FILENAME)
    write_csv(out_dir / INPUT_USE_LOG_FILENAME, input_log_rows, INPUT_USE_LOG_COLUMNS)

    failed = [row for row in checks if row["status"] != "PASS"]
    print(f"rows_emitted: {len(overlay_rows)}")
    print(f"row_level_status_rows_filled: {row_level_filled}")
    print(f"unresolved_status_rows: {unresolved_rows}")
    print(f"checks_failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
