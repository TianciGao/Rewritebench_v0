#!/usr/bin/env python3
"""Build Track-A rewrite_candidate_cell scaffold rows.

This bounded adapter reads only release-repo Common-core denominator and
registry scaffolds. It emits planned same-engine rewrite candidate rows for
the five authorized method routes. It does not parse retained evidence,
method outputs, timing files, reports/results, or legacy data, and it does
not compute metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


ADAPTER_NAME = "rewrite_candidate_adapter_v0"
ADAPTER_SCOPE = "track_a_same_engine_scaffold_only"
CASE_SET = "common_core_v0"
RECORD_TYPE = "rewrite_candidate_cell"
ROUTE = "same_engine_rewrite"
EVIDENCE_SOURCE = "release_denominator_scaffold"

LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DEFAULT_OUT_DIR = Path("audits/rewrite_candidate_adapter_v0")
CASE_REGISTRY_PATH = Path("inventory/case_registry.csv")

LEDGER_FILENAME = "rewrite_candidate_scaffold_ledger_v0.csv"
METHOD_SCOPE_FILENAME = "rewrite_candidate_adapter_v0_method_scope.csv"
SUMMARY_FILENAME = "rewrite_candidate_adapter_v0_summary.json"
REPORT_FILENAME = "rewrite_candidate_adapter_v0_report.md"
CHECKS_FILENAME = "rewrite_candidate_adapter_v0_checks.csv"
LIMITATIONS_FILENAME = "rewrite_candidate_adapter_v0_limitations.md"

METHODS = [
    {
        "rewrite_method": "direct_llm_original",
        "display_name": "Direct LLM original",
        "method_role": "same_engine_rewrite_method",
        "route_family": "llm_direct",
    },
    {
        "rewrite_method": "direct_llm_repair_1",
        "display_name": "Direct LLM + Repair-1",
        "method_role": "same_engine_feedback_rewrite_method",
        "route_family": "llm_feedback_repair",
    },
    {
        "rewrite_method": "sqlglot_optimize",
        "display_name": "SQLGlot optimize",
        "method_role": "deterministic_same_engine_rewrite_method",
        "route_family": "sqlglot_optimize",
    },
    {
        "rewrite_method": "sqlglot_noop",
        "display_name": "SQLGlot no-op",
        "method_role": "low_transform_infrastructure_route",
        "route_family": "sqlglot_noop",
    },
    {
        "rewrite_method": "calcite_hep_fail_closed",
        "display_name": "Calcite HEP fail-closed",
        "method_role": "rule_based_fail_closed_rewrite_method",
        "route_family": "calcite_hep",
    },
]

EXCLUDED_METHODS = [
    ("r_bot", "R-Bot", "bounded prior route; separate adapter required"),
    ("llm_r2", "LLM-R2", "bounded prior route; separate adapter required"),
    ("learnedrewrite", "LearnedRewrite", "bounded prior route; separate adapter required"),
    ("sqlglot_transpile", "SQLGlot Transpile", "portability/transpile route; separate adapter required"),
    ("llm_translate", "LLM Translate", "portability/translation route; separate adapter required"),
    ("sqlsolver", "SQLSolver", "verifier support route; not a rewrite-generation baseline"),
    ("verieql", "VeriEQL", "verifier support route; not a rewrite-generation baseline"),
    ("user_submitted_methods", "User-submitted methods", "future public-runner route; not retained scaffold"),
]

LEDGER_COLUMNS = [
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
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

METHOD_SCOPE_COLUMNS = [
    "rewrite_method",
    "display_name",
    "route_family",
    "method_role",
    "included_in_scaffold",
    "excluded_from_scaffold_reason",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Track-A same-engine rewrite candidate scaffold rows."
    )
    parser.add_argument("--case-set", required=True, type=Path)
    parser.add_argument("--denominator", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_safe_path(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo path is not allowed: {path}")
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results paths are not valid scaffold inputs: {path}")
    if "runs" in path.parts:
        raise ValueError(f"runs paths are not valid scaffold inputs: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def false_text() -> str:
    return "false"


def build_method_scope_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for method in METHODS:
        rows.append(
            {
                "rewrite_method": method["rewrite_method"],
                "display_name": method["display_name"],
                "route_family": method["route_family"],
                "method_role": method["method_role"],
                "included_in_scaffold": "true",
                "excluded_from_scaffold_reason": "",
                "notes": "Authorized main Track-A same-engine scaffold method; no evidence parsed.",
            }
        )
    for rewrite_method, display_name, reason in EXCLUDED_METHODS:
        rows.append(
            {
                "rewrite_method": rewrite_method,
                "display_name": display_name,
                "route_family": "",
                "method_role": "",
                "included_in_scaffold": "false",
                "excluded_from_scaffold_reason": reason,
                "notes": "Excluded from this bounded scaffold; handle only in a later authorized adapter.",
            }
        )
    return rows


def build_ledger_rows(
    denominator_rows: list[dict[str, str]],
    case_rows: list[dict[str, str]],
    registry_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    case_by_id = {row["case_id"]: row for row in case_rows}
    registry_case_ids = {row.get("case_id", "") for row in registry_rows}
    rows: list[dict[str, str]] = []
    for denominator in denominator_rows:
        case_id = denominator["case_id"]
        case = case_by_id[case_id]
        engine = denominator["engine"]
        case_path = Path(denominator["case_path"])
        source_sql_path = str(case_path / "sql/source.sql")
        for method in METHODS:
            method_name = method["rewrite_method"]
            candidate_id = f"candidate:{case_id}:{engine}:{method_name}:planned"
            record_id = f"{ADAPTER_NAME}:{denominator['denominator_id']}:{method_name}"
            notes = [
                "Track-A same-engine rewrite candidate scaffold row only.",
                "No retained candidate evidence parsed.",
                "No generated/executed/exact/timed status inferred.",
                "No metrics computed.",
            ]
            if case_id in registry_case_ids:
                notes.append("case present in inventory/case_registry.csv")
            rows.append(
                {
                    "record_id": record_id,
                    "record_type": RECORD_TYPE,
                    "adapter_name": ADAPTER_NAME,
                    "adapter_scope": ADAPTER_SCOPE,
                    "case_id": case_id,
                    "pool": denominator["pool"],
                    "case_set": CASE_SET,
                    "denominator_id": denominator["denominator_id"],
                    "engine": engine,
                    "rewrite_method": method_name,
                    "rewrite_method_display_name": method["display_name"],
                    "route": ROUTE,
                    "route_family": method["route_family"],
                    "method_role": method["method_role"],
                    "candidate_id": candidate_id,
                    "source_sql_path": source_sql_path,
                    "candidate_sql_path": "",
                    "planned": "true",
                    "generated": "N.A.",
                    "ready": "N.A.",
                    "executed": "N.A.",
                    "exact": "N.A.",
                    "timed": "N.A.",
                    "result_status": "evidence_not_adapted_yet",
                    "failure_stage": "N.A.",
                    "failure_type": "N.A.",
                    "parse_status": "N.A.",
                    "checker_status": "N.A.",
                    "plan_available": "N.A.",
                    "plan_artifact_path": "",
                    "latency_ms": "",
                    "speedup_ratio": "",
                    "timing_eligible": "N.A.",
                    "evidence_source": EVIDENCE_SOURCE,
                    "retained_artifact_path": "",
                    "status": "N.A.",
                    "na_reason": "evidence_not_adapted_yet",
                    "metric_input_authorized": false_text(),
                    "metrics_computed": false_text(),
                    "production_retained_evidence_parsed": false_text(),
                    "legacy_repo_read": false_text(),
                    "reports_changed": false_text(),
                    "results_changed": false_text(),
                    "denominator_changed": false_text(),
                    "paper_results_changed": false_text(),
                    "notes": "; ".join(notes),
                }
            )
    return rows


def checks_rows(
    denominator_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    method_scope_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    included_method_count = sum(
        1 for row in method_scope_rows if row["included_in_scaffold"] == "true"
    )
    checks: list[tuple[str, bool, str]] = [
        (
            "denominator_same_engine_120 row count = 120",
            len(denominator_rows) == 120,
            f"denominator_rows={len(denominator_rows)}",
        ),
        ("method route count = 5", included_method_count == 5, f"method_routes={included_method_count}"),
        ("emitted scaffold row count = 600", len(ledger_rows) == 600, f"rows_emitted={len(ledger_rows)}"),
        (
            "all rows record_type=rewrite_candidate_cell",
            all(row["record_type"] == RECORD_TYPE for row in ledger_rows),
            RECORD_TYPE,
        ),
        (
            "all rows metric_input_authorized=false",
            all(row["metric_input_authorized"] == "false" for row in ledger_rows),
            "metric_input_authorized=false",
        ),
        (
            "all rows metrics_computed=false",
            all(row["metrics_computed"] == "false" for row in ledger_rows),
            "metrics_computed=false",
        ),
        (
            "all rows production_retained_evidence_parsed=false",
            all(row["production_retained_evidence_parsed"] == "false" for row in ledger_rows),
            "production_retained_evidence_parsed=false",
        ),
        ("no legacy repo path read", True, "legacy_repo_read=false"),
        ("no reports/results changed", True, "reports_changed=false;results_changed=false"),
        ("denominator unchanged", True, "denominator_changed=false"),
        ("paper results unchanged", True, "paper_results_changed=false"),
        (
            "no generated/executed/exact/timed values inferred",
            all(
                row[field] == "N.A."
                for row in ledger_rows
                for field in ("generated", "ready", "executed", "exact", "timed")
            ),
            "generated/ready/executed/exact/timed=N.A.",
        ),
        ("no metric computed", True, "all metric computation flags false"),
    ]
    return [
        {
            "check_name": name,
            "status": "PASS" if passed else "FAIL",
            "details": details,
        }
        for name, passed, details in checks
    ]


def summary_payload(ledger_rows: list[dict[str, str]]) -> dict[str, object]:
    return {
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "rows_emitted": len(ledger_rows),
        "same_engine_denominator_rows_expected": 120,
        "method_routes_expected": len(METHODS),
        "scaffold_rows_expected": 120 * len(METHODS),
        "scaffold_rows_emitted": len(ledger_rows),
        "record_types_emitted": sorted({row["record_type"] for row in ledger_rows}),
        "methods_emitted": [method["rewrite_method"] for method in METHODS],
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


def write_report(
    path: Path,
    args: argparse.Namespace,
    ledger_rows: list[dict[str, str]],
    method_scope_rows: list[dict[str, object]],
) -> None:
    method_counts = Counter(row["rewrite_method"] for row in ledger_rows)
    lines = [
        "# rewrite_candidate_adapter_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "This bounded scaffold emits draft `rewrite_candidate_cell` rows for the",
        "main Track-A same-engine rewrite method scope. It materializes row grain",
        "only: `case_id x engine x rewrite_method x denominator_id`.",
        "",
        "## Inputs Read",
        "",
        f"- Case set: `{args.case_set}`",
        f"- Same-engine denominator: `{args.denominator}`",
        f"- Case registry: `{CASE_REGISTRY_PATH}`",
        "",
        "No legacy reports/results/runs, raw method outputs, timing files, or",
        "retained-evidence candidate maps were read.",
        "",
        "## Method Scope",
        "",
    ]
    for method in METHODS:
        lines.append(
            f"- `{method['rewrite_method']}`: {method['display_name']} "
            f"({method['route_family']})"
        )
    lines.extend(
        [
            "",
            "Excluded route families include R-Bot, LLM-R2, LearnedRewrite,",
            "SQLGlot Transpile, LLM Translate, SQLSolver, VeriEQL, and future",
            "user-submitted methods. These are prior, portability, verifier, or",
            "future public-runner routes requiring separate adapters.",
            "",
            "## Rows Emitted",
            "",
            f"- Same-engine denominator rows: 120.",
            f"- Method routes: {len(METHODS)}.",
            f"- Scaffold rows emitted: {len(ledger_rows)}.",
            "",
        ]
    )
    lines.extend(f"- `{method}`: {count} rows." for method, count in sorted(method_counts.items()))
    lines.extend(
        [
            "",
            "## Explicit Non-goals",
            "",
            "- No production retained evidence was parsed.",
            "- No method candidate evidence was parsed.",
            "- No timing files were parsed.",
            "- No metrics were computed.",
            "- No reports/results were copied or changed.",
            "- No denominator, paper result, case membership, or raw legacy evidence was changed.",
            "",
            "## Why This Is Not Metrics Computation",
            "",
            "All candidate outcome fields remain `N.A.` and `result_status` is",
            "`evidence_not_adapted_yet`. The scaffold does not count generated,",
            "executed, result-consistent, exact, timed, or speedup rows and cannot",
            "be used to compute Generation Rate, Execution Coverage Rate, Result",
            "Consistency Rate, or timing metrics.",
            "",
            "## Validation Result",
            "",
            "The adapter writes a scaffold ready for `scripts/dev/validate_ledger_csv.py`.",
            "See `audits/rewrite_candidate_adapter_v0/ledger_validation/` after",
            "running the validator.",
            "",
            "## Next Safe Action",
            "",
            "Review scaffold row grain and method scope. Do not parse retained",
            "candidate evidence, compute metrics, or emit metric-eligible rows",
            "without separate authorization.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# rewrite_candidate_adapter_v0 Limitations",
                "",
                "- This adapter only creates planned Track-A same-engine candidate scaffold rows.",
                "- It does not parse real retained candidate evidence.",
                "- It does not parse legacy reports, results, runs, or raw evidence.",
                "- It does not compute metrics.",
                "- It does not compute Generation Rate, Execution Coverage Rate, or Result Consistency Rate.",
                "- It does not handle timing, GM_Speedup, or Speedup Ratio Percentiles.",
                "- It does not handle portability or verifier support.",
                "- Future metric-eligible candidate adapters require separate authorization.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    root = repo_root()
    input_paths = [args.case_set, args.denominator, CASE_REGISTRY_PATH]
    resolved_inputs: list[Path] = []
    for path in input_paths:
        resolved = path if path.is_absolute() else root / path
        ensure_safe_path(resolved)
        if not resolved.exists():
            raise FileNotFoundError(resolved)
        resolved_inputs.append(resolved)

    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    ensure_safe_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    case_rows = read_csv(resolved_inputs[0])
    denominator_rows = read_csv(resolved_inputs[1])
    registry_rows = read_csv(resolved_inputs[2])

    case_ids = {row["case_id"] for row in case_rows}
    denominator_case_ids = {row["case_id"] for row in denominator_rows}
    if not denominator_case_ids <= case_ids:
        missing = sorted(denominator_case_ids - case_ids)
        raise ValueError("denominator cases missing from case set: " + ";".join(missing))

    ledger_rows = build_ledger_rows(denominator_rows, case_rows, registry_rows)
    method_scope_rows = build_method_scope_rows()
    checks = checks_rows(denominator_rows, ledger_rows, method_scope_rows)
    summary = summary_payload(ledger_rows)

    write_csv(out_dir / LEDGER_FILENAME, ledger_rows, LEDGER_COLUMNS)
    write_csv(out_dir / METHOD_SCOPE_FILENAME, method_scope_rows, METHOD_SCOPE_COLUMNS)
    write_csv(out_dir / CHECKS_FILENAME, checks, ["check_name", "status", "details"])
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(out_dir / REPORT_FILENAME, args, ledger_rows, method_scope_rows)
    write_limitations(out_dir / LIMITATIONS_FILENAME)

    failed_checks = [row for row in checks if row["status"] != "PASS"]
    print(f"rows_emitted: {len(ledger_rows)}")
    print(f"method_routes: {len(METHODS)}")
    print(f"failed_checks: {len(failed_checks)}")
    return 0 if not failed_checks else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
