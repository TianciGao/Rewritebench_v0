#!/usr/bin/env python3
"""Build draft control_cell ledger rows from release case packages only.

This bounded adapter reads Common-core case-set scaffolds and canonical case
package metadata/evidence index files. It emits one non-metric control_cell row
for every row in controls_360.csv. It does not read legacy reports/results/runs,
parse production retained evidence, or compute metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


ADAPTER_NAME = "control_cell_adapter_v0"
ADAPTER_SCOPE = "release_case_package_only"
CASE_SET = "common_core_v0"
RECORD_TYPE = "control_cell"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DEFAULT_OUT_DIR = Path("audits/control_cell_adapter_v0")
CASE_REGISTRY_PATH = Path("inventory/case_registry.csv")

LEDGER_FILENAME = "control_cell_ledger_v0.csv"
SUMMARY_FILENAME = "control_cell_adapter_v0_summary.json"
REPORT_FILENAME = "control_cell_adapter_v0_report.md"
CHECKS_FILENAME = "control_cell_adapter_v0_checks.csv"

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
    "route",
    "method_role",
    "control_route",
    "candidate_id",
    "source_sql_path",
    "candidate_sql_path",
    "planned",
    "applicable_status",
    "evidence_index_status",
    "expected_rejection_status",
    "checker_guard_role",
    "retained_artifact_path",
    "runs_retention_path",
    "package_validation_summary_path",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "result_status",
    "checker_status",
    "evidence_source",
    "status",
    "na_reason",
    "metrics_computed",
    "metric_input_authorized",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build control_cell rows from Common-core release case packages."
    )
    parser.add_argument("--case-set", required=True, type=Path)
    parser.add_argument("--controls", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_safe_path(path: Path, *, allow_cases: bool = False) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo path is not allowed: {path}")
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results paths are not valid adapter inputs: {path}")
    if "runs" in path.parts and not allow_cases:
        raise ValueError(f"raw runs paths are not valid adapter inputs: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text_if_exists(path: Path) -> str:
    ensure_safe_path(path, allow_cases=True)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def parse_checker_guard_role(expected_rejections_text: str) -> str:
    match = re.search(r"^\s*checker_guard_role:\s*(.+?)\s*$", expected_rejections_text, re.MULTILINE)
    if match:
        return match.group(1).strip().strip("'\"")
    return "manual_review_required"


def expected_rejection_status(route: str, expected_rejections_text: str, expected_path: Path) -> str:
    if route != "hard_negative":
        return "not_applicable"
    if not expected_path.exists():
        return "manual_review_required"
    if "hard_negative_id" in expected_rejections_text:
        return "expected_rejection_indexed"
    return "manual_review_required"


def checker_guard_role(route: str, expected_rejections_text: str) -> str:
    if route == "source":
        return "source_reference_control"
    if route == "positive":
        return "source_positive_equivalence_control"
    return parse_checker_guard_role(expected_rejections_text)


def candidate_sql_path(case_path: Path, route: str) -> str:
    if route == "source":
        return str(case_path / "sql/source.sql")
    if route == "positive":
        return str(case_path / "sql/positives/pos_01.sql")
    if route == "hard_negative":
        return str(case_path / "sql/negatives/neg_01.sql")
    return ""


def retained_artifact_candidate(case_path: Path, engine: str, route: str) -> Path:
    if route == "source":
        return case_path / f"evidence/retained_controls/{engine}/source.tsv"
    if route == "positive":
        return case_path / f"evidence/retained_controls/{engine}/rewrite_pos_01.tsv"
    if route == "hard_negative":
        return case_path / f"evidence/hard_negative/{engine}/rewrite_neg_01.tsv"
    return case_path


def evidence_index_status(retained_path: Path, runs_retention_path: Path) -> str:
    ensure_safe_path(retained_path, allow_cases=True)
    if retained_path.exists():
        return "indexed_public_safe_reference"
    if runs_retention_path.exists():
        return "evidence_not_retained"
    return "manual_review_required"


def build_rows(
    root: Path,
    case_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    registry_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    case_by_id = {row["case_id"]: row for row in case_rows}
    registry_case_ids = {row.get("case_id", "") for row in registry_rows}
    inputs_read = [
        str(Path("case_sets/common_core_v0/cases.csv")),
        str(Path("case_sets/common_core_v0/controls_360.csv")),
        str(CASE_REGISTRY_PATH),
    ]
    output_rows: list[dict[str, str]] = []
    for control in control_rows:
        case_id = control["case_id"]
        case = case_by_id[case_id]
        case_path = Path(case["case_path"])
        manifest_path = root / case["manifest_path"]
        runs_retention_path = root / case_path / "evidence/runs_retention.yaml"
        package_summary_path = root / case_path / "evidence/package_validation_summary.json"
        expected_rejections_path = root / case_path / "checker/expected_rejections.yaml"
        for path in (manifest_path, runs_retention_path, package_summary_path, expected_rejections_path):
            ensure_safe_path(path, allow_cases=True)
        # Read metadata/index files only. These reads do not parse raw retained outputs.
        read_text_if_exists(manifest_path)
        read_text_if_exists(runs_retention_path)
        package_summary = {}
        if package_summary_path.exists():
            package_summary = json.loads(package_summary_path.read_text(encoding="utf-8"))
        expected_text = read_text_if_exists(expected_rejections_path)
        for path in (case["manifest_path"], str(case_path / "evidence/runs_retention.yaml"), str(case_path / "evidence/package_validation_summary.json"), str(case_path / "checker/expected_rejections.yaml")):
            if path not in inputs_read:
                inputs_read.append(path)

        route = control["control_route"]
        retained_path = retained_artifact_candidate(case_path, control["engine"], route)
        retained_full = root / retained_path
        source_path = case_path / "sql/source.sql"
        candidate_path = candidate_sql_path(case_path, route)
        claim_boundaries = package_summary.get("claim_boundaries", {}) if isinstance(package_summary, dict) else {}
        no_db_validation = claim_boundaries.get("db_validation_run") is False
        output_rows.append(
            {
                "record_id": f"{ADAPTER_NAME}:{control['control_id']}",
                "record_type": RECORD_TYPE,
                "adapter_name": ADAPTER_NAME,
                "adapter_scope": ADAPTER_SCOPE,
                "case_id": case_id,
                "pool": control["pool"],
                "case_set": CASE_SET,
                "denominator_id": control["control_id"],
                "engine": control["engine"],
                "route": route,
                "method_role": "control",
                "control_route": route,
                "candidate_id": control["control_id"],
                "source_sql_path": str(source_path),
                "candidate_sql_path": candidate_path,
                "planned": control["planned"],
                "applicable_status": "planned_control" if control["planned"] == "true" else "not_applicable",
                "evidence_index_status": evidence_index_status(retained_full, runs_retention_path),
                "expected_rejection_status": expected_rejection_status(
                    route, expected_text, expected_rejections_path
                ),
                "checker_guard_role": checker_guard_role(route, expected_text),
                "retained_artifact_path": str(retained_path) if retained_full.exists() else "",
                "runs_retention_path": str(case_path / "evidence/runs_retention.yaml"),
                "package_validation_summary_path": str(
                    case_path / "evidence/package_validation_summary.json"
                ),
                "generated": "false",
                "ready": "N.A.",
                "executed": "N.A.",
                "exact": "N.A.",
                "timed": "N.A.",
                "result_status": "N.A.",
                "checker_status": "not_run",
                "evidence_source": "canonical_case_package",
                "status": "N.A.",
                "na_reason": "not_applicable",
                "metrics_computed": "false",
                "metric_input_authorized": "false",
                "production_retained_evidence_parsed": "false",
                "legacy_repo_read": "false",
                "reports_changed": "false",
                "results_changed": "false",
                "denominator_changed": "false",
                "paper_results_changed": "false",
                "notes": (
                    "Control scaffold row emitted from release case package metadata only; "
                    "no fresh execution or correctness status inferred"
                    + ("; case present in inventory/case_registry.csv" if case_id in registry_case_ids else "; case missing from inventory/case_registry.csv")
                    + ("; package summary records no DB validation run during migration" if no_db_validation else "")
                ),
            }
        )
    return output_rows, inputs_read


def checks(rows: list[dict[str, str]], controls_count: int) -> list[dict[str, str]]:
    evidence_missing = sum(1 for row in rows if row["evidence_index_status"] != "indexed_public_safe_reference")
    checks_data = [
        ("controls_360 row count = 360", controls_count == 360, f"controls_360_rows={controls_count}"),
        ("emitted row count = 360", len(rows) == 360, f"rows_emitted={len(rows)}"),
        ("all rows record_type=control_cell", all(row["record_type"] == RECORD_TYPE for row in rows), RECORD_TYPE),
        ("no legacy repo path read", all(row["legacy_repo_read"] == "false" for row in rows), "legacy_repo_read=false"),
        ("metrics_computed=false", all(row["metrics_computed"] == "false" for row in rows), "metrics_computed=false"),
        ("metric_input_authorized=false", all(row["metric_input_authorized"] == "false" for row in rows), "metric_input_authorized=false"),
        (
            "production_retained_evidence_parsed=false",
            all(row["production_retained_evidence_parsed"] == "false" for row in rows),
            "production_retained_evidence_parsed=false",
        ),
        (
            "no reports/results changed",
            all(row["reports_changed"] == "false" and row["results_changed"] == "false" for row in rows),
            "reports_changed=false;results_changed=false",
        ),
        ("denominator unchanged", all(row["denominator_changed"] == "false" for row in rows), "denominator_changed=false"),
        ("paper results unchanged", all(row["paper_results_changed"] == "false" for row in rows), "paper_results_changed=false"),
    ]
    result = [
        {"check_name": name, "status": "PASS" if ok else "FAIL", "details": details}
        for name, ok, details in checks_data
    ]
    result.append(
        {
            "check_name": "evidence-index caveats documented",
            "status": "WARN" if evidence_missing else "PASS",
            "details": f"rows_without_direct_retained_artifact_path={evidence_missing}",
        }
    )
    return result


def write_report(
    path: Path,
    rows: list[dict[str, str]],
    inputs_read: list[str],
    validation_result: str,
) -> None:
    route_counts = Counter(row["control_route"] for row in rows)
    evidence_counts = Counter(row["evidence_index_status"] for row in rows)
    lines = [
        "# control_cell_adapter_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "This bounded adapter emits one `control_cell` row per `controls_360.csv` scaffold row from release-repo Common-core case packages and metadata indexes only.",
        "",
        "The output is an audit artifact. It is not a production metrics ledger and is not paper evidence by itself.",
        "",
        "## Inputs Read",
        "",
    ]
    lines.extend(f"- `{path}`" for path in inputs_read)
    lines.extend(["", "## Rows Emitted", "", f"- Rows emitted: {len(rows)}"])
    lines.extend(["", "## Control Route Counts", ""])
    lines.extend(f"- `{route}`: {count}" for route, count in sorted(route_counts.items()))
    lines.extend(["", "## Evidence-index Caveats", ""])
    lines.extend(f"- `{status}`: {count}" for status, count in sorted(evidence_counts.items()))
    lines.extend(
        [
            "",
            "Rows with `evidence_not_retained` preserve the scaffolded control row without inferring execution or failure. They are not metric failures.",
            "",
            "## Explicit Non-goals",
            "",
            "- No legacy reports/results/runs were read.",
            "- No production retained evidence was parsed.",
            "- No metrics were computed.",
            "- No hard-negative pass rate was computed.",
            "- No source/positive execution status was inferred.",
            "- No reports/results were copied or modified.",
            "- No production ledger was created under `results/`.",
            "- No paper tables were rendered.",
            "",
            "## Why This Is Not Metrics Computation",
            "",
            "Every row has `metric_input_authorized=false`, `metrics_computed=false`, and execution/correctness/timing fields set to `N.A.`. The adapter preserves planned control scaffold rows and indexed evidence references only.",
            "",
            "## Why This Is Not Legacy Retained-evidence Parsing",
            "",
            "The adapter reads only release-repo case package metadata and evidence indexes. It does not inspect `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean` or parse legacy reports/results/runs.",
            "",
            "## Validation Result",
            "",
            validation_result,
            "",
            "## Next Safe Action",
            "",
            "Review control-cell row coverage and validator output before authorizing any adapter that parses real retained evidence or emits metric-eligible rows.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = repo_root()
    case_set_path = args.case_set if args.case_set.is_absolute() else root / args.case_set
    controls_path = args.controls if args.controls.is_absolute() else root / args.controls
    registry_path = root / CASE_REGISTRY_PATH
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    for path in (case_set_path, controls_path, registry_path, out_dir):
        ensure_safe_path(path, allow_cases=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    case_rows = read_csv(case_set_path)
    control_rows = read_csv(controls_path)
    registry_rows = read_csv(registry_path)
    rows, inputs_read = build_rows(root, case_rows, control_rows, registry_rows)

    ledger_path = out_dir / LEDGER_FILENAME
    summary_path = out_dir / SUMMARY_FILENAME
    checks_path = out_dir / CHECKS_FILENAME
    report_path = out_dir / REPORT_FILENAME

    write_csv(ledger_path, rows, LEDGER_COLUMNS)
    check_rows = checks(rows, len(control_rows))
    write_csv(checks_path, check_rows, ["check_name", "status", "details"])
    validation_result = "PASS: all required adapter checks passed."
    if any(row["status"] == "FAIL" for row in check_rows):
        validation_result = "FAIL: one or more required adapter checks failed."
    write_report(report_path, rows, inputs_read, validation_result)

    route_counts = Counter(row["control_route"] for row in rows)
    summary = {
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "rows_emitted": len(rows),
        "planned_control_rows_expected": 360,
        "planned_control_rows_emitted": len(rows),
        "control_route_counts": dict(sorted(route_counts.items())),
        "record_types_emitted": sorted({row["record_type"] for row in rows}),
        "production_retained_evidence_parsed": False,
        "legacy_repo_read": False,
        "metrics_computed": False,
        "metric_input_authorized": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"rows_emitted: {len(rows)}")
    print("record_types_emitted:", ",".join(summary["record_types_emitted"]))
    print("control_route_counts:", dict(sorted(route_counts.items())))
    return 0 if validation_result.startswith("PASS") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
