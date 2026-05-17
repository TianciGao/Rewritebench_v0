#!/usr/bin/env python3
"""Build a draft retained-summary ledger from release-repo summaries only.

This adapter skeleton is intentionally narrow. It emits only
``retained_summary_artifact`` rows from selected release-repo summaries,
case-set scaffolds, inventory files, and repository specifications. It does
not parse legacy retained evidence, compute metrics, or create production
ledger outputs under reports/results.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ADAPTER_NAME = "retained_summary_adapter_v0"
ADAPTER_SCOPE = "release_repo_summary_only"
RECORD_TYPE = "retained_summary_artifact"
CASE_SET = "common_core_v0"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DEFAULT_OUT_DIR = Path("audits/retained_summary_adapter_v0")

LEDGER_FILENAME = "retained_summary_ledger_v0.csv"
SUMMARY_FILENAME = "retained_summary_adapter_v0_summary.json"
REPORT_FILENAME = "retained_summary_adapter_v0_report.md"
CHECKS_FILENAME = "retained_summary_adapter_v0_checks.csv"
LIMITATIONS_FILENAME = "retained_summary_adapter_v0_limitations.md"

LEDGER_COLUMNS = [
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
    "source_artifact_path",
    "source_artifact_kind",
    "source_artifact_exists",
    "related_scope",
    "related_case_set",
    "related_pool",
    "related_case_id",
    "denominator_id",
    "evidence_role",
    "summary_status",
    "claim_boundary",
    "supports_metric_family",
    "metric_input_authorized",
    "not_metric_input",
    "metrics_computed",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
    "retained_artifact_path",
    "notes",
]


@dataclass(frozen=True)
class InputSpec:
    path: str
    kind: str
    evidence_role: str
    related_scope: str
    claim_boundary: str
    supports_metric_family: str = "none"
    related_pool: str = ""
    related_case_id: str = ""
    denominator_id: str = ""
    optional: bool = True


SUMMARY_INPUTS = [
    InputSpec(
        "audits/common_core40_final_closeout/common_core40_final_closeout_summary.md",
        "audit_summary_md",
        "common_core_closeout_summary",
        "common_core_40",
        "canonical package closeout evidence summary only",
    ),
    InputSpec(
        "audits/common_core40_final_closeout/common_core40_final_status_snapshot.json",
        "audit_summary_json",
        "common_core_closeout_snapshot",
        "common_core_40",
        "machine-readable closeout status summary only",
    ),
    InputSpec(
        "audits/common_core40_registry_alignment/common_core40_registry_alignment_summary.md",
        "audit_summary_md",
        "registry_alignment_summary",
        "common_core_v0",
        "membership and scaffold alignment summary only",
    ),
    InputSpec(
        "audits/common_core40_registry_alignment/common_core40_registry_alignment_summary.json",
        "audit_summary_json",
        "registry_alignment_snapshot",
        "common_core_v0",
        "machine-readable registry alignment summary only",
    ),
    InputSpec(
        "audits/reports_results_retained_evidence_map/reports_results_retained_evidence_summary.md",
        "audit_summary_md",
        "reports_results_mapping_summary",
        "common_core_v0",
        "retained-evidence map summary; no copied reports/results",
    ),
    InputSpec(
        "audits/reports_results_retained_evidence_map/reports_results_retained_evidence_summary.json",
        "audit_summary_json",
        "reports_results_mapping_snapshot",
        "common_core_v0",
        "machine-readable retained-evidence map summary only",
    ),
    InputSpec(
        "audits/retained_evidence_ledger_mapping/retained_evidence_ledger_mapping_summary.md",
        "audit_summary_md",
        "retained_evidence_to_ledger_mapping_summary",
        "common_core_v0",
        "field-coverage mapping summary; not adapter output",
    ),
    InputSpec(
        "audits/retained_evidence_ledger_mapping/retained_evidence_ledger_mapping_summary.json",
        "audit_summary_json",
        "retained_evidence_to_ledger_mapping_snapshot",
        "common_core_v0",
        "machine-readable field-coverage mapping summary only",
    ),
    InputSpec(
        "audits/metrics_contract_formalization/metrics_contract_formalization_summary.md",
        "audit_summary_md",
        "metrics_contract_formalization_summary",
        "metrics_contract_v1",
        "metric contract formalization summary; no metrics computed",
        "all_primary_metrics_reference_only",
    ),
    InputSpec(
        "audits/metrics_contract_formalization/metrics_contract_formalization_summary.json",
        "audit_summary_json",
        "metrics_contract_formalization_snapshot",
        "metrics_contract_v1",
        "machine-readable metric contract summary; no metrics computed",
        "all_primary_metrics_reference_only",
    ),
    InputSpec(
        "audits/retained_evidence_adapter_design/retained_evidence_adapter_design_summary.md",
        "audit_summary_md",
        "adapter_design_summary",
        "retained_evidence_adapter_design",
        "adapter design summary; not implementation output",
    ),
    InputSpec(
        "audits/retained_evidence_adapter_design/retained_evidence_adapter_design_summary.json",
        "audit_summary_json",
        "adapter_design_snapshot",
        "retained_evidence_adapter_design",
        "machine-readable adapter design summary only",
    ),
    InputSpec(
        "audits/ledger_schema_validation_fixtures/ledger_schema_validation_fixtures_summary.json",
        "audit_summary_json",
        "ledger_fixture_schema_summary",
        "synthetic_fixture_validation",
        "synthetic fixture summary only",
    ),
    InputSpec(
        "audits/ledger_fixture_validator_hardening/ledger_fixture_hardening_summary.json",
        "audit_summary_json",
        "ledger_fixture_hardening_summary",
        "synthetic_fixture_validation",
        "hardened fixture validation summary only",
    ),
    InputSpec(
        "audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json",
        "audit_summary_json",
        "ledger_fixture_dev_smoke_summary",
        "synthetic_fixture_validation",
        "developer smoke output summary only",
    ),
    InputSpec(
        "audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_summary.json",
        "audit_summary_json",
        "ledger_fixture_ci_smoke_summary",
        "synthetic_fixture_validation",
        "CI smoke wiring summary only",
    ),
    InputSpec(
        "audits/production_ledger_validation_gates/production_ledger_validation_gates_summary.md",
        "audit_summary_md",
        "production_ledger_gate_summary",
        "production_ledger_validation_planning",
        "validation-gate planning summary only",
    ),
    InputSpec(
        "audits/production_ledger_validation_gates/production_ledger_validation_gates_summary.json",
        "audit_summary_json",
        "production_ledger_gate_snapshot",
        "production_ledger_validation_planning",
        "machine-readable validation-gate planning summary only",
    ),
]

SCAFFOLD_INPUTS = [
    InputSpec(
        "case_sets/common_core_v0/manifest.yaml",
        "case_set_manifest",
        "case_set_membership_scaffold",
        "common_core_v0",
        "release membership scaffold only; no denominator values changed",
        optional=False,
    ),
    InputSpec(
        "case_sets/common_core_v0/cases.csv",
        "case_set_cases_csv",
        "case_set_membership_scaffold",
        "common_core_v0",
        "40 fixed Common-core membership rows; not result evidence",
        optional=False,
    ),
    InputSpec(
        "case_sets/common_core_v0/denominator_same_engine_120.csv",
        "denominator_scaffold_csv",
        "planned_denominator_scaffold",
        "common_core_v0_track_a_same_engine",
        "120 planned same-engine rows; no metrics computed",
        "coverage_and_performance_denominator_reference_only",
        optional=False,
    ),
    InputSpec(
        "case_sets/common_core_v0/controls_360.csv",
        "control_scaffold_csv",
        "planned_control_scaffold",
        "common_core_v0_controls",
        "360 planned control rows; checker-control scaffold only",
        "control_denominator_reference_only",
        optional=False,
    ),
    InputSpec(
        "inventory/case_registry.csv",
        "inventory_registry_csv",
        "case_registry_scaffold",
        "common_core_v0",
        "Common-core registry rows; not result evidence",
        optional=False,
    ),
    InputSpec(
        "inventory/source_registry.csv",
        "inventory_registry_csv",
        "source_registry_scaffold",
        "common_core_v0",
        "source-family registry rows; no license claim invented",
        optional=False,
    ),
    InputSpec(
        "repository_spec/metrics_contract_v1.md",
        "repository_spec_md",
        "metrics_contract_reference",
        "metrics_contract_v1",
        "formal metric contract reference; no metrics computed",
        "all_primary_metrics_reference_only",
        optional=False,
    ),
    InputSpec(
        "repository_spec/evidence_record_type_policy_v1_draft.md",
        "repository_spec_md",
        "record_type_policy_reference",
        "evidence_record_type_policy",
        "record-type boundary reference only",
        optional=False,
    ),
    InputSpec(
        "repository_spec/production_ledger_validation_policy_v1_draft.md",
        "repository_spec_md",
        "production_validation_policy_reference",
        "production_ledger_validation_policy",
        "future validation-gate policy reference only",
        optional=False,
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build retained_summary_artifact rows from release-repo summaries only."
    )
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any optional curated input is missing.",
    )
    parser.add_argument(
        "--include-optional-missing",
        action="store_true",
        help="Emit rows for missing optional curated inputs.",
    )
    parser.add_argument(
        "--input-manifest",
        type=Path,
        default=None,
        help="Optional future manifest selecting a subset of curated input paths.",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def assert_release_relative(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        raise ValueError(f"absolute input path is not allowed: {path_text}")
    if ".." in path.parts:
        raise ValueError(f"parent traversal is not allowed: {path_text}")
    first = path.parts[0] if path.parts else ""
    if first in {"reports", "results", "runs"}:
        raise ValueError(f"disallowed output/evidence path is not allowed: {path_text}")
    return path


def assert_not_legacy_path(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo path is not allowed: {path}")


def allowed_specs() -> list[InputSpec]:
    return SUMMARY_INPUTS + SCAFFOLD_INPUTS


def selected_specs(input_manifest: Path | None) -> list[InputSpec]:
    specs = allowed_specs()
    if input_manifest is None:
        return specs

    assert_not_legacy_path(input_manifest)
    if not input_manifest.exists():
        raise FileNotFoundError(f"input manifest not found: {input_manifest}")
    selected_paths = read_input_manifest(input_manifest)
    allowed_by_path = {spec.path: spec for spec in specs}
    unknown = sorted(set(selected_paths) - set(allowed_by_path))
    if unknown:
        raise ValueError(
            "input manifest includes paths outside the curated release input list: "
            + "; ".join(unknown)
        )
    return [allowed_by_path[path] for path in selected_paths]


def read_input_manifest(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
        if isinstance(payload, list):
            values = payload
        elif isinstance(payload, dict) and isinstance(payload.get("inputs"), list):
            values = payload["inputs"]
        else:
            raise ValueError("JSON input manifest must be a list or contain inputs[]")
        return [str(assert_release_relative(str(item))) for item in values]
    return [
        str(assert_release_relative(line.strip()))
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_artifact_metadata(path: Path, kind: str) -> tuple[str, str]:
    """Return summary status and short notes without computing benchmark metrics."""
    if not path.exists():
        return "missing_optional_input", "optional curated input not present"
    if kind.endswith("_json"):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        keys = sorted(data.keys()) if isinstance(data, dict) else []
        return "present", f"JSON parsed for summary metadata; top-level keys: {';'.join(keys[:12])}"
    if kind.endswith("_csv"):
        rows = read_csv_rows(path)
        return "present", f"CSV read for summary metadata; data_rows={len(rows)}"
    text = path.read_text(encoding="utf-8", errors="replace")
    heading = next((line.strip("# ").strip() for line in text.splitlines() if line.startswith("#")), "")
    if heading:
        return "present", f"Markdown/text read for summary metadata; heading={heading}"
    return "present", "Text read for summary metadata"


def make_row(spec: InputSpec, index: int, root: Path, *, exists_override: bool | None = None) -> dict[str, str]:
    rel_path = assert_release_relative(spec.path)
    full_path = root / rel_path
    assert_not_legacy_path(full_path)
    exists = full_path.exists() if exists_override is None else exists_override
    summary_status, metadata_note = read_artifact_metadata(full_path, spec.kind) if exists else (
        "missing_optional_input",
        "optional curated input not present",
    )
    record_id = f"{ADAPTER_NAME}:{index:04d}:{slug(spec.evidence_role)}"
    return {
        "record_id": record_id,
        "record_type": RECORD_TYPE,
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "source_artifact_path": str(rel_path),
        "source_artifact_kind": spec.kind,
        "source_artifact_exists": bool_text(exists),
        "related_scope": spec.related_scope,
        "related_case_set": CASE_SET if spec.related_scope.startswith("common_core") else "",
        "related_pool": spec.related_pool,
        "related_case_id": spec.related_case_id,
        "denominator_id": spec.denominator_id,
        "evidence_role": spec.evidence_role,
        "summary_status": summary_status,
        "claim_boundary": spec.claim_boundary,
        "supports_metric_family": spec.supports_metric_family,
        "metric_input_authorized": "false",
        "not_metric_input": "true",
        "metrics_computed": "false",
        "production_retained_evidence_parsed": "false",
        "legacy_repo_read": "false",
        "reports_changed": "false",
        "results_changed": "false",
        "denominator_changed": "false",
        "paper_results_changed": "false",
        "retained_artifact_path": str(rel_path),
        "notes": metadata_note,
    }


def pool_summary_specs(root: Path) -> list[InputSpec]:
    cases_path = root / "case_sets/common_core_v0/cases.csv"
    if not cases_path.exists():
        return []
    rows = read_csv_rows(cases_path)
    pools = sorted({row["pool"] for row in rows if row.get("pool")})
    specs: list[InputSpec] = []
    for pool in pools:
        count = sum(1 for row in rows if row.get("pool") == pool)
        specs.append(
            InputSpec(
                "case_sets/common_core_v0/cases.csv",
                "pool_summary_from_cases_csv",
                "pool_membership_summary",
                "common_core_v0",
                f"{pool} pool membership count metadata only; no metric computed; cases={count}",
                related_pool=pool,
                optional=False,
            )
        )
    return specs


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def check_rows(rows: list[dict[str, str]], optional_missing: list[str]) -> list[dict[str, str]]:
    checks = [
        (
            "only release repo inputs used",
            all(not row["source_artifact_path"].startswith("/") for row in rows),
            "All emitted rows use repository-relative curated release inputs.",
        ),
        (
            "no legacy repo path read",
            all(row["legacy_repo_read"] == "false" for row in rows),
            "No path under /home/tianci_gao/code/sql-rewrite-bench-artifact-clean was read.",
        ),
        (
            "output rows record_type retained_summary_artifact only",
            all(row["record_type"] == RECORD_TYPE for row in rows),
            "All rows are retained_summary_artifact.",
        ),
        (
            "metric_input_authorized false for all rows",
            all(row["metric_input_authorized"] == "false" for row in rows),
            "No row is authorized as a metric input.",
        ),
        (
            "metrics_computed false",
            all(row["metrics_computed"] == "false" for row in rows),
            "No metric computation performed.",
        ),
        (
            "production_retained_evidence_parsed false",
            all(row["production_retained_evidence_parsed"] == "false" for row in rows),
            "Only release summaries and scaffolds were read.",
        ),
        (
            "reports/results unchanged",
            all(row["reports_changed"] == "false" and row["results_changed"] == "false" for row in rows),
            "No reports/ or results/ outputs were written.",
        ),
        (
            "denominator unchanged",
            all(row["denominator_changed"] == "false" for row in rows),
            "Scaffolds were read only.",
        ),
        (
            "paper results unchanged",
            all(row["paper_results_changed"] == "false" for row in rows),
            "No paper result values inferred or changed.",
        ),
        (
            "output row count greater than zero",
            len(rows) > 0,
            f"rows_emitted={len(rows)}",
        ),
        (
            "no disallowed record types emitted",
            {row["record_type"] for row in rows} == {RECORD_TYPE},
            f"record_types={sorted({row['record_type'] for row in rows})}",
        ),
    ]
    result = [
        {
            "check_name": name,
            "status": "PASS" if ok else "FAIL",
            "details": details,
        }
        for name, ok, details in checks
    ]
    result.append(
        {
            "check_name": "optional missing inputs documented",
            "status": "WARN" if optional_missing else "PASS",
            "details": ";".join(optional_missing) if optional_missing else "No optional curated inputs missing.",
        }
    )
    return result


def write_report(
    path: Path,
    rows: list[dict[str, str]],
    inputs_checked: list[str],
    optional_missing: list[str],
    validation_summary: str,
) -> None:
    lines = [
        "# retained_summary_adapter_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "This adapter skeleton reads selected release-repo summary artifacts, case-set scaffolds, inventory files, and repository specifications, then emits draft ledger-style `retained_summary_artifact` rows.",
        "",
        "It is an audit artifact only. It is not an official production evidence ledger and is not a metrics input.",
        "",
        "## Inputs Read",
        "",
    ]
    lines.extend(f"- `{path}`" for path in inputs_checked)
    lines.extend(["", "## Optional Inputs Missing", ""])
    if optional_missing:
        lines.extend(f"- `{path}`" for path in optional_missing)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Rows Emitted",
            "",
            f"- Rows emitted: {len(rows)}",
            f"- Record type emitted: `{RECORD_TYPE}`",
            "",
            "## Explicit Non-goals",
            "",
            "- No legacy reports/results/runs were read.",
            "- No production retained evidence was parsed.",
            "- No metrics were computed.",
            "- No reports/results were copied or modified.",
            "- No production ledger was created under `results/`.",
            "- No paper tables were rendered.",
            "- No denominator values, paper results, case membership, case packages, or raw legacy evidence were changed.",
            "",
            "## Why This Is Not Metrics Computation",
            "",
            "Every row has `metric_input_authorized=false`, `not_metric_input=true`, and `metrics_computed=false`. Rows summarize artifact provenance and governance boundaries only; they do not contain numerator, denominator, speedup, correctness, or cross-engine metric values.",
            "",
            "## Why This Is Not Production Retained-evidence Parsing",
            "",
            "The script reads only curated release-repo summaries and static scaffolds. It refuses legacy paths and does not inspect `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.",
            "",
            "## Validation Result",
            "",
            validation_summary,
            "",
            "## Next Safe Action",
            "",
            "Review the retained summary adapter v0 output. Any adapter that parses real retained evidence, emits metric-eligible rows, writes `results/retained`, or feeds metrics computation requires separate authorization.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# retained_summary_adapter_v0 Limitations",
                "",
                "- This adapter only reads release-repo summary artifacts, case-set scaffolds, inventory files, and repository specs.",
                "- It does not read legacy retained evidence.",
                "- It does not parse production reports/results/runs.",
                "- It does not compute metrics.",
                "- It does not create official `results/retained` or `reports/evaluation` outputs.",
                "- It emits only `retained_summary_artifact` rows.",
                "- The output is not an official production evidence ledger and is not a metric input.",
                "- Future adapters that parse retained evidence or emit metric-eligible rows need separate authorization.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    root = repo_root()
    out_dir = args.out_dir
    if not out_dir.is_absolute():
        out_dir = root / out_dir
    assert_not_legacy_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    specs = selected_specs(args.input_manifest)
    specs = specs + pool_summary_specs(root)

    rows: list[dict[str, str]] = []
    optional_missing: list[str] = []
    required_missing: list[str] = []
    inputs_checked: list[str] = []
    for spec in specs:
        rel_path = assert_release_relative(spec.path)
        full_path = root / rel_path
        assert_not_legacy_path(full_path)
        exists = full_path.exists()
        if not exists and spec.optional:
            optional_missing.append(spec.path)
            if not args.include_optional_missing:
                continue
        if not exists and not spec.optional:
            required_missing.append(spec.path)
            continue
        inputs_checked.append(spec.path)
        rows.append(make_row(spec, len(rows) + 1, root, exists_override=exists))

    if required_missing:
        raise FileNotFoundError("required curated inputs missing: " + "; ".join(required_missing))
    if args.strict and optional_missing:
        raise FileNotFoundError("optional curated inputs missing in strict mode: " + "; ".join(optional_missing))

    ledger_path = out_dir / LEDGER_FILENAME
    summary_path = out_dir / SUMMARY_FILENAME
    report_path = out_dir / REPORT_FILENAME
    checks_path = out_dir / CHECKS_FILENAME
    limitations_path = out_dir / LIMITATIONS_FILENAME

    write_csv(ledger_path, rows, LEDGER_COLUMNS)
    checks = check_rows(rows, optional_missing)
    write_csv(checks_path, checks, ["check_name", "status", "details"])

    validation_summary = (
        "PASS: retained summary rows emitted with no metric inputs, no production retained "
        "evidence parsing, no legacy repo reads, and no reports/results or denominator changes."
    )
    if any(check["status"] == "FAIL" for check in checks):
        validation_summary = "FAIL: one or more required adapter checks failed."

    summary = {
        "adapter_name": ADAPTER_NAME,
        "adapter_scope": ADAPTER_SCOPE,
        "rows_emitted": len(rows),
        "inputs_checked": len(inputs_checked),
        "optional_inputs_missing": optional_missing,
        "optional_inputs_missing_count": len(optional_missing),
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
    write_report(report_path, rows, inputs_checked, optional_missing, validation_summary)
    write_limitations(limitations_path)

    print(f"rows_emitted: {len(rows)}")
    print(f"inputs_checked: {len(inputs_checked)}")
    print(f"optional_inputs_missing: {len(optional_missing)}")
    print("record_types_emitted:", ",".join(summary["record_types_emitted"]))
    return 1 if any(check["status"] == "FAIL" for check in checks) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
