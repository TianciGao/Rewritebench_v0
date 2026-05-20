"""Local quality summaries for user-entry diagnostic runs."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_NON_DB,
    CHECKER_STATUS_NOT_ENABLED,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_NON_DB,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_MISMATCH,
    FAILURE_NO_CANDIDATE_SQL,
    SOURCE_LIKE_STATUS_SOURCE_LIKE,
    TIMED_STATUS_NON_DB,
)


def build_quality_summary(
    ledger_rows: list[dict[str, object]],
    run_config: dict[str, object] | None = None,
    *,
    tag_slices_included: bool = False,
) -> dict[str, object]:
    """Build a denominator-aware local diagnostic summary from ledger rows."""

    config = run_config or {}
    failure_counts = Counter(_text(row.get("failure_bucket")) for row in ledger_rows)
    summary = {
        "schema_version": "local_quality_report_v0",
        "scope": {
            "run_id": _text(config.get("run_id")),
            "case_set": _text(config.get("case_set")),
            "engine": _text(config.get("engine")),
            "local_diagnostic_only": True,
            "official_metrics": False,
            "paper_results_updated": False,
            "retained_evidence_input": False,
            "leaderboard_created": False,
        },
        "funnel_counts": {
            "selected_rows": _count_true(ledger_rows, "selected"),
            "adapter_invoked_rows": _count_true(ledger_rows, "adapter_invoked"),
            "candidate_generated_rows": _count_true(ledger_rows, "candidate_generated"),
            "candidate_missing_rows": _candidate_missing_rows(ledger_rows),
            "candidate_preflight_passed_rows": _candidate_preflight_passed_rows(
                ledger_rows
            ),
            "candidate_preflight_failed_rows": _candidate_preflight_failed_rows(
                ledger_rows
            ),
            "db_execution_attempted_rows": _db_execution_attempted_rows(ledger_rows),
            "source_executable_rows": _count_equal(
                ledger_rows, "source_execution_status", EXECUTION_STATUS_SOURCE_SUCCESS
            ),
            "candidate_executable_rows": _count_equal(
                ledger_rows,
                "candidate_execution_status",
                EXECUTION_STATUS_CANDIDATE_SUCCESS,
            ),
            "checker_attempted_rows": _checker_attempted_rows(ledger_rows),
            "exact_rows": _count_equal(ledger_rows, "exact_status", EXACT_STATUS_EXACT),
            "mismatch_rows": _mismatch_rows(ledger_rows),
            "source_like_rows": _count_equal(
                ledger_rows, "source_like_status", SOURCE_LIKE_STATUS_SOURCE_LIKE
            ),
            "timed_rows": _timed_rows(ledger_rows),
        },
        "failure_bucket_counts": dict(sorted(failure_counts.items())),
        "status_counts": {
            "candidate_preflight_status": _counter(ledger_rows, "candidate_preflight_status"),
            "execution_status": _counter(ledger_rows, "execution_status"),
            "checker_status": _counter(ledger_rows, "checker_status"),
            "exact_status": _counter(ledger_rows, "exact_status"),
            "timed_status": _counter(ledger_rows, "timed_status"),
            "source_like_status": _counter(ledger_rows, "source_like_status"),
        },
        "interpretation_boundary": {
            "quality_report_is_official_metric": False,
            "tag_slices_included": tag_slices_included,
            "timing_included": False,
            "paper_tables_rendered": False,
            "global_leaderboard": False,
        },
        "derivation_notes": {
            "db_execution_attempted_rows": (
                "Counted only when execution_status is neither non-DB nor not-enabled."
            ),
            "checker_attempted_rows": (
                "Counted only when checker_status is neither non-DB nor not-enabled."
            ),
            "timed_rows": (
                "Counted only when timed_status is populated and not the non-DB "
                "placeholder; U4 does not collect timing."
            ),
            "local_only_boundary": (
                "This summary is local diagnostic output, not official metrics, "
                "paper tables, retained evidence, reports/results, or leaderboard data."
            ),
        },
    }
    return summary


def write_quality_summary(summary: dict[str, object], output_path: Path) -> None:
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_quality_report(summary: dict[str, object], output_path: Path) -> None:
    funnel = summary["funnel_counts"]
    failure_counts = summary["failure_bucket_counts"]
    status_counts = summary["status_counts"]
    scope = summary["scope"]

    lines = [
        "# Local Quality Report",
        "",
        "This is local diagnostic output only.",
        "It is not official metrics, not a paper table, not retained evidence, "
        "not a reports/results update, and not a leaderboard.",
        "",
        "## Scope",
        "",
        f"- Run id: `{scope.get('run_id', '')}`",
        f"- Case set: `{scope.get('case_set', '')}`",
        f"- Engine: `{scope.get('engine', '')}`",
        "- Local diagnostic only: `true`",
        "- Official metrics: `false`",
        "- Paper results updated: `false`",
        "- Retained evidence input: `false`",
        "- Leaderboard created: `false`",
        "",
        "## Denominator-aware funnel",
        "",
    ]
    for key, value in funnel.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Failure buckets", ""])
    if failure_counts:
        for bucket, count in failure_counts.items():
            lines.append(f"- {bucket}: {count}")
    else:
        lines.append("- none: 0")

    lines.extend(["", "## Status counts", ""])
    for family, counts in status_counts.items():
        lines.append(f"- {family}:")
        if counts:
            for status, count in counts.items():
                lines.append(f"  - {status}: {count}")
        else:
            lines.append("  - none: 0")

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- This report summarizes local user-run diagnostics only.",
            "- It does not compute official metrics.",
            "- It is not a paper table.",
            "- It does not update `reports/` or `results/`.",
            "- It is not retained evidence.",
            "- It is not a leaderboard.",
            "",
            "## Deferred outputs",
            "",
            _tag_slice_report_line(summary),
            "- Timing and speedup are not included.",
            "- Official metrics remain unauthorized here.",
            "- Paper table rendering remains deferred.",
            "- Full paper reproduction remains deferred.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _tag_slice_report_line(summary: dict[str, object]) -> str:
    boundary = summary.get("interpretation_boundary", {})
    if isinstance(boundary, dict) and boundary.get("tag_slices_included") is True:
        return "- Tag-aware slices are available as local diagnostics in `tag_slices.csv`."
    return "- Tag-aware slices are not included."


def _text(value: object) -> str:
    return "" if value is None else str(value)


def _is_true_like(value: object) -> bool:
    return _text(value).strip().lower() in {"true", "1", "yes"}


def _count_true(rows: list[dict[str, object]], field: str) -> int:
    return sum(_is_true_like(row.get(field)) for row in rows)


def _count_equal(rows: list[dict[str, object]], field: str, expected: str) -> int:
    return sum(_text(row.get(field)) == expected for row in rows)


def _counter(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    counts = Counter(_text(row.get(field)) for row in rows)
    return dict(sorted(counts.items()))


def _candidate_missing_rows(rows: list[dict[str, object]]) -> int:
    return sum(
        _text(row.get("failure_bucket")) == FAILURE_NO_CANDIDATE_SQL
        or (
            not _is_true_like(row.get("candidate_generated"))
            and _text(row.get("candidate_sql_path")) == ""
            and _text(row.get("adapter_invoked")) == "true"
        )
        for row in rows
    )


def _candidate_preflight_passed_rows(rows: list[dict[str, object]]) -> int:
    return sum(
        _text(row.get("candidate_preflight_status")) == CANDIDATE_PREFLIGHT_STATUS_PASSED
        or _is_true_like(row.get("candidate_preflight_passed"))
        for row in rows
    )


def _candidate_preflight_failed_rows(rows: list[dict[str, object]]) -> int:
    return sum(
        _text(row.get("candidate_preflight_status")) == CANDIDATE_PREFLIGHT_STATUS_FAILED
        or _text(row.get("failure_bucket")) == FAILURE_CANDIDATE_PREFLIGHT_FAILED
        for row in rows
    )


def _db_execution_attempted_rows(rows: list[dict[str, object]]) -> int:
    not_attempted = {EXECUTION_STATUS_NON_DB, EXECUTION_STATUS_NOT_ENABLED, ""}
    return sum(_text(row.get("execution_status")) not in not_attempted for row in rows)


def _checker_attempted_rows(rows: list[dict[str, object]]) -> int:
    not_attempted = {CHECKER_STATUS_NON_DB, CHECKER_STATUS_NOT_ENABLED, ""}
    return sum(_text(row.get("checker_status")) not in not_attempted for row in rows)


def _mismatch_rows(rows: list[dict[str, object]]) -> int:
    return sum(
        _text(row.get("exact_status")) == EXACT_STATUS_MISMATCH
        or _text(row.get("failure_bucket")) == FAILURE_MISMATCH
        for row in rows
    )


def _timed_rows(rows: list[dict[str, object]]) -> int:
    return sum(
        bool(_text(row.get("timed_status")))
        and _text(row.get("timed_status")) != TIMED_STATUS_NON_DB
        for row in rows
    )
