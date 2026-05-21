"""Human-readable local user-run output schema descriptions."""

from __future__ import annotations

from .tag_slices import TAG_SLICE_FIELDS
from .user_run_schema import FAILURE_FIELDS, LEDGER_FIELDS, SELECTED_CASE_FIELDS


def output_schema_text() -> str:
    """Return a concise local-only schema description for user-run outputs."""

    sections = [
        "# SQL-RewriteBench User-Run Output Schema",
        "",
        "These files are local diagnostics only.",
        "They are not official metrics, not paper tables, not retained evidence, "
        "not reports/results updates, and not leaderboard input.",
        "",
        "## selected_cases.csv",
        "",
        "Purpose: selected Common-core case-engine rows resolved from case-set CSV files.",
        _fields_line(SELECTED_CASE_FIELDS),
        "",
        "## ledger.csv",
        "",
        "Purpose: one local diagnostic row per selected case-engine row.",
        "Key fields include case identity, adapter status, candidate capture, "
        "candidate preflight, optional execution/checker status, failure bucket, "
        "and local-only boundary flags.",
        _fields_line(LEDGER_FIELDS),
        "",
        "## failures.csv",
        "",
        "Purpose: subset of ledger rows whose local failure bucket is not `none`.",
        _fields_line(FAILURE_FIELDS),
        "",
        "## summary.json",
        "",
        "Purpose: local run counts and boundary flags for the basic user run.",
        "Key fields: run id, dry-run flag, selected rows, adapter-invoked rows, "
        "candidate-generated rows, local execution/checker counts when enabled, "
        "and no-report/no-result/no-leaderboard flags.",
        "",
        "## quality_summary.json",
        "",
        "Purpose: denominator-aware local diagnostic funnel summary built from "
        "`ledger.csv`.",
        "Key groups: scope, funnel_counts, failure_bucket_counts, status_counts, "
        "interpretation_boundary, derivation_notes.",
        "",
        "## quality_report.md",
        "",
        "Purpose: human-readable local diagnostic report mirroring "
        "`quality_summary.json`.",
        "Sections: Scope, Denominator-aware funnel, Failure buckets, Status counts, "
        "Interpretation boundary, Deferred outputs.",
        "",
        "## tag_slices.csv",
        "",
        "Purpose: local diagnostic slices by retained manifest/taxonomy tags.",
        "Tags are loaded from package metadata, not inferred from SQL text.",
        _fields_line(TAG_SLICE_FIELDS),
        "",
        "## Boundary",
        "",
        "- Local diagnostic only.",
        "- No official metrics.",
        "- No paper table rendering.",
        "- No reports/results updates.",
        "- No retained evidence promotion.",
        "- No leaderboard input.",
        "",
    ]
    return "\n".join(sections)


def _fields_line(fields: list[str]) -> str:
    return "Fields: " + ", ".join(f"`{field}`" for field in fields) + "."
