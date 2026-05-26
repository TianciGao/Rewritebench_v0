"""Quality linter for POCR Stage A evidence refs.

The linter reports evidence-ref quality issues before Stage B interpretation.
It does not compute POCR, override Stage B, or change diagnostic results.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, annotation_from_mapping

SUPPORTED_EVIDENCE_REF_PREFIXES = (
    "candidate_sql_span:",
    "source_sql_span:",
    "positive_sql_span:",
    "candidate_token_span:",
    "source_candidate_diff:changed",
)
SPAN_PREFIXES = ("candidate_sql_span:", "source_sql_span:", "positive_sql_span:", "candidate_token_span:")
MAX_EVIDENCE_REF_LENGTH = 500


@dataclass(frozen=True)
class EvidenceRefLintRow:
    case_id: str
    pool: str
    atom_id: str
    atom_type: str
    observed_status: str
    evidence_ref: str
    lint_status: str
    issue_type: str
    severity: str
    recommendation: str


def evidence_ref_lint_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "atom_id",
        "atom_type",
        "observed_status",
        "evidence_ref",
        "lint_status",
        "issue_type",
        "severity",
        "recommendation",
    ]


def lint_rows_to_csv_rows(rows: Iterable[EvidenceRefLintRow]) -> list[dict[str, str]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "atom_id": row.atom_id,
            "atom_type": row.atom_type,
            "observed_status": row.observed_status,
            "evidence_ref": row.evidence_ref,
            "lint_status": row.lint_status,
            "issue_type": row.issue_type,
            "severity": row.severity,
            "recommendation": row.recommendation,
        }
        for row in rows
    ]


def lint_annotation(annotation: CandidateAnnotation | Mapping[str, object]) -> list[EvidenceRefLintRow]:
    if not isinstance(annotation, CandidateAnnotation):
        annotation = annotation_from_mapping(annotation)
    rows: list[EvidenceRefLintRow] = []
    for atom in annotation.atoms:
        evidence_refs = tuple(atom.evidence_refs)
        if atom.observed_status == "implemented" and not evidence_refs:
            rows.append(
                _row(
                    annotation,
                    atom.atom_id,
                    atom.atom_type,
                    atom.observed_status,
                    "",
                    "missing_evidence_refs",
                    "error",
                    "add explicit evidence refs or mark the atom unclear/not_implemented",
                )
            )
        seen: set[str] = set()
        for evidence_ref in evidence_refs:
            if evidence_ref in seen:
                rows.append(
                    _row(
                        annotation,
                        atom.atom_id,
                        atom.atom_type,
                        atom.observed_status,
                        evidence_ref,
                        "duplicate_evidence_refs",
                        "warning",
                        "deduplicate evidence refs before retry or manual review",
                    )
                )
            seen.add(evidence_ref)
            if not _supported_prefix(evidence_ref):
                rows.append(
                    _row(
                        annotation,
                        atom.atom_id,
                        atom.atom_type,
                        atom.observed_status,
                        evidence_ref,
                        "unsupported_prefix",
                        "error",
                        "use a supported evidence_ref prefix",
                    )
                )
            if len(evidence_ref) > MAX_EVIDENCE_REF_LENGTH:
                rows.append(
                    _row(
                        annotation,
                        atom.atom_id,
                        atom.atom_type,
                        atom.observed_status,
                        evidence_ref,
                        "evidence_ref_too_long",
                        "warning",
                        "shorten the cited span to the atom-specific fragment",
                    )
                )
            if _vague_ref(evidence_ref):
                rows.append(
                    _row(
                        annotation,
                        atom.atom_id,
                        atom.atom_type,
                        atom.observed_status,
                        evidence_ref,
                        "vague_evidence_ref",
                        "warning",
                        "replace vague evidence with a literal span or source_candidate_diff:changed",
                    )
                )
        if atom.atom_type == "operation_atom" and atom.observed_status == "implemented":
            rows.extend(_operation_quality_rows(annotation, atom.atom_id, atom.atom_type, atom.observed_status, evidence_refs))
        if atom.atom_type == "semantic_guard_atom":
            rows.append(
                _row(
                    annotation,
                    atom.atom_id,
                    atom.atom_type,
                    atom.observed_status,
                    "",
                    "semantic_guard_not_operation_numerator",
                    "info",
                    "keep semantic guard review separate from operation coverage numerator",
                )
            )
    return rows


def lint_jsonl_annotation_rows(rows: Iterable[Mapping[str, object]]) -> list[EvidenceRefLintRow]:
    lint_rows: list[EvidenceRefLintRow] = []
    for row in rows:
        if row.get("annotation_status") != "schema_valid":
            continue
        annotation = row.get("annotation")
        if isinstance(annotation, Mapping):
            lint_rows.extend(lint_annotation(annotation))
    return lint_rows


def summarize_lint_rows(rows: Iterable[EvidenceRefLintRow]) -> list[dict[str, str]]:
    counts: Counter[tuple[str, str]] = Counter((row.issue_type, row.severity) for row in rows)
    return [
        {
            "issue_type": issue_type,
            "severity": severity,
            "count": str(count),
            "notes": _summary_note(issue_type),
        }
        for (issue_type, severity), count in sorted(counts.items())
    ]


def write_lint_rows_csv(path: Path, rows: Iterable[EvidenceRefLintRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=evidence_ref_lint_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(lint_rows_to_csv_rows(rows))


def _operation_quality_rows(
    annotation: CandidateAnnotation,
    atom_id: str,
    atom_type: str,
    observed_status: str,
    evidence_refs: tuple[str, ...],
) -> list[EvidenceRefLintRow]:
    rows: list[EvidenceRefLintRow] = []
    if not any(ref == "source_candidate_diff:changed" for ref in evidence_refs):
        rows.append(
            _row(
                annotation,
                atom_id,
                atom_type,
                observed_status,
                "",
                "missing_source_candidate_diff",
                "warning",
                "pair operation evidence with source_candidate_diff:changed",
            )
        )
    prefix_set = {_prefix(ref) for ref in evidence_refs if _prefix(ref)}
    only_candidate = prefix_set == {"candidate_sql_span:"}
    only_source = prefix_set == {"source_sql_span:"}
    only_positive = prefix_set == {"positive_sql_span:"}
    if only_candidate:
        issue = "candidate_sql_span_only"
    elif only_source:
        issue = "source_sql_span_only"
    elif only_positive:
        issue = "positive_sql_span_only"
    else:
        issue = ""
    if issue:
        rows.append(
            _row(
                annotation,
                atom_id,
                atom_type,
                observed_status,
                " | ".join(evidence_refs),
                issue,
                "warning",
                "span presence alone is not transformation evidence; add diff plus atom-specific support",
            )
        )
    return rows


def _row(
    annotation: CandidateAnnotation,
    atom_id: str,
    atom_type: str,
    observed_status: str,
    evidence_ref: str,
    issue_type: str,
    severity: str,
    recommendation: str,
) -> EvidenceRefLintRow:
    return EvidenceRefLintRow(
        case_id=annotation.case_id,
        pool=annotation.pool,
        atom_id=atom_id,
        atom_type=atom_type,
        observed_status=observed_status,
        evidence_ref=evidence_ref,
        lint_status="issue",
        issue_type=issue_type,
        severity=severity,
        recommendation=recommendation,
    )


def _supported_prefix(evidence_ref: str) -> bool:
    return any(evidence_ref.startswith(prefix) for prefix in SUPPORTED_EVIDENCE_REF_PREFIXES)


def _prefix(evidence_ref: str) -> str:
    if evidence_ref.startswith("source_candidate_diff:changed"):
        return "source_candidate_diff:changed"
    if ":" not in evidence_ref:
        return ""
    return evidence_ref.split(":", 1)[0] + ":"


def _vague_ref(evidence_ref: str) -> bool:
    if not evidence_ref.strip():
        return True
    if ":" not in evidence_ref:
        return True
    _, value = evidence_ref.split(":", 1)
    normalized = " ".join(value.strip().lower().split())
    if evidence_ref == "source_candidate_diff:changed":
        return False
    return normalized in {"", "...", "same", "same as source", "changed", "candidate", "source", "positive"} or len(normalized) < 4


def _summary_note(issue_type: str) -> str:
    if issue_type == "semantic_guard_not_operation_numerator":
        return "informational boundary reminder; not an operation numerator issue"
    if issue_type == "missing_source_candidate_diff":
        return "operation atoms need transformation-aware evidence relative to source"
    if issue_type.endswith("_only"):
        return "span-only evidence is quality feedback and remains Stage B limited"
    return "quality feedback only; diagnostics are not modified"
