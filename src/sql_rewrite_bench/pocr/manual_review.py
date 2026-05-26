"""Manual-review queue builders for diagnostic POCR artifacts.

These helpers only build CSV-ready review rows. They do not update annotation
JSONL, Stage B diagnostics, official POCR, or paper-facing metrics.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from sql_rewrite_bench.pocr.evidence_ref_linter import EvidenceRefLintRow
from sql_rewrite_bench.pocr.operation_evidence_policy import TransformationStageBValidationResult
from sql_rewrite_bench.pocr.retry_planner import RetryPlanRow


@dataclass(frozen=True)
class ManualReviewRow:
    review_id: str
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    atom_id: str
    atom_type: str
    stage_a_status: str
    stage_b_status: str
    evidence_refs: str
    review_reason: str
    suggested_review_action: str
    diagnostic_only: bool
    official_pocr_computed: bool


def manual_review_fields() -> list[str]:
    return [
        "review_id",
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "atom_id",
        "atom_type",
        "stage_a_status",
        "stage_b_status",
        "evidence_refs",
        "review_reason",
        "suggested_review_action",
        "diagnostic_only",
        "official_pocr_computed",
    ]


def manual_review_rows_to_csv_rows(rows: Iterable[ManualReviewRow]) -> list[dict[str, str]]:
    return [
        {
            "review_id": row.review_id,
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "atom_id": row.atom_id,
            "atom_type": row.atom_type,
            "stage_a_status": row.stage_a_status,
            "stage_b_status": row.stage_b_status,
            "evidence_refs": row.evidence_refs,
            "review_reason": row.review_reason,
            "suggested_review_action": row.suggested_review_action,
            "diagnostic_only": str(row.diagnostic_only).lower(),
            "official_pocr_computed": str(row.official_pocr_computed).lower(),
        }
        for row in rows
    ]


def review_rows_for_stage_b(result: TransformationStageBValidationResult) -> list[ManualReviewRow]:
    rows: list[ManualReviewRow] = []
    for atom in result.atom_results:
        refs = tuple(atom.evidence_refs)
        if atom.atom_type == "operation_atom" and atom.evidence_status == "transformation_supported":
            rows.append(
                _row(
                    case_id=result.case_id or "",
                    pool=result.pool or "",
                    engine=result.engine,
                    method_id=result.method_id,
                    route_id=result.route_id,
                    atom_id=atom.atom_id,
                    atom_type=str(atom.atom_type),
                    stage_a_status=atom.observed_status,
                    stage_b_status=atom.evidence_status,
                    evidence_refs=refs,
                    review_reason="transformation_supported_atom",
                    suggested_review_action="inspect_candidate_source_diff",
                )
            )
        elif atom.atom_type == "operation_atom" and _possible_under_accept(atom.observed_status, atom.evidence_status, refs):
            rows.append(
                _row(
                    case_id=result.case_id or "",
                    pool=result.pool or "",
                    engine=result.engine,
                    method_id=result.method_id,
                    route_id=result.route_id,
                    atom_id=atom.atom_id,
                    atom_type=str(atom.atom_type),
                    stage_a_status=atom.observed_status,
                    stage_b_status=atom.evidence_status,
                    evidence_refs=refs,
                    review_reason="possible_under_accept",
                    suggested_review_action="inspect_candidate_source_diff",
                )
            )
    return rows


def review_rows_for_retry_plan(rows: Iterable[RetryPlanRow]) -> list[ManualReviewRow]:
    review_rows: list[ManualReviewRow] = []
    for row in rows:
        if not row.retry_eligible:
            continue
        review_rows.append(
            _row(
                case_id=row.case_id,
                pool=row.pool,
                engine=row.engine,
                method_id=row.method_id,
                route_id=row.route_id,
                atom_id="",
                atom_type="",
                stage_a_status=row.current_status,
                stage_b_status="not_run",
                evidence_refs=(),
                review_reason=row.current_status,
                suggested_review_action="retry_annotation",
            )
        )
    return review_rows


def review_rows_for_lint(rows: Iterable[EvidenceRefLintRow], *, engine: str, method_id: str, route_id: str) -> list[ManualReviewRow]:
    review_rows: list[ManualReviewRow] = []
    for row in rows:
        if row.severity == "info":
            action = "mark_manual_note_only"
        elif row.issue_type in {"missing_evidence_refs", "unsupported_prefix"}:
            action = "inspect_prompt_output"
        else:
            action = "inspect_candidate_source_diff"
        review_rows.append(
            _row(
                case_id=row.case_id,
                pool=row.pool,
                engine=engine,
                method_id=method_id,
                route_id=route_id,
                atom_id=row.atom_id,
                atom_type=row.atom_type,
                stage_a_status=row.observed_status,
                stage_b_status="lint_only",
                evidence_refs=(row.evidence_ref,) if row.evidence_ref else (),
                review_reason=f"evidence_ref_linter:{row.issue_type}:{row.severity}",
                suggested_review_action=action,
            )
        )
    return review_rows


def dedupe_manual_review_rows(rows: Iterable[ManualReviewRow]) -> list[ManualReviewRow]:
    deduped: dict[str, ManualReviewRow] = {}
    for row in rows:
        deduped[row.review_id] = row
    return [deduped[key] for key in sorted(deduped)]


def write_manual_review_csv(path: Path, rows: Iterable[ManualReviewRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=manual_review_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(manual_review_rows_to_csv_rows(rows))


def _possible_under_accept(observed_status: str, stage_b_status: str, evidence_refs: tuple[str, ...]) -> bool:
    return (
        observed_status == "implemented"
        and stage_b_status in {"presence_only", "insufficient_transformation_evidence"}
        and "source_candidate_diff:changed" in evidence_refs
        and any(ref.startswith(("candidate_sql_span:", "positive_sql_span:", "candidate_token_span:")) for ref in evidence_refs)
    )


def _row(
    *,
    case_id: str,
    pool: str,
    engine: str,
    method_id: str,
    route_id: str,
    atom_id: str,
    atom_type: str,
    stage_a_status: str,
    stage_b_status: str,
    evidence_refs: tuple[str, ...],
    review_reason: str,
    suggested_review_action: str,
) -> ManualReviewRow:
    key = "|".join(
        [
            case_id,
            engine,
            method_id,
            route_id,
            atom_id,
            stage_a_status,
            stage_b_status,
            review_reason,
            " ".join(evidence_refs),
        ]
    )
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return ManualReviewRow(
        review_id=f"pocr_review_{digest}",
        case_id=case_id,
        pool=pool,
        engine=engine,
        method_id=method_id,
        route_id=route_id,
        atom_id=atom_id,
        atom_type=atom_type,
        stage_a_status=stage_a_status,
        stage_b_status=stage_b_status,
        evidence_refs=" | ".join(evidence_refs),
        review_reason=review_reason,
        suggested_review_action=suggested_review_action,
        diagnostic_only=True,
        official_pocr_computed=False,
    )
