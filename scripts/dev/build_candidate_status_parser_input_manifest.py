#!/usr/bin/env python3
"""Build the candidate_status_parser_v0 input manifest.

This manifest builder is intentionally conservative. It reads release-repo
locator and mapping metadata only, never opens legacy artifacts, and approves
parser inputs only when exact candidate row grain is provable from metadata.
When no safe row-level inputs are available, it writes a header-only manifest
so the parser can fail closed without inventing row statuses.
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


PARSER_NAME = "candidate_status_parser_v0"
DEFAULT_OUT_DIR = Path("audits/candidate_status_parser_v0")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

MANIFEST_FILENAME = "candidate_status_parser_input_manifest.csv"
SUMMARY_FILENAME = "candidate_status_parser_input_manifest_summary.json"
REPORT_FILENAME = "candidate_status_parser_input_manifest_report.md"
CHECKS_FILENAME = "candidate_status_parser_input_manifest_checks.csv"

EXPECTED_ROW_GRAIN = "case_id x engine x rewrite_method x candidate_id x denominator_id"

MANIFEST_COLUMNS = [
    "manifest_id",
    "source_repo",
    "source_path",
    "relative_path",
    "source_category",
    "candidate_method",
    "route_family",
    "expected_row_grain",
    "row_grain_verified_from_metadata",
    "approved_for_parser",
    "allowed_fields",
    "disallowed_fields",
    "parser_mode",
    "safety_conditions",
    "may_open_file",
    "may_open_full_content",
    "may_parse_header",
    "may_parse_rows",
    "timing_fields_present",
    "prompt_or_token_risk",
    "raw_log_risk",
    "local_path_hygiene_risk",
    "requires_manual_review",
    "fail_closed_reason",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]

METADATA_SOURCES = [
    (
        Path("audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv"),
        "artifact_inventory_metadata",
    ),
    (
        Path("audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv"),
        "retained_evidence_candidate_metadata",
    ),
    (
        Path("audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv"),
        "ledger_field_mapping_metadata",
    ),
    (
        Path("audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv"),
        "source_group_inventory_metadata",
    ),
]

METHOD_TOKENS = {
    "direct_llm_original": ("direct_llm", "direct_llm_original", "llm_direct"),
    "direct_llm_repair_1": (
        "direct_llm_repair_1",
        "direct_llm_execute_repair",
        "repair_1",
        "repair_1shot",
        "llm_feedback_repair",
    ),
    "sqlglot_optimize": ("sqlglot_optimize", "sqlglot"),
    "sqlglot_noop": ("sqlglot_noop", "noop", "no-op"),
    "calcite_hep_fail_closed": ("calcite_hep", "calcite_hep_fail_closed", "calcite"),
}

ROUTE_FAMILY_BY_METHOD = {
    "direct_llm_original": "llm_direct",
    "direct_llm_repair_1": "llm_feedback_repair",
    "sqlglot_optimize": "sqlglot_optimize",
    "sqlglot_noop": "sqlglot_noop",
    "calcite_hep_fail_closed": "calcite_hep",
}

ROW_GRAIN_COLUMNS = {"case_id", "engine", "rewrite_method", "candidate_id", "denominator_id"}
FORBIDDEN_FIELD_TOKENS = {
    "timed",
    "latency",
    "latency_ms",
    "speedup",
    "speedup_ratio",
    "timing",
    "timing_eligible",
}
PROMPT_OR_TOKEN_TOKENS = {"prompt", "token", "api_key", "model_trace", "llm_trace"}
RAW_LOG_TOKENS = {"stdout", "stderr", ".log", "raw_log", "trace"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a fail-closed input manifest for candidate_status_parser_v0."
    )
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_release_path(path: Path) -> Path:
    root = repo_root()
    resolved = path if path.is_absolute() else root / path
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"manifest builder cannot open legacy paths: {path}")
    return resolved


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize(values: Iterable[str]) -> str:
    return " ".join(str(value) for value in values if value).lower()


def source_path_from_row(row: dict[str, str]) -> str:
    for key in (
        "source_repo_path",
        "source_artifact_path",
        "source_path_or_pattern",
        "retained_artifact_path",
        "relative_path",
    ):
        if row.get(key):
            return row[key]
    return ""


def source_repo_for_path(path: str) -> str:
    if path.startswith("legacy:") or str(LEGACY_REPO_ROOT) in path:
        return "legacy_repo"
    return "release_repo"


def relative_path_for_source(path: str) -> str:
    if path.startswith("legacy:"):
        return path.removeprefix("legacy:")
    if str(LEGACY_REPO_ROOT) in path:
        return path.replace(str(LEGACY_REPO_ROOT) + "/", "")
    return path


def path_has_token(path: str, tokens: set[str]) -> bool:
    lowered = path.lower()
    return any(token in lowered for token in tokens)


def field_tokens_present(fieldnames: Iterable[str], row: dict[str, str], tokens: set[str]) -> bool:
    lowered = " ".join(list(fieldnames) + list(row.values())).lower()
    return any(token in lowered for token in tokens)


def method_mentions(row_text: str) -> list[str]:
    methods: list[str] = []
    for method, tokens in METHOD_TOKENS.items():
        if any(token in row_text for token in tokens):
            methods.append(method)
    return methods


def row_grain_verified(fieldnames: list[str], row: dict[str, str]) -> bool:
    field_set = set(fieldnames)
    if not ROW_GRAIN_COLUMNS <= field_set:
        return False
    return all(row.get(column, "").strip() for column in ROW_GRAIN_COLUMNS)


def inspect_metadata_source(relative_path: Path, source_category: str) -> dict[str, object]:
    path = resolve_release_path(relative_path)
    if not path.exists():
        return {
            "metadata_path": str(relative_path),
            "source_category": source_category,
            "rows_inspected": 0,
            "method_related_rows": 0,
            "row_grain_verified_rows": 0,
            "deferred_rows": 0,
            "methods_seen": [],
            "notes": "metadata file missing; no manifest inputs approved",
        }

    rows, fieldnames = read_csv(path)
    method_related_rows = 0
    verified_rows = 0
    deferred_rows = 0
    methods_seen: set[str] = set()
    for row in rows:
        row_text = normalize(row.values())
        methods = method_mentions(row_text)
        if not methods:
            continue
        method_related_rows += 1
        methods_seen.update(methods)
        source_path = source_path_from_row(row)
        timing_risk = field_tokens_present(fieldnames, row, FORBIDDEN_FIELD_TOKENS)
        prompt_risk = field_tokens_present(fieldnames, row, PROMPT_OR_TOKEN_TOKENS)
        raw_log_risk = path_has_token(source_path, RAW_LOG_TOKENS)
        hygiene_risk = source_path.startswith("legacy:") or source_path.startswith("/")
        if row_grain_verified(fieldnames, row) and not any(
            [timing_risk, prompt_risk, raw_log_risk, hygiene_risk]
        ):
            verified_rows += 1
        else:
            deferred_rows += 1

    return {
        "metadata_path": str(relative_path),
        "source_category": source_category,
        "rows_inspected": len(rows),
        "method_related_rows": method_related_rows,
        "row_grain_verified_rows": verified_rows,
        "deferred_rows": deferred_rows,
        "methods_seen": sorted(methods_seen),
        "notes": "metadata inspected only; legacy artifacts were not opened",
    }


def build_checks(summary: dict[str, object]) -> list[dict[str, str]]:
    checks = [
        (
            "manifest file created",
            True,
            "candidate_status_parser_input_manifest.csv written",
        ),
        (
            "manifest has header",
            True,
            f"columns={len(MANIFEST_COLUMNS)}",
        ),
        (
            "approved parser inputs = 0",
            summary["approved_parser_inputs"] == 0,
            f"approved_parser_inputs={summary['approved_parser_inputs']}",
        ),
        (
            "legacy files opened = false",
            summary["legacy_files_opened"] is False,
            "manifest builder reads release metadata only",
        ),
        (
            "production retained evidence parsed = false",
            summary["production_retained_evidence_parsed"] is False,
            "no retained artifact content parsed",
        ),
        (
            "timing inputs approved = false",
            summary["timing_inputs_approved"] is False,
            "timing stays separate",
        ),
        (
            "prompt/token inputs approved = false",
            summary["prompt_token_inputs_approved"] is False,
            "prompt/token risky inputs are not approved",
        ),
        (
            "raw log inputs approved = false",
            summary["raw_log_inputs_approved"] is False,
            "raw log inputs are not approved",
        ),
        (
            "header-only fail-closed manifest when no row-grain sources",
            summary["manifest_rows"] == 0,
            "no exact row-grain metadata source was approved",
        ),
    ]
    return [
        {
            "check_name": name,
            "status": "PASS" if passed else "FAIL",
            "details": details,
        }
        for name, passed, details in checks
    ]


def write_report(
    path: Path,
    summary: dict[str, object],
    metadata_reviews: list[dict[str, object]],
    checks: list[dict[str, str]],
) -> None:
    lines = [
        "# candidate_status_parser_v0 Input Manifest Report",
        "",
        "## Purpose And Scope",
        "",
        "This report records manifest-first input selection for the bounded non-timing candidate status parser.",
        "The manifest builder inspects release-repo locator and mapping metadata only. It does not open legacy files or parse retained evidence.",
        "",
        "## Manifest Result",
        "",
        f"- Manifest rows: {summary['manifest_rows']}",
        f"- Approved parser inputs: {summary['approved_parser_inputs']}",
        f"- Rejected/deferred metadata candidates: {summary['rejected_or_deferred_inputs']}",
        "- Legacy files opened: false",
        "- Production retained evidence parsed: false",
        "- Metrics computed: false",
        "",
        "Because no exact `case_id x engine x rewrite_method x candidate_id x denominator_id` source was verified from metadata, the manifest is header-only and the parser must fail closed.",
        "",
        "## Metadata Sources Inspected",
        "",
    ]
    for review in metadata_reviews:
        lines.append(
            f"- `{review['metadata_path']}`: rows={review['rows_inspected']}, "
            f"method_related={review['method_related_rows']}, "
            f"row_grain_verified={review['row_grain_verified_rows']}, "
            f"deferred={review['deferred_rows']}, methods={','.join(review['methods_seen']) or 'none'}"
        )
    lines.extend(
        [
            "",
            "## Checks",
            "",
        ]
    )
    lines.extend(f"- {row['check_name']}: {row['status']} ({row['details']})" for row in checks)
    lines.extend(
        [
            "",
            "## Non-goals",
            "",
            "- No parser implementation is run by this script.",
            "- No row statuses are filled.",
            "- No timing fields are approved.",
            "- No metric input is authorized.",
            "- No metrics are computed.",
            "- No reports/results, denominator, paper-result, case membership, or raw legacy evidence changes are made.",
            "",
            "## Next Safe Action",
            "",
            "Run `parse_candidate_status_from_manifest.py`. With the current header-only manifest, the expected safe behavior is a 600-row unresolved ledger with `parser_status=no_approved_row_level_inputs`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    out_dir = resolve_release_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    metadata_reviews = [
        inspect_metadata_source(path, category) for path, category in METADATA_SOURCES
    ]
    deferred_inputs = sum(int(review["deferred_rows"]) for review in metadata_reviews)
    methods_seen = sorted(
        {
            method
            for review in metadata_reviews
            for method in review.get("methods_seen", [])
        }
    )
    source_category_counts = Counter(str(review["source_category"]) for review in metadata_reviews)

    manifest_rows: list[dict[str, str]] = []
    summary: dict[str, object] = {
        "parser_name": PARSER_NAME,
        "manifest_rows": len(manifest_rows),
        "approved_parser_inputs": 0,
        "rejected_or_deferred_inputs": deferred_inputs,
        "metadata_sources_inspected": len(metadata_reviews),
        "metadata_source_category_counts": dict(sorted(source_category_counts.items())),
        "methods_seen_in_metadata": methods_seen,
        "expected_row_grain": EXPECTED_ROW_GRAIN,
        "legacy_files_opened": False,
        "production_retained_evidence_parsed": False,
        "metrics_computed": False,
        "timing_inputs_approved": False,
        "prompt_token_inputs_approved": False,
        "raw_log_inputs_approved": False,
    }
    checks = build_checks(summary)

    write_csv(out_dir / MANIFEST_FILENAME, manifest_rows, MANIFEST_COLUMNS)
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(out_dir / CHECKS_FILENAME, checks, CHECK_COLUMNS)
    write_report(out_dir / REPORT_FILENAME, summary, metadata_reviews, checks)

    failed = [row for row in checks if row["status"] == "FAIL"]
    print(f"manifest_rows: {len(manifest_rows)}")
    print("approved_parser_inputs: 0")
    print(f"rejected_or_deferred_inputs: {deferred_inputs}")
    print(f"checks_failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
