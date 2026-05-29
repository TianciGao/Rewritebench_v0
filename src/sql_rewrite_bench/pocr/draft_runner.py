"""Diagnostic POCR row draft runner.

The runner resolves existing candidate artifacts and emits row-level draft
records only. It does not call APIs, run baselines, execute databases, run
checkers/timing, compute official POCR, or aggregate route-level POCR.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, annotation_from_mapping
from sql_rewrite_bench.pocr.candidate_resolver import resolve_candidate_sources
from sql_rewrite_bench.pocr.evidence_validation import validate_stage_b
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.json_output_guard import guarded_json_loads


@dataclass(frozen=True)
class DiagnosticPOCRDraftRow:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    skill_present: bool
    candidate_present: bool
    annotation_present: bool
    stage_b_status: str
    expected_operation_atoms_count: int
    expected_semantic_guard_atoms_count: int
    validated_operation_atoms_count: int
    official_pocr_computed: bool
    diagnostic_only: bool
    boundary_notes: str


def build_diagnostic_drafts(
    repo_root: Path,
    *,
    candidate_root: Path,
    method_id: str,
    route_id: str,
    engine: str = "postgres",
    case_ids: tuple[str, ...] | None = None,
    annotation_jsonl: Path | None = None,
) -> tuple[DiagnosticPOCRDraftRow, ...]:
    """Build row-level diagnostic drafts from candidates and optional annotations."""

    inventory = build_common_core_inventory(repo_root)
    contract_by_case = {
        member.case_id: result.contract
        for member, result in zip(inventory.members, inventory.parse_results, strict=True)
    }
    sources = resolve_candidate_sources(
        repo_root,
        candidate_root=candidate_root,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        case_ids=case_ids,
    )
    annotation_by_case = _load_annotations(annotation_jsonl) if annotation_jsonl else {}

    rows: list[DiagnosticPOCRDraftRow] = []
    for source in sources:
        contract = contract_by_case[source.case_id]
        skill_present = contract is not None and bool(contract.atoms)
        annotation = annotation_by_case.get(source.case_id)
        if not skill_present:
            stage_b_status = "missing_skill_contract"
            validated_operation_atoms = 0
            boundary = "skills.md contract missing or invalid; no POCR computation"
        elif not source.candidate_present:
            stage_b_status = "missing_candidate"
            validated_operation_atoms = 0
            boundary = "candidate SQL missing; no POCR computation"
        elif annotation is None:
            stage_b_status = "annotation_missing"
            validated_operation_atoms = 0
            boundary = "Stage A annotation absent; diagnostic row only"
        elif isinstance(annotation, str):
            stage_b_status = "schema_invalid"
            validated_operation_atoms = 0
            boundary = f"Stage A annotation invalid: {annotation}; no repair or POCR contribution"
        else:
            stage_b = validate_stage_b(
                contract,
                annotation,
                candidate_path=source.candidate_path.as_posix(),
                candidate_sql=(repo_root / source.candidate_path).read_text(encoding="utf-8-sig"),
            )
            stage_b_status = stage_b.stage_b_status
            validated_operation_atoms = stage_b.validated_operation_atoms_count
            boundary = "Stage B fail-closed unless independent evidence is supplied"
        rows.append(
            DiagnosticPOCRDraftRow(
                case_id=source.case_id,
                pool=source.pool,
                engine=source.engine,
                method_id=source.method_id,
                route_id=source.route_id,
                skill_present=skill_present,
                candidate_present=source.candidate_present,
                annotation_present=isinstance(annotation, CandidateAnnotation),
                stage_b_status=stage_b_status,
                expected_operation_atoms_count=len(contract.operation_atoms) if contract else 0,
                expected_semantic_guard_atoms_count=len(contract.semantic_guard_atoms) if contract else 0,
                validated_operation_atoms_count=validated_operation_atoms,
                official_pocr_computed=False,
                diagnostic_only=True,
                boundary_notes=boundary,
            )
        )
    return tuple(rows)


def write_diagnostic_draft_csv(path: Path, rows: tuple[DiagnosticPOCRDraftRow, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=diagnostic_draft_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(diagnostic_draft_to_csv_rows(rows))


def diagnostic_draft_to_csv_rows(rows: tuple[DiagnosticPOCRDraftRow, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "skill_present": str(row.skill_present).lower(),
            "candidate_present": str(row.candidate_present).lower(),
            "annotation_present": str(row.annotation_present).lower(),
            "stage_b_status": row.stage_b_status,
            "expected_operation_atoms_count": row.expected_operation_atoms_count,
            "expected_semantic_guard_atoms_count": row.expected_semantic_guard_atoms_count,
            "validated_operation_atoms_count": row.validated_operation_atoms_count,
            "official_pocr_computed": str(row.official_pocr_computed).lower(),
            "diagnostic_only": str(row.diagnostic_only).lower(),
            "boundary_notes": row.boundary_notes,
        }
        for row in rows
    ]


def diagnostic_draft_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "skill_present",
        "candidate_present",
        "annotation_present",
        "stage_b_status",
        "expected_operation_atoms_count",
        "expected_semantic_guard_atoms_count",
        "validated_operation_atoms_count",
        "official_pocr_computed",
        "diagnostic_only",
        "boundary_notes",
    ]


def _load_annotations(path: Path) -> dict[str, CandidateAnnotation | str]:
    annotations: dict[str, CandidateAnnotation | str] = {}
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            guarded = guarded_json_loads(line)
            if guarded.parsed is None:
                annotations[_case_id_hint(line, line_number)] = guarded.error
                continue
            payload = guarded.parsed.get("annotation", guarded.parsed)
            if not isinstance(payload, Mapping):
                annotations[f"line_{line_number}"] = "annotation payload is not an object"
                continue
            case_id = str(payload.get("case_id") or guarded.parsed.get("case_id") or f"line_{line_number}")
            try:
                annotations[case_id] = annotation_from_mapping(payload)
            except (TypeError, ValueError) as exc:
                annotations[case_id] = str(exc)
    return annotations


def _case_id_hint(raw: str, line_number: int) -> str:
    match = re.search(r'"case_id"\s*:\s*"([^"]+)"', raw)
    if match:
        return match.group(1)
    return f"line_{line_number}"
