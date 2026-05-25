import csv
from pathlib import Path

from sql_rewrite_bench.pocr.inventory import EXPECTED_COMMON_CORE_SPLIT, build_common_core_inventory, write_parse_only_report


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_common_core_skills_inventory_parses_all_40_contracts() -> None:
    inventory = build_common_core_inventory(REPO_ROOT)

    assert len(inventory.members) == 40
    assert inventory.parsed_count == 40
    assert inventory.valid_count == 40
    assert inventory.pool_split == EXPECTED_COMMON_CORE_SPLIT
    assert inventory.operation_atom_count >= 40
    assert inventory.semantic_guard_atom_count >= 40
    assert inventory.issues_count == 0


def test_parse_only_report_writes_audit_csvs(tmp_path: Path) -> None:
    inventory = build_common_core_inventory(REPO_ROOT)
    write_parse_only_report(inventory, tmp_path)

    parsed_path = tmp_path / "parsed_skills_inventory.csv"
    atom_path = tmp_path / "atom_inventory.csv"
    issues_path = tmp_path / "validation_issues.csv"

    parsed_rows = list(csv.DictReader(parsed_path.open(newline="")))
    atom_rows = list(csv.DictReader(atom_path.open(newline="")))
    issue_rows = list(csv.DictReader(issues_path.open(newline="")))

    assert len(parsed_rows) == 40
    assert len(atom_rows) == inventory.atom_count
    assert issue_rows == []
    assert {row["validation_status"] for row in parsed_rows} == {"pass"}
    assert {"operation_atom", "semantic_guard_atom"}.issubset({row["category"] for row in atom_rows})
