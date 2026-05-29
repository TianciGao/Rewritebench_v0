"""Deterministic retry planning for fail-closed POCR annotation rows.

This module is offline-only. It reads checkpoint/manifest rows and produces a
reviewable retry plan. It never calls a provider and never mutates annotation
JSONL, diagnostic rows, or official metrics.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_RETRY_ELIGIBLE_STATUSES = frozenset({"malformed_json", "timeout", "provider_call_failed"})
DEFAULT_NON_RETRY_STATUSES = frozenset(
    {
        "schema_valid",
        "route_mismatch",
        "candidate_mismatch",
        "skills_contract_mismatch",
        "duplicate_annotation",
        "duplicate_annotation_rows",
        "missing_candidate",
        "skipped_no_candidate",
        "skipped_unsupported_engine",
    }
)


@dataclass(frozen=True)
class RetryPlanRow:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_sha256: str
    current_status: str
    retry_eligible: bool
    retry_reason: str
    retry_requires_explicit_flag: bool
    prior_attempt_count: int
    recommendation: str


def retry_plan_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_sha256",
        "current_status",
        "retry_eligible",
        "retry_reason",
        "retry_requires_explicit_flag",
        "prior_attempt_count",
        "recommendation",
    ]


def retry_plan_rows_to_csv_rows(rows: Iterable[RetryPlanRow]) -> list[dict[str, str]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "candidate_sha256": row.candidate_sha256,
            "current_status": row.current_status,
            "retry_eligible": str(row.retry_eligible).lower(),
            "retry_reason": row.retry_reason,
            "retry_requires_explicit_flag": str(row.retry_requires_explicit_flag).lower(),
            "prior_attempt_count": str(row.prior_attempt_count),
            "recommendation": row.recommendation,
        }
        for row in rows
    ]


def plan_retries_from_manifest_rows(
    manifest_rows: Iterable[Mapping[str, str]],
    *,
    allowed_retry_statuses: Iterable[str] | None = None,
) -> list[RetryPlanRow]:
    """Build a retry plan from checkpointed annotation manifest rows."""

    allowed = frozenset(allowed_retry_statuses or DEFAULT_RETRY_ELIGIBLE_STATUSES)
    return [_plan_one(row, allowed) for row in manifest_rows]


def plan_retries_from_manifest_csv(
    path: Path,
    *,
    allowed_retry_statuses: Iterable[str] | None = None,
) -> list[RetryPlanRow]:
    with path.open(newline="", encoding="utf-8") as handle:
        return plan_retries_from_manifest_rows(csv.DictReader(handle), allowed_retry_statuses=allowed_retry_statuses)


def plan_retries_from_checkpoint_state(
    checkpoint_state_json: Path,
    *,
    allowed_retry_statuses: Iterable[str] | None = None,
) -> list[RetryPlanRow]:
    """Build a retry plan from a checkpoint state if row-level state exists.

    Current checkpoint states may contain only aggregate counts. In that case
    there is no safe row identity to retry, so this returns an empty plan rather
    than fabricating rows.
    """

    raw = json.loads(checkpoint_state_json.read_text(encoding="utf-8"))
    row_items: list[Mapping[str, str]] = []
    if isinstance(raw, dict) and isinstance(raw.get("rows"), list):
        row_items = [row for row in raw["rows"] if isinstance(row, Mapping)]  # type: ignore[list-item]
    elif isinstance(raw, dict) and isinstance(raw.get("row_statuses"), Mapping):
        for case_id, status in raw["row_statuses"].items():
            if isinstance(status, Mapping):
                merged = {"case_id": str(case_id), **{str(k): str(v) for k, v in status.items()}}
            else:
                merged = {"case_id": str(case_id), "annotation_status": str(status)}
            row_items.append(merged)
    return plan_retries_from_manifest_rows(row_items, allowed_retry_statuses=allowed_retry_statuses)


def write_retry_plan_csv(path: Path, rows: Iterable[RetryPlanRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=retry_plan_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(retry_plan_rows_to_csv_rows(rows))


def summarize_retry_plan(rows: Iterable[RetryPlanRow]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        counter["total_rows"] += 1
        if row.retry_eligible:
            counter["retry_eligible_rows"] += 1
        counter[f"status_{row.current_status or 'missing'}"] += 1
    return dict(counter)


def _plan_one(row: Mapping[str, str], allowed_retry_statuses: frozenset[str]) -> RetryPlanRow:
    status = _status(row)
    eligible = status in allowed_retry_statuses
    if eligible:
        reason = f"{status} is fail-closed and retry-eligible by policy"
        recommendation = _eligible_recommendation(status)
    elif status in DEFAULT_NON_RETRY_STATUSES:
        reason = f"{status} is non-retry by policy"
        recommendation = _non_retry_recommendation(status)
    else:
        reason = "status is not in the retry allowlist"
        recommendation = "manual_review_before_retry"
    return RetryPlanRow(
        case_id=str(row.get("case_id", "")),
        pool=str(row.get("pool", "")),
        engine=str(row.get("engine", "")),
        method_id=str(row.get("method_id", "")),
        route_id=str(row.get("route_id", "")),
        candidate_sha256=str(row.get("candidate_sha256", "")),
        current_status=status,
        retry_eligible=eligible,
        retry_reason=reason,
        retry_requires_explicit_flag=eligible,
        prior_attempt_count=_prior_attempt_count(row),
        recommendation=recommendation,
    )


def _status(row: Mapping[str, str]) -> str:
    for field in ("annotation_status", "current_status", "call_status", "validation_status"):
        value = str(row.get(field, "")).strip()
        if value:
            return value
    return ""


def _prior_attempt_count(row: Mapping[str, str]) -> int:
    for field in ("prior_attempt_count", "attempt_count", "call_attempt_count"):
        value = str(row.get(field, "")).strip()
        if value.isdigit():
            return int(value)
    status = _status(row)
    if status in {"", "not_run", "pending", "skipped_no_candidate", "skipped_unsupported_engine"}:
        return 0
    return 1


def _eligible_recommendation(status: str) -> str:
    if status == "malformed_json":
        return "retry_annotation_with_json_guard_after_review"
    if status == "timeout":
        return "retry_annotation_with_timeout_budget_after_review"
    if status == "provider_call_failed":
        return "retry_annotation_after_provider_error_review"
    return "retry_annotation_after_explicit_review"


def _non_retry_recommendation(status: str) -> str:
    if status == "schema_valid":
        return "do_not_retry_successful_annotation"
    if status in {"candidate_mismatch", "route_mismatch", "skills_contract_mismatch"}:
        return "fix_binding_before_retry"
    if status in {"duplicate_annotation", "duplicate_annotation_rows"}:
        return "deduplicate_before_retry"
    return "keep_fail_closed"
