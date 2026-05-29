"""Metadata-driven case selection for user-run MVP.

The MVP intentionally resolves only Common-core v0 case-engine rows from
``case_sets/`` metadata. It does not infer membership by scanning ``cases/``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ALLOWED_ENGINES = {"postgres", "mysql", "spark"}
ALLOWED_POOLS = {"PERF", "CONS", "PORT", "LONGTAIL"}
SUPPORTED_CASE_SET = "common_core_v0"
SMOKE_CASE_IDS = ("PERF_0006", "CONS_0005")


@dataclass(frozen=True)
class SelectedCaseEngineRow:
    """One selected Common-core case-engine row."""

    denominator_id: str
    case_id: str
    pool: str
    engine: str
    planned: str
    case_path: str
    source_sql_path: str


@dataclass(frozen=True)
class CaseInventoryRow:
    """One Common-core case package row from case-set metadata."""

    case_id: str
    pool: str
    case_path: str
    common_core_v0_member: str
    denominator_eligible: str
    planned_engines: tuple[str, ...]
    planned_row_count: int


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_case_list(path: Path) -> set[str]:
    """Read a simple case-id list, allowing blank lines and comments."""

    case_ids: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            case_ids.add(line)
    return case_ids


def read_common_core_case_inventory(
    *,
    repo_root: Path,
    case_set: str,
    pool: str = "all",
    engine: str = "all",
) -> list[CaseInventoryRow]:
    """Read Common-core case inventory from case-set metadata."""

    if case_set != SUPPORTED_CASE_SET:
        raise ValueError(f"unsupported case set for MVP: {case_set}")
    if pool != "all" and pool not in ALLOWED_POOLS:
        raise ValueError(f"unsupported pool: {pool}")
    if engine != "all" and engine not in ALLOWED_ENGINES:
        raise ValueError(f"unsupported engine: {engine}")

    case_set_dir = repo_root / "case_sets" / SUPPORTED_CASE_SET
    case_rows = _read_csv(case_set_dir / "cases.csv")
    denominator_rows = _read_csv(case_set_dir / "denominator_same_engine_120.csv")
    planned_by_case: dict[str, list[str]] = {}
    for row in denominator_rows:
        if row.get("planned") != "true":
            continue
        if engine != "all" and row.get("engine") != engine:
            continue
        planned_by_case.setdefault(row["case_id"], []).append(row["engine"])

    inventory: list[CaseInventoryRow] = []
    for row in case_rows:
        if row.get("common_core_v0_member") != "true":
            continue
        if pool != "all" and row.get("pool") != pool:
            continue
        planned_engines = tuple(sorted(planned_by_case.get(row["case_id"], [])))
        inventory.append(
            CaseInventoryRow(
                case_id=row["case_id"],
                pool=row["pool"],
                case_path=row["case_path"],
                common_core_v0_member=row["common_core_v0_member"],
                denominator_eligible=row["denominator_eligible"],
                planned_engines=planned_engines,
                planned_row_count=len(planned_engines),
            )
        )
    return inventory


def common_core_case_ids(*, repo_root: Path, case_set: str) -> set[str]:
    """Return Common-core case ids from case-set metadata."""

    if case_set != SUPPORTED_CASE_SET:
        raise ValueError(f"unsupported case set for MVP: {case_set}")
    case_rows = _read_csv(repo_root / "case_sets" / SUPPORTED_CASE_SET / "cases.csv")
    return {
        row["case_id"]
        for row in case_rows
        if row.get("common_core_v0_member") == "true"
    }


def resolve_common_core_selection(
    *,
    repo_root: Path,
    case_set: str,
    pool: str = "all",
    engine: str = "all",
    case_list: Path | None = None,
    smoke: bool = False,
) -> list[SelectedCaseEngineRow]:
    """Resolve Common-core v0 selected case-engine rows from static metadata."""

    if case_set != SUPPORTED_CASE_SET:
        raise ValueError(f"unsupported case set for MVP: {case_set}")
    if pool != "all" and pool not in ALLOWED_POOLS:
        raise ValueError(f"unsupported pool: {pool}")
    if engine != "all" and engine not in ALLOWED_ENGINES:
        raise ValueError(f"unsupported engine: {engine}")
    if smoke and case_list is not None:
        raise ValueError("--smoke cannot be combined with --case-list")
    if smoke and pool != "all":
        raise ValueError(
            "--smoke cannot be combined with --pool; it selects PERF_0006 and CONS_0005"
        )

    case_set_dir = repo_root / "case_sets" / SUPPORTED_CASE_SET
    cases_path = case_set_dir / "cases.csv"
    denominator_path = case_set_dir / "denominator_same_engine_120.csv"
    if not cases_path.exists():
        raise FileNotFoundError(cases_path)
    if not denominator_path.exists():
        raise FileNotFoundError(denominator_path)

    case_rows = _read_csv(cases_path)
    denominator_rows = _read_csv(denominator_path)
    case_by_id = {row["case_id"]: row for row in case_rows}
    explicit_cases = (
        set(SMOKE_CASE_IDS)
        if smoke
        else (read_case_list(case_list) if case_list else None)
    )

    selected: list[SelectedCaseEngineRow] = []
    for row in denominator_rows:
        case_id = row["case_id"]
        case_meta = case_by_id.get(case_id)
        if case_meta is None:
            raise ValueError(f"denominator row has no case metadata: {case_id}")
        if case_meta.get("common_core_v0_member") != "true":
            continue
        if row.get("planned") != "true":
            continue
        if pool != "all" and row["pool"] != pool:
            continue
        if engine != "all" and row["engine"] != engine:
            continue
        if explicit_cases is not None and case_id not in explicit_cases:
            continue
        case_path = row["case_path"]
        source_sql_path = str(Path(case_path) / "sql" / "source.sql")
        selected.append(
            SelectedCaseEngineRow(
                denominator_id=row["denominator_id"],
                case_id=case_id,
                pool=row["pool"],
                engine=row["engine"],
                planned=row["planned"],
                case_path=case_path,
                source_sql_path=source_sql_path,
            )
        )

    return selected
