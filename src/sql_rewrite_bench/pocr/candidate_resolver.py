"""Read-only candidate SQL source resolver for POCR diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sql_rewrite_bench.pocr.inventory import build_common_core_inventory


@dataclass(frozen=True)
class CandidateSource:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_path: Path
    candidate_present: bool
    source_sql_path: Path
    positive_sql_path: Path | None
    negative_sql_path: Path | None
    skills_md_path: Path
    resolver_status: str
    boundary_notes: str


def resolve_candidate_sources(
    repo_root: Path,
    *,
    candidate_root: Path,
    method_id: str,
    route_id: str,
    engine: str = "postgres",
    case_ids: tuple[str, ...] | None = None,
) -> tuple[CandidateSource, ...]:
    """Resolve existing candidate SQL artifacts without running any method."""

    inventory = build_common_core_inventory(repo_root)
    wanted = set(case_ids) if case_ids else {member.case_id for member in inventory.members}
    unknown = wanted - {member.case_id for member in inventory.members}
    if unknown:
        raise ValueError(f"case filter includes non-Common-core case IDs: {sorted(unknown)}")

    rows: list[CandidateSource] = []
    for member in inventory.members:
        if member.case_id not in wanted:
            continue
        case_dir = repo_root / member.case_path
        source_path = member.case_path / "sql/source.sql"
        positive_path = member.case_path / "sql/pos_01.sql"
        negative_path = member.case_path / "sql/neg_01.sql"
        skills_path = member.skills_path
        candidate_path = candidate_root / f"{member.case_id}__{engine}.sql"

        source_present = (repo_root / source_path).is_file()
        skills_present = (repo_root / skills_path).is_file()
        candidate_present = (repo_root / candidate_path).is_file()
        positive_present = (repo_root / positive_path).is_file()
        negative_present = (repo_root / negative_path).is_file()

        if not source_present:
            status = "missing_source_sql"
        elif not skills_present:
            status = "missing_skills_md"
        elif not candidate_present:
            status = "missing_candidate"
        else:
            status = "resolved"

        rows.append(
            CandidateSource(
                case_id=member.case_id,
                pool=member.pool,
                engine=engine,
                method_id=method_id,
                route_id=route_id,
                candidate_path=candidate_path,
                candidate_present=candidate_present,
                source_sql_path=source_path,
                positive_sql_path=positive_path if positive_present else None,
                negative_sql_path=negative_path if negative_present else None,
                skills_md_path=skills_path,
                resolver_status=status,
                boundary_notes=(
                    "read-only resolver; no candidate SQL created; v2 case paths only; "
                    "skills.md aliases do not trigger rewrites"
                ),
            )
        )
    return tuple(rows)


def candidate_sources_to_csv_rows(sources: tuple[CandidateSource, ...]) -> list[dict[str, object]]:
    """Return audit CSV rows for resolved candidate sources."""

    return [
        {
            "case_id": source.case_id,
            "pool": source.pool,
            "engine": source.engine,
            "method_id": source.method_id,
            "route_id": source.route_id,
            "candidate_path": source.candidate_path.as_posix(),
            "candidate_present": str(source.candidate_present).lower(),
            "source_sql_path": source.source_sql_path.as_posix(),
            "positive_sql_path": source.positive_sql_path.as_posix() if source.positive_sql_path else "",
            "negative_sql_path": source.negative_sql_path.as_posix() if source.negative_sql_path else "",
            "skills_md_path": source.skills_md_path.as_posix(),
            "resolver_status": source.resolver_status,
            "boundary_notes": source.boundary_notes,
        }
        for source in sources
    ]


def candidate_inventory_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_path",
        "candidate_present",
        "source_sql_path",
        "positive_sql_path",
        "negative_sql_path",
        "skills_md_path",
        "resolver_status",
        "boundary_notes",
    ]
