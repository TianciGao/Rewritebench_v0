"""Read-only resolver for Stage A POCR annotation artifacts."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from sql_rewrite_bench.pocr.annotation_schema import (
    CandidateAnnotation,
    annotation_from_mapping,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.json_output_guard import guarded_json_loads
from sql_rewrite_bench.pocr.models import SkillContract


@dataclass(frozen=True)
class ResolvedAnnotationArtifact:
    """One resolved Stage A annotation artifact row.

    This resolver only reads audit artifacts. It does not call providers,
    repair malformed JSON, or treat Stage A output as POCR evidence.
    """

    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_ref: str
    annotation_schema_version: str
    annotation_status: str
    artifact_path: Path | None
    annotation: CandidateAnnotation | None
    issue_codes: tuple[str, ...]
    boundary_notes: str


def resolve_annotation_artifacts(
    repo_root: Path,
    *,
    annotation_jsonl: Path | None,
    method_id: str,
    route_id: str,
    engine: str = "postgres",
    case_ids: tuple[str, ...] | None = None,
) -> tuple[ResolvedAnnotationArtifact, ...]:
    """Resolve existing Stage A annotation JSONL artifacts for Common-core rows."""

    inventory = build_common_core_inventory(repo_root)
    contract_by_case: dict[str, SkillContract] = {
        member.case_id: result.contract
        for member, result in zip(inventory.members, inventory.parse_results, strict=True)
        if result.contract is not None
    }
    member_by_case = {member.case_id: member for member in inventory.members}
    wanted = set(case_ids) if case_ids else set(member_by_case)
    unknown = wanted - set(member_by_case)
    if unknown:
        raise ValueError(f"case filter includes non-Common-core case IDs: {sorted(unknown)}")

    resolved_by_case: dict[str, ResolvedAnnotationArtifact] = {}
    artifact_path = _normalize_annotation_path(repo_root, annotation_jsonl)
    if artifact_path and artifact_path.is_file():
        for row in _read_annotation_jsonl(
            repo_root,
            artifact_path=artifact_path,
            contract_by_case=contract_by_case,
            method_id=method_id,
            route_id=route_id,
            engine=engine,
        ):
            if row.case_id in wanted:
                resolved_by_case[row.case_id] = row

    rows: list[ResolvedAnnotationArtifact] = []
    for member in inventory.members:
        if member.case_id not in wanted:
            continue
        row = resolved_by_case.get(member.case_id)
        if row is not None:
            rows.append(row)
            continue
        rows.append(
            ResolvedAnnotationArtifact(
                case_id=member.case_id,
                pool=member.pool,
                engine=engine,
                method_id=method_id,
                route_id=route_id,
                candidate_ref="",
                annotation_schema_version="",
                annotation_status="missing",
                artifact_path=artifact_path if artifact_path and artifact_path.exists() else None,
                annotation=None,
                issue_codes=("annotation_missing",),
                boundary_notes="no usable Stage A annotation artifact was found for this row",
            )
        )
    return tuple(rows)


def write_annotation_artifact_inventory(path: Path, rows: tuple[ResolvedAnnotationArtifact, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=annotation_artifact_inventory_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(annotation_artifacts_to_csv_rows(rows))


def annotation_artifacts_to_csv_rows(rows: tuple[ResolvedAnnotationArtifact, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "candidate_ref": row.candidate_ref,
            "annotation_schema_version": row.annotation_schema_version,
            "annotation_status": row.annotation_status,
            "artifact_path": row.artifact_path.as_posix() if row.artifact_path else "",
            "issue_codes": ";".join(row.issue_codes),
            "boundary_notes": row.boundary_notes,
        }
        for row in rows
    ]


def annotation_artifact_inventory_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_ref",
        "annotation_schema_version",
        "annotation_status",
        "artifact_path",
        "issue_codes",
        "boundary_notes",
    ]


def _read_annotation_jsonl(
    repo_root: Path,
    *,
    artifact_path: Path,
    contract_by_case: dict[str, SkillContract],
    method_id: str,
    route_id: str,
    engine: str,
) -> tuple[ResolvedAnnotationArtifact, ...]:
    rows: list[ResolvedAnnotationArtifact] = []
    with artifact_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            rows.append(
                _resolve_annotation_line(
                    repo_root,
                    artifact_path=artifact_path,
                    line_number=line_number,
                    raw_line=line,
                    contract_by_case=contract_by_case,
                    method_id=method_id,
                    route_id=route_id,
                    engine=engine,
                )
            )
    return tuple(rows)


def _resolve_annotation_line(
    repo_root: Path,
    *,
    artifact_path: Path,
    line_number: int,
    raw_line: str,
    contract_by_case: dict[str, SkillContract],
    method_id: str,
    route_id: str,
    engine: str,
) -> ResolvedAnnotationArtifact:
    guarded = guarded_json_loads(raw_line)
    if guarded.parsed is None:
        case_id = _case_id_hint(raw_line, line_number)
        return ResolvedAnnotationArtifact(
            case_id=case_id,
            pool=_pool_from_case(case_id),
            engine=engine,
            method_id=method_id,
            route_id=route_id,
            candidate_ref="",
            annotation_schema_version="",
            annotation_status="malformed_json",
            artifact_path=_relative_to_repo(repo_root, artifact_path),
            annotation=None,
            issue_codes=("malformed_json",),
            boundary_notes=f"JSON guard rejected line {line_number}: {guarded.error}",
        )

    parsed = guarded.parsed
    payload = parsed.get("annotation", parsed)
    case_id = str(parsed.get("case_id") or _payload_case_id(payload) or f"line_{line_number}")
    pool = str(parsed.get("pool") or _payload_pool(payload) or _pool_from_case(case_id))
    if not isinstance(payload, Mapping):
        return _schema_invalid_row(
            repo_root,
            artifact_path=artifact_path,
            line_number=line_number,
            case_id=case_id,
            pool=pool,
            method_id=method_id,
            route_id=route_id,
            engine=engine,
            issue_codes=("annotation_payload_not_object",),
            message="annotation payload is not an object",
        )

    try:
        annotation = annotation_from_mapping(payload)
    except (TypeError, ValueError) as exc:
        return _schema_invalid_row(
            repo_root,
            artifact_path=artifact_path,
            line_number=line_number,
            case_id=case_id,
            pool=pool,
            method_id=method_id,
            route_id=route_id,
            engine=engine,
            issue_codes=("annotation_schema_conversion_failed",),
            message=str(exc),
        )

    top_case = parsed.get("case_id")
    if isinstance(top_case, str) and top_case and top_case != annotation.case_id:
        return _annotation_row(
            repo_root,
            artifact_path=artifact_path,
            annotation=annotation,
            status="case_mismatch",
            issue_codes=("annotation_case_id_mismatch",),
            notes=f"top-level case_id {top_case!r} does not match annotation case_id {annotation.case_id!r}",
        )

    contract = contract_by_case.get(annotation.case_id)
    if contract is None:
        return _annotation_row(
            repo_root,
            artifact_path=artifact_path,
            annotation=annotation,
            status="case_mismatch",
            issue_codes=("case_not_in_common_core_or_contract_missing",),
            notes="annotation case is not in the Common-core contract inventory",
        )

    issues = validate_candidate_annotation(
        annotation,
        contract,
        expected_engine=engine,
        expected_method_id=method_id,
        expected_route_id=route_id,
    )
    issue_codes = tuple(issue.code for issue in issues)
    if "annotation_method_id_mismatch" in issue_codes or "annotation_route_id_mismatch" in issue_codes:
        status = "route_mismatch"
    elif "annotation_case_id_mismatch" in issue_codes or "annotation_pool_mismatch" in issue_codes:
        status = "case_mismatch"
    elif issue_codes:
        status = "schema_invalid"
    else:
        status = "present"
    return _annotation_row(
        repo_root,
        artifact_path=artifact_path,
        annotation=annotation,
        status=status,
        issue_codes=issue_codes,
        notes="Stage A annotation resolved read-only; Stage B still requires independent evidence",
    )


def _annotation_row(
    repo_root: Path,
    *,
    artifact_path: Path,
    annotation: CandidateAnnotation,
    status: str,
    issue_codes: tuple[str, ...],
    notes: str,
) -> ResolvedAnnotationArtifact:
    return ResolvedAnnotationArtifact(
        case_id=annotation.case_id,
        pool=annotation.pool,
        engine=annotation.engine,
        method_id=annotation.method_id,
        route_id=annotation.route_id,
        candidate_ref=annotation.candidate_ref or "",
        annotation_schema_version=annotation.annotation_schema_version,
        annotation_status=status,
        artifact_path=_relative_to_repo(repo_root, artifact_path),
        annotation=annotation if status == "present" else None,
        issue_codes=issue_codes,
        boundary_notes=notes,
    )


def _schema_invalid_row(
    repo_root: Path,
    *,
    artifact_path: Path,
    line_number: int,
    case_id: str,
    pool: str,
    method_id: str,
    route_id: str,
    engine: str,
    issue_codes: tuple[str, ...],
    message: str,
) -> ResolvedAnnotationArtifact:
    return ResolvedAnnotationArtifact(
        case_id=case_id,
        pool=pool,
        engine=engine,
        method_id=method_id,
        route_id=route_id,
        candidate_ref="",
        annotation_schema_version="",
        annotation_status="schema_invalid",
        artifact_path=_relative_to_repo(repo_root, artifact_path),
        annotation=None,
        issue_codes=issue_codes,
        boundary_notes=f"line {line_number}: {message}",
    )


def _normalize_annotation_path(repo_root: Path, path: Path | None) -> Path | None:
    if path is None:
        return None
    return path if path.is_absolute() else repo_root / path


def _relative_to_repo(repo_root: Path, path: Path) -> Path:
    try:
        return path.relative_to(repo_root)
    except ValueError:
        return path


def _payload_case_id(payload: object) -> str | None:
    if isinstance(payload, Mapping):
        value = payload.get("case_id")
        if isinstance(value, str):
            return value
    return None


def _payload_pool(payload: object) -> str | None:
    if isinstance(payload, Mapping):
        value = payload.get("pool")
        if isinstance(value, str):
            return value
    return None


def _case_id_hint(raw: str, line_number: int) -> str:
    match = re.search(r'"case_id"\s*:\s*"([^"]+)"', raw)
    if match:
        return match.group(1)
    return f"line_{line_number}"


def _pool_from_case(case_id: str) -> str:
    return case_id.split("_", 1)[0] if "_" in case_id else ""
