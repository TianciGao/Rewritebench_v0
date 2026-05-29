"""Tag-aware local diagnostic slices for user-entry runs."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .case_package_resolver import ResolvedCasePackage
from .user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_CONFIG_MISSING,
    CHECKER_STATUS_FAILED,
    CHECKER_STATUS_INTERNAL_ERROR,
    CHECKER_STATUS_NON_DB,
    CHECKER_STATUS_NORMALIZATION_MISSING,
    CHECKER_STATUS_NOT_ENABLED,
    CHECKER_STATUS_TIMEOUT,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_INTERNAL_ERROR,
    EXECUTION_STATUS_NON_DB,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_TIMEOUT,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_CHECKER_CONFIG_MISSING,
    FAILURE_CHECKER_FAILED,
    FAILURE_CHECKER_TIMEOUT,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_MISMATCH,
    FAILURE_SOURCE_EXECUTION_FAILED,
    SOURCE_LIKE_STATUS_SOURCE_LIKE,
    TIMED_STATUS_NON_DB,
)


TAG_SLICE_FIELDS = [
    "axis",
    "tag",
    "selected_rows",
    "candidate_generated_rows",
    "candidate_preflight_passed_rows",
    "candidate_preflight_failed_rows",
    "db_execution_attempted_rows",
    "candidate_executed_rows",
    "checker_attempted_rows",
    "exact_rows",
    "mismatch_rows",
    "execution_failed_rows",
    "checker_failed_rows",
    "source_like_rows",
    "timed_rows",
    "local_diagnostic_only",
    "official_metric",
    "leaderboard_input",
    "claim_boundary",
    "notes",
]

SUPPORTED_AXIS_KEYS = {
    "sql_feature": ("sql_feature", "sql_features"),
    "rewrite_opportunity": ("rewrite_opportunity", "rewrite_opportunities"),
    "plan_operator": ("plan_operator", "plan_operators"),
    "workload_realism": ("workload_realism", "workload_realism_tags"),
    "portability_risk": ("portability_risk", "portability", "portability_focus"),
}

CLAIM_BOUNDARY = (
    "local diagnostic tag slice only; not a score, not official metrics, "
    "not paper evidence, not leaderboard input"
)


@dataclass(frozen=True)
class RetainedTag:
    axis: str
    tag: str
    source: str


def load_retained_tags(resolved_package: ResolvedCasePackage) -> list[RetainedTag]:
    """Load retained taxonomy tags from a resolved case package manifest."""

    return load_retained_tags_from_taxonomy(resolved_package.manifest_taxonomy)


def load_retained_tags_from_taxonomy(taxonomy: dict[str, Any]) -> list[RetainedTag]:
    """Map clearly retained taxonomy fields to supported diagnostic axes."""

    tags: list[RetainedTag] = []
    seen: set[tuple[str, str]] = set()
    for axis, source_keys in SUPPORTED_AXIS_KEYS.items():
        for source_key in source_keys:
            if source_key not in taxonomy:
                continue
            for tag in _extract_string_values(taxonomy[source_key]):
                normalized = tag.strip()
                if not normalized:
                    continue
                key = (axis, normalized)
                if key in seen:
                    continue
                seen.add(key)
                tags.append(
                    RetainedTag(
                        axis=axis,
                        tag=normalized,
                        source=f"manifest.taxonomy.{source_key}",
                    )
                )
    return sorted(tags, key=lambda item: (item.axis, item.tag))


def build_tag_slice_rows(
    ledger_rows: list[dict[str, object]],
    resolved_packages: list[ResolvedCasePackage],
) -> list[dict[str, object]]:
    """Build denominator-aware local diagnostic counts by retained manifest tag."""

    aggregates: dict[tuple[str, str], dict[str, object]] = {}
    for ledger, resolved in zip(ledger_rows, resolved_packages, strict=True):
        for retained_tag in load_retained_tags(resolved):
            key = (retained_tag.axis, retained_tag.tag)
            aggregate = aggregates.setdefault(
                key,
                _empty_slice(axis=retained_tag.axis, tag=retained_tag.tag),
            )
            _add_row_counts(aggregate, ledger)

    return [
        {field: aggregate[field] for field in TAG_SLICE_FIELDS}
        for aggregate in sorted(aggregates.values(), key=lambda row: (row["axis"], row["tag"]))
    ]


def write_tag_slices(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TAG_SLICE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _extract_string_values(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_extract_string_values(item))
        return values
    if isinstance(value, dict):
        values = []
        for nested in value.values():
            values.extend(_extract_string_values(nested))
        return values
    return []


def _empty_slice(*, axis: str, tag: str) -> dict[str, object]:
    row: dict[str, object] = {
        "axis": axis,
        "tag": tag,
        "local_diagnostic_only": "true",
        "official_metric": "false",
        "leaderboard_input": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": "tags loaded from retained manifest taxonomy; counts are selected rows",
    }
    for field in TAG_SLICE_FIELDS:
        if field not in row:
            row[field] = 0
    return row


def _add_row_counts(aggregate: dict[str, object], ledger: dict[str, object]) -> None:
    aggregate["selected_rows"] += _as_int(_is_true_like(ledger.get("selected")))
    aggregate["candidate_generated_rows"] += _as_int(
        _is_true_like(ledger.get("candidate_generated"))
    )
    aggregate["candidate_preflight_passed_rows"] += _as_int(
        _text(ledger.get("candidate_preflight_status")) == CANDIDATE_PREFLIGHT_STATUS_PASSED
        or _is_true_like(ledger.get("candidate_preflight_passed"))
    )
    aggregate["candidate_preflight_failed_rows"] += _as_int(
        _text(ledger.get("candidate_preflight_status")) == CANDIDATE_PREFLIGHT_STATUS_FAILED
        or _text(ledger.get("failure_bucket")) == FAILURE_CANDIDATE_PREFLIGHT_FAILED
    )
    aggregate["db_execution_attempted_rows"] += _as_int(_db_execution_attempted(ledger))
    aggregate["candidate_executed_rows"] += _as_int(
        _text(ledger.get("candidate_execution_status")) == EXECUTION_STATUS_CANDIDATE_SUCCESS
    )
    aggregate["checker_attempted_rows"] += _as_int(_checker_attempted(ledger))
    aggregate["exact_rows"] += _as_int(_text(ledger.get("exact_status")) == EXACT_STATUS_EXACT)
    aggregate["mismatch_rows"] += _as_int(
        _text(ledger.get("exact_status")) == EXACT_STATUS_MISMATCH
        or _text(ledger.get("failure_bucket")) == FAILURE_MISMATCH
    )
    aggregate["execution_failed_rows"] += _as_int(_execution_failed(ledger))
    aggregate["checker_failed_rows"] += _as_int(_checker_failed(ledger))
    aggregate["source_like_rows"] += _as_int(
        _text(ledger.get("source_like_status")) == SOURCE_LIKE_STATUS_SOURCE_LIKE
    )
    aggregate["timed_rows"] += _as_int(
        bool(_text(ledger.get("timed_status")))
        and _text(ledger.get("timed_status")) != TIMED_STATUS_NON_DB
    )


def _db_execution_attempted(ledger: dict[str, object]) -> bool:
    return _text(ledger.get("execution_status")) not in {
        "",
        EXECUTION_STATUS_NON_DB,
        EXECUTION_STATUS_NOT_ENABLED,
    }


def _checker_attempted(ledger: dict[str, object]) -> bool:
    return _text(ledger.get("checker_status")) not in {
        "",
        CHECKER_STATUS_NON_DB,
        CHECKER_STATUS_NOT_ENABLED,
    }


def _execution_failed(ledger: dict[str, object]) -> bool:
    return _text(ledger.get("failure_bucket")) in {
        FAILURE_SOURCE_EXECUTION_FAILED,
        FAILURE_CANDIDATE_EXECUTION_FAILED,
        FAILURE_CROSS_DIALECT_BACKEND_MISSING,
        FAILURE_EXECUTION_TIMEOUT,
    } or _text(ledger.get("execution_status")) in {
        EXECUTION_STATUS_SOURCE_FAILED,
        EXECUTION_STATUS_CANDIDATE_FAILED,
        EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
        EXECUTION_STATUS_TIMEOUT,
        EXECUTION_STATUS_INTERNAL_ERROR,
    }


def _checker_failed(ledger: dict[str, object]) -> bool:
    return _text(ledger.get("failure_bucket")) in {
        FAILURE_CHECKER_CONFIG_MISSING,
        FAILURE_CHECKER_FAILED,
        FAILURE_CHECKER_TIMEOUT,
    } or _text(ledger.get("checker_status")) in {
        CHECKER_STATUS_CONFIG_MISSING,
        CHECKER_STATUS_FAILED,
        CHECKER_STATUS_TIMEOUT,
        CHECKER_STATUS_NORMALIZATION_MISSING,
        CHECKER_STATUS_INTERNAL_ERROR,
    }


def _text(value: object) -> str:
    return "" if value is None else str(value)


def _is_true_like(value: object) -> bool:
    return _text(value).strip().lower() in {"true", "1", "yes"}


def _as_int(value: bool) -> int:
    return 1 if value else 0
