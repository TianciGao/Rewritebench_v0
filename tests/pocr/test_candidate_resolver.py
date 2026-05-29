from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.candidate_resolver import (
    candidate_inventory_fields,
    candidate_sources_to_csv_rows,
    resolve_candidate_sources,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_candidate_resolver_maps_existing_candidate_without_running_method(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")

    rows = resolve_candidate_sources(
        REPO_ROOT,
        candidate_root=candidate_root,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.case_id == "PERF_0006"
    assert row.pool == "PERF"
    assert row.candidate_present is True
    assert row.resolver_status == "resolved"
    assert row.source_sql_path.as_posix() == "cases/PERF/PERF_0006/sql/source.sql"
    assert row.skills_md_path.as_posix() == "cases/PERF/PERF_0006/skills.md"
    assert row.positive_sql_path is not None
    assert row.negative_sql_path is not None

    csv_rows = candidate_sources_to_csv_rows(rows)
    assert list(csv_rows[0]) == candidate_inventory_fields()
    assert csv_rows[0]["candidate_present"] == "true"


def test_candidate_resolver_reports_missing_candidate(tmp_path: Path) -> None:
    rows = resolve_candidate_sources(
        REPO_ROOT,
        candidate_root=tmp_path / "candidate_sql",
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("CONS_0005",),
    )

    assert rows[0].candidate_present is False
    assert rows[0].resolver_status == "missing_candidate"


def test_candidate_resolver_rejects_non_common_core_case_filter(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="non-Common-core"):
        resolve_candidate_sources(
            REPO_ROOT,
            candidate_root=tmp_path / "candidate_sql",
            method_id="noop_adapter",
            route_id="test_route",
            engine="postgres",
            case_ids=("NOT_A_CASE",),
        )
