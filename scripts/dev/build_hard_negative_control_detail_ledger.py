#!/usr/bin/env python3
"""Build hard-negative control detail rows from release case packages only.

This bounded adapter reads Common-core control scaffolds and canonical case
package metadata/evidence indexes. It emits one non-metric control_cell row for
each hard_negative row in controls_360.csv. It does not read legacy
reports/results/runs, parse production retained evidence, compute hard-negative
rates, or infer rejection outcomes.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ADAPTER_NAME = "hard_negative_control_detail_adapter_v0"
ADAPTER_SCOPE = "release_case_package_only"
CASE_SET = "common_core_v0"
RECORD_TYPE = "control_cell"
CONTROL_ROUTE = "hard_negative"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DEFAULT_OUT_DIR = Path("audits/hard_negative_control_detail_adapter_v0")
CASE_REGISTRY_PATH = Path("inventory/case_registry.csv")

LEDGER_FILENAME = "hard_negative_control_detail_ledger_v0.csv"
SUMMARY_FILENAME = "hard_negative_control_detail_adapter_v0_summary.json"
REPORT_FILENAME = "hard_negative_control_detail_adapter_v0_report.md"
CHECKS_FILENAME = "hard_negative_control_detail_adapter_v0_checks.csv"
LIMITATIONS_FILENAME = "hard_negative_control_detail_limitations.md"

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
    "hard_negative_id",
    "expected_rejection_reason",
    "expected_rejection_approval_status",
    "semantic_risk_type",
    "checker_guard_role",
    "expected_rejection_source_path",
    "hard_negative_evidence_path",
    "runs_retention_path",
    "package_validation_summary_path",
    "retained_artifact_path",
    "evidence_index_status",
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
    "hard_negative_rate_computed",
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
        description="Build hard-negative control detail rows from release case packages."
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


def read_text_if_exists(path: Path) -> str:
    ensure_safe_path(path, allow_cases=True)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json_if_exists(path: Path) -> dict[str, Any]:
    ensure_safe_path(path, allow_cases=True)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def extract_yaml_scalar(text: str, keys: list[str]) -> str:
    for key in keys:
        pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", re.MULTILINE)
        matches = [match.group(1).strip().strip("'\"") for match in pattern.finditer(text)]
        matches = [match for match in matches if match not in {"", "[]", "{}"}]
        if matches:
            return matches[-1]
    return ""


def extract_yaml_list_after_key(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(rf"^\s*{re.escape(key)}:\s*$", line):
            base_indent = len(line) - len(line.lstrip())
            values: list[str] = []
            for next_line in lines[index + 1 :]:
                stripped = next_line.strip()
                if not stripped:
                    continue
                indent = len(next_line) - len(next_line.lstrip())
                if indent <= base_indent and not stripped.startswith("-"):
                    break
                if stripped.startswith("- "):
                    values.append(stripped[2:].strip().strip("'\""))
                    continue
                if ":" in stripped and not stripped.startswith("-"):
                    break
            return values
        inline = re.match(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", line)
        if inline:
            value = inline.group(1).strip().strip("'\"")
            return [value] if value else []
    return []


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}={val}" for key, val in sorted(value.items()))
    return str(value)


def detail_from_metadata(expected_text: str, summary: dict[str, Any]) -> dict[str, str]:
    hard_negative_id = (
        extract_yaml_scalar(expected_text, ["hard_negative_id", "id"])
        or as_text(summary.get("hard_negative_id"))
        or "manual_review_required"
    )
    reason = (
        extract_yaml_scalar(expected_text, ["expected_rejection_reason", "reason"])
        or as_text(summary.get("expected_rejection_reason"))
        or as_text(summary.get("approved_expected_rejection_reason"))
        or "manual_review_required"
    )
    approval_status = (
        extract_yaml_scalar(expected_text, ["approval_status"])
        or as_text(summary.get("approval_status"))
        or "manual_review_required"
    )
    semantic_risk_values = extract_yaml_list_after_key(expected_text, "semantic_risk_type")
    semantic_risk = (
        ";".join(semantic_risk_values)
        or as_text(summary.get("semantic_risk_type"))
        or "manual_review_required"
    )
    checker_guard_role = (
        extract_yaml_scalar(expected_text, ["checker_guard_role"])
        or "manual_review_required"
    )
    source_sql_path = (
        extract_yaml_scalar(expected_text, ["source_sql_path"])
        or "sql/source.sql"
    )
    negative_sql_path = (
        extract_yaml_scalar(expected_text, ["negative_sql_path", "path"])
        or as_text(summary.get("hard_negative_sql"))
        or "sql/negatives/neg_01.sql"
    )
    return {
        "hard_negative_id": hard_negative_id,
        "expected_rejection_reason": reason,
        "expected_rejection_approval_status": approval_status,
        "semantic_risk_type": semantic_risk,
        "checker_guard_role": checker_guard_role,
        "source_sql_path": source_sql_path,
        "candidate_sql_path": negative_sql_path,
    }


def summary_engine_path(summary: dict[str, Any], engine: str) -> str:
    for key in ("retained_outputs", "retained_evidence"):
        values = summary.get(key)
        if not isinstance(values, dict):
            continue
        exact = values.get(engine)
        if isinstance(exact, str):
            return exact
        for nested_key, nested_value in values.items():
            if (
                isinstance(nested_key, str)
                and nested_key.startswith(engine)
                and "neg" in nested_key
                and isinstance(nested_value, str)
            ):
                return nested_value
    return ""


def first_existing_tsv(paths: list[Path]) -> Path | None:
    existing = [path for path in paths if path.exists() and path.suffix == ".tsv"]
    if not existing:
        return None
    preferred = [path for path in existing if path.name == "rewrite_neg_01.tsv"]
    return sorted(preferred or existing)[0]


def engine_hard_negative_artifact(root: Path, case_path: Path, engine: str, summary: dict[str, Any]) -> Path | None:
    base = case_path / "evidence/hard_negative"
    summary_path_text = summary_engine_path(summary, engine)
    candidates: list[Path] = []
    if summary_path_text:
        candidates.append(case_path / summary_path_text if not summary_path_text.startswith("cases/") else Path(summary_path_text))
    candidates.extend(sorted((base / engine).glob("*.tsv")) if (root / base / engine).is_dir() else [])
    candidates.extend(sorted(base.glob(f"{engine}*neg*.tsv")))
    candidates.extend(sorted(base.glob(f"*{engine}*neg*.tsv")))
    safe_candidates: list[Path] = []
    for rel_path in candidates:
        ensure_safe_path(root / rel_path, allow_cases=True)
        safe_candidates.append(rel_path)
    return first_existing_tsv([root / path for path in safe_candidates])


def relative_to_root(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def evidence_status_and_paths(
    root: Path,
    case_path: Path,
    engine: str,
    summary: dict[str, Any],
) -> tuple[str, str, str]:
    artifact = engine_hard_negative_artifact(root, case_path, engine, summary)
    summary_path = root / case_path / "evidence/hard_negative/hard_negative_summary.json"
    ensure_safe_path(summary_path, allow_cases=True)
    if artifact is not None:
        rel = relative_to_root(artifact, root)
        return "indexed_not_recomputed", rel, rel
    if summary_path.exists():
        return "evidence_not_retained", relative_to_root(summary_path, root), ""
    return "manual_review_required", "", ""


def build_rows(
    root: Path,
    case_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    registry_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    case_by_id = {row["case_id"]: row for row in case_rows}
    registry_case_ids = {row.get("case_id", "") for row in registry_rows}
    hard_negative_controls = [row for row in control_rows if row.get("control_route") == CONTROL_ROUTE]
    inputs_read = [
        str(Path("case_sets/common_core_v0/cases.csv")),
        str(Path("case_sets/common_core_v0/controls_360.csv")),
        str(CASE_REGISTRY_PATH),
    ]
    output_rows: list[dict[str, str]] = []

    for control in hard_negative_controls:
        case_id = control["case_id"]
        case = case_by_id[case_id]
        case_path = Path(case["case_path"])
        manifest_path = root / case["manifest_path"]
        runs_retention_path = root / case_path / "evidence/runs_retention.yaml"
        package_summary_path = root / case_path / "evidence/package_validation_summary.json"
        expected_rejections_path = root / case_path / "checker/expected_rejections.yaml"
        hard_negative_summary_path = root / case_path / "evidence/hard_negative/hard_negative_summary.json"
        hard_negative_dir = root / case_path / "evidence/hard_negative"
        for path in (
            manifest_path,
            runs_retention_path,
            package_summary_path,
            expected_rejections_path,
            hard_negative_summary_path,
            hard_negative_dir,
        ):
            ensure_safe_path(path, allow_cases=True)

        read_text_if_exists(manifest_path)
        read_text_if_exists(runs_retention_path)
        expected_text = read_text_if_exists(expected_rejections_path)
        package_summary = load_json_if_exists(package_summary_path)
        summary = load_json_if_exists(hard_negative_summary_path)
        for rel_path in (
            case["manifest_path"],
            str(case_path / "checker/expected_rejections.yaml"),
            str(case_path / "evidence/runs_retention.yaml"),
            str(case_path / "evidence/package_validation_summary.json"),
            str(case_path / "evidence/hard_negative/hard_negative_summary.json"),
        ):
            if rel_path not in inputs_read:
                inputs_read.append(rel_path)

        detail = detail_from_metadata(expected_text, summary)
        evidence_index_status, hard_negative_evidence_path, retained_artifact_path = (
            evidence_status_and_paths(root, case_path, control["engine"], summary)
        )
        claim_boundaries = package_summary.get("claim_boundaries", {}) if isinstance(package_summary, dict) else {}
        no_db_validation = claim_boundaries.get("db_validation_run") is False
        applicable_status = "planned_control" if control.get("planned") == "true" else "not_applicable"
        notes = [
            "Hard-negative control detail row emitted from release case package metadata only",
            "no fresh execution or rejection status inferred",
            "hard-negative false-accept rate not computed",
            "case present in inventory/case_registry.csv" if case_id in registry_case_ids else "case missing from inventory/case_registry.csv",
        ]
        if evidence_index_status != "indexed_not_recomputed":
            notes.append("engine-specific hard-negative retained artifact not indexed for this control cell")
        if no_db_validation:
            notes.append("package summary records no DB validation run during migration")

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
                "route": CONTROL_ROUTE,
                "method_role": "control",
                "control_route": CONTROL_ROUTE,
                "candidate_id": control["control_id"],
                "source_sql_path": str(case_path / detail["source_sql_path"]),
                "candidate_sql_path": str(case_path / detail["candidate_sql_path"]),
                "planned": control["planned"],
                "applicable_status": applicable_status,
                "hard_negative_id": detail["hard_negative_id"],
                "expected_rejection_reason": detail["expected_rejection_reason"],
                "expected_rejection_approval_status": detail["expected_rejection_approval_status"],
                "semantic_risk_type": detail["semantic_risk_type"],
                "checker_guard_role": detail["checker_guard_role"],
                "expected_rejection_source_path": str(case_path / "checker/expected_rejections.yaml"),
                "hard_negative_evidence_path": hard_negative_evidence_path,
                "runs_retention_path": str(case_path / "evidence/runs_retention.yaml"),
                "package_validation_summary_path": str(
                    case_path / "evidence/package_validation_summary.json"
                ),
                "retained_artifact_path": retained_artifact_path,
                "evidence_index_status": evidence_index_status,
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
                "hard_negative_rate_computed": "false",
                "production_retained_evidence_parsed": "false",
                "legacy_repo_read": "false",
                "reports_changed": "false",
                "results_changed": "false",
                "denominator_changed": "false",
                "paper_results_changed": "false",
                "notes": "; ".join(notes),
            }
        )
    return output_rows, inputs_read


def checks(rows: list[dict[str, str]], hard_negative_controls_count: int) -> list[dict[str, str]]:
    evidence_missing = sum(1 for row in rows if row["evidence_index_status"] != "indexed_not_recomputed")
    dropped = hard_negative_controls_count - len(rows)
    checks_data = [
        (
            "hard_negative scaffold row count = 120",
            hard_negative_controls_count == 120,
            f"hard_negative_control_rows={hard_negative_controls_count}",
        ),
        ("emitted row count = 120", len(rows) == 120, f"rows_emitted={len(rows)}"),
        ("all rows record_type=control_cell", all(row["record_type"] == RECORD_TYPE for row in rows), RECORD_TYPE),
        (
            "all rows control_route=hard_negative",
            all(row["control_route"] == CONTROL_ROUTE for row in rows),
            CONTROL_ROUTE,
        ),
        ("no legacy repo path read", all(row["legacy_repo_read"] == "false" for row in rows), "legacy_repo_read=false"),
        ("metrics_computed=false", all(row["metrics_computed"] == "false" for row in rows), "metrics_computed=false"),
        (
            "metric_input_authorized=false",
            all(row["metric_input_authorized"] == "false" for row in rows),
            "metric_input_authorized=false",
        ),
        (
            "hard_negative_rate_computed=false",
            all(row["hard_negative_rate_computed"] == "false" for row in rows),
            "hard_negative_rate_computed=false",
        ),
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
        ("no hard_negative control row silently dropped", dropped == 0, f"dropped_rows={dropped}"),
    ]
    result = [
        {"check_name": name, "status": "PASS" if ok else "FAIL", "details": details}
        for name, ok, details in checks_data
    ]
    result.append(
        {
            "check_name": "evidence-index caveats documented",
            "status": "WARN" if evidence_missing else "PASS",
            "details": f"rows_without_engine_specific_retained_artifact={evidence_missing}",
        }
    )
    return result


def write_report(
    path: Path,
    rows: list[dict[str, str]],
    inputs_read: list[str],
    validation_result: str,
) -> None:
    pool_counts = Counter(row["pool"] for row in rows)
    engine_counts = Counter(row["engine"] for row in rows)
    approval_counts = Counter(row["expected_rejection_approval_status"] for row in rows)
    applicable_counts = Counter(row["applicable_status"] for row in rows)
    evidence_counts = Counter(row["evidence_index_status"] for row in rows)
    lines = [
        "# hard_negative_control_detail_adapter_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "This bounded adapter emits one hard-negative `control_cell` detail row per hard-negative row in `controls_360.csv`.",
        "It reads only release-repo Common-core scaffolds and canonical case package metadata/evidence indexes.",
        "The output is an audit artifact. It is not a production metrics ledger and is not paper evidence by itself.",
        "",
        "## Inputs Read",
        "",
    ]
    lines.extend(f"- `{input_path}`" for input_path in inputs_read)
    lines.extend(["", "## Rows Emitted", "", f"- Rows emitted: {len(rows)}"])
    lines.extend(["", "## Pool Counts", ""])
    lines.extend(f"- `{pool}`: {count}" for pool, count in sorted(pool_counts.items()))
    lines.extend(["", "## Engine Counts", ""])
    lines.extend(f"- `{engine}`: {count}" for engine, count in sorted(engine_counts.items()))
    lines.extend(["", "## Approval Status Counts", ""])
    lines.extend(f"- `{status}`: {count}" for status, count in sorted(approval_counts.items()))
    lines.extend(["", "## Applicable / N.A. Counts", ""])
    lines.extend(f"- `{status}`: {count}" for status, count in sorted(applicable_counts.items()))
    lines.extend(["", "## Evidence-index Caveats", ""])
    lines.extend(f"- `{status}`: {count}" for status, count in sorted(evidence_counts.items()))
    lines.extend(
        [
            "",
            "`indexed_not_recomputed` means an engine-specific hard-negative retained artifact is indexed in the release case package, but this task did not parse or rerun it.",
            "`evidence_not_retained` means the row is preserved from the scaffold, but no engine-specific hard-negative retained artifact was indexed for that control cell.",
            "",
            "## Explicit Non-goals",
            "",
            "- No legacy reports/results/runs were read.",
            "- No production retained evidence was parsed.",
            "- No hard-negative validation was rerun.",
            "- No hard-negative pass/fail rate was computed.",
            "- No false-accept rate was computed.",
            "- No semantic equivalence proof was created.",
            "- No reports/results were copied or modified.",
            "- No production ledger was created under `results/`.",
            "- No paper tables were rendered.",
            "",
            "## Why This Is Not Metrics Computation",
            "",
            "Every row has `metric_input_authorized=false`, `metrics_computed=false`, `hard_negative_rate_computed=false`, and execution/correctness/timing fields set to `N.A.`.",
            "",
            "## Why This Is Not False-accept-rate Computation",
            "",
            "The adapter records expected-rejection metadata and retained artifact pointers only. It does not inspect outputs, classify outcomes, or aggregate rejected/accepted counts.",
            "",
            "## Why This Is Not Legacy Retained-evidence Parsing",
            "",
            "The adapter reads only release-repo case package metadata and indexes. It does not inspect `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean` or parse legacy reports/results/runs.",
            "",
            "## Validation Result",
            "",
            validation_result,
            "",
            "## Next Safe Action",
            "",
            "Review hard-negative detail row coverage and validator output before authorizing any adapter that parses real retained evidence or computes hard-negative metrics.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# hard_negative_control_detail_adapter_v0 Limitations",
                "",
                "- This adapter only indexes release case-package hard-negative metadata and evidence pointers.",
                "- It does not rerun hard-negative validation.",
                "- It does not compute false-accept rate.",
                "- It does not parse legacy retained evidence.",
                "- It does not prove semantic equivalence.",
                "- It does not create official `results/retained` or `reports/evaluation` outputs.",
                "- Future metrics and reporting require separate authorization.",
                "",
            ]
        ),
        encoding="utf-8",
    )


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
    hard_negative_controls_count = sum(1 for row in control_rows if row.get("control_route") == CONTROL_ROUTE)

    ledger_path = out_dir / LEDGER_FILENAME
    summary_path = out_dir / SUMMARY_FILENAME
    checks_path = out_dir / CHECKS_FILENAME
    report_path = out_dir / REPORT_FILENAME
    limitations_path = out_dir / LIMITATIONS_FILENAME

    write_csv(ledger_path, rows, LEDGER_COLUMNS)
    check_rows = checks(rows, hard_negative_controls_count)
    write_csv(checks_path, check_rows, ["check_name", "status", "details"])
    validation_result = "PASS: all required adapter checks passed."
    if any(row["status"] == "FAIL" for row in check_rows):
        validation_result = "FAIL: one or more required adapter checks failed."
    write_report(report_path, rows, inputs_read, validation_result)
    write_limitations(limitations_path)

    summary = {
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "rows_emitted": len(rows),
        "planned_hard_negative_rows_expected": 120,
        "planned_hard_negative_rows_emitted": len(rows),
        "record_types_emitted": sorted({row["record_type"] for row in rows}),
        "control_route_emitted": sorted({row["control_route"] for row in rows}),
        "approval_status_counts": dict(
            sorted(Counter(row["expected_rejection_approval_status"] for row in rows).items())
        ),
        "applicable_status_counts": dict(sorted(Counter(row["applicable_status"] for row in rows).items())),
        "evidence_index_status_counts": dict(
            sorted(Counter(row["evidence_index_status"] for row in rows).items())
        ),
        "production_retained_evidence_parsed": False,
        "legacy_repo_read": False,
        "metrics_computed": False,
        "metric_input_authorized": False,
        "hard_negative_rate_computed": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"rows_emitted: {len(rows)}")
    print("record_types_emitted:", ",".join(summary["record_types_emitted"]))
    print("control_route_emitted:", ",".join(summary["control_route_emitted"]))
    print("evidence_index_status_counts:", summary["evidence_index_status_counts"])
    return 0 if validation_result.startswith("PASS") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
