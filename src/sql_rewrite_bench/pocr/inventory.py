"""Repository-level parse-only inventory for Common-core skills.md files."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from sql_rewrite_bench.pocr.models import SkillParseResult
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file

EXPECTED_COMMON_CORE_SPLIT = {"PERF": 16, "CONS": 9, "PORT": 9, "LONGTAIL": 6}


@dataclass(frozen=True)
class CommonCoreMember:
    case_id: str
    pool: str
    case_path: Path
    skills_path: Path


@dataclass(frozen=True)
class CommonCoreSkillInventory:
    repo_root: Path
    members: tuple[CommonCoreMember, ...]
    parse_results: tuple[SkillParseResult, ...]

    @property
    def parsed_count(self) -> int:
        return sum(1 for result in self.parse_results if result.contract is not None)

    @property
    def valid_count(self) -> int:
        return sum(1 for result in self.parse_results if result.ok)

    @property
    def atom_count(self) -> int:
        return sum(len(result.contract.atoms) for result in self.parse_results if result.contract)

    @property
    def operation_atom_count(self) -> int:
        return sum(len(result.contract.operation_atoms) for result in self.parse_results if result.contract)

    @property
    def semantic_guard_atom_count(self) -> int:
        return sum(len(result.contract.semantic_guard_atoms) for result in self.parse_results if result.contract)

    @property
    def pool_split(self) -> dict[str, int]:
        return dict(Counter(member.pool for member in self.members))

    @property
    def issues_count(self) -> int:
        return sum(len(result.issues) for result in self.parse_results)


def load_common_core_members(
    repo_root: Path,
    *,
    case_set_csv: Path = Path("case_sets/common_core_v0/cases.csv"),
) -> tuple[CommonCoreMember, ...]:
    """Load Common-core v0 case membership and expected skills.md paths."""

    csv_path = repo_root / case_set_csv
    members: list[CommonCoreMember] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            case_path = Path(row["case_path"])
            members.append(
                CommonCoreMember(
                    case_id=row["case_id"],
                    pool=row["pool"],
                    case_path=case_path,
                    skills_path=case_path / "skills.md",
                )
            )
    return tuple(members)


def build_common_core_inventory(repo_root: Path) -> CommonCoreSkillInventory:
    """Parse and validate exactly the Common-core v0 skills.md files."""

    members = load_common_core_members(repo_root)
    _validate_membership_shape(members)
    results = tuple(
        parse_skills_file(
            repo_root / member.skills_path,
            expected_case_id=member.case_id,
            expected_pool=member.pool,
        )
        for member in members
    )
    return CommonCoreSkillInventory(repo_root=repo_root, members=members, parse_results=results)


def write_parse_only_report(inventory: CommonCoreSkillInventory, output_dir: Path) -> None:
    """Write audit-only parse inventory CSV files.

    This is not a metric computation and does not write user-run output,
    top-level reports/results, or case-local files.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_parsed_skills_inventory(inventory, output_dir / "parsed_skills_inventory.csv")
    _write_atom_inventory(inventory, output_dir / "atom_inventory.csv")
    _write_validation_issues(inventory, output_dir / "validation_issues.csv")


def _validate_membership_shape(members: tuple[CommonCoreMember, ...]) -> None:
    if len(members) != 40:
        raise ValueError(f"expected 40 Common-core members, found {len(members)}")
    split = Counter(member.pool for member in members)
    if dict(split) != EXPECTED_COMMON_CORE_SPLIT:
        raise ValueError(f"unexpected Common-core pool split: {dict(split)}")
    seen = {(member.pool, member.case_id) for member in members}
    if len(seen) != len(members):
        raise ValueError("duplicate Common-core case membership rows")


def _write_parsed_skills_inventory(inventory: CommonCoreSkillInventory, path: Path) -> None:
    fields = [
        "case_id",
        "pool",
        "skills_path",
        "parsed_case_id",
        "parsed_pool",
        "atom_count",
        "operation_atom_count",
        "semantic_guard_atom_count",
        "has_required_candidate_annotation_shape",
        "has_review_boundaries",
        "validation_status",
        "issue_count",
        "notes",
    ]
    rows = []
    for member, result in zip(inventory.members, inventory.parse_results, strict=True):
        contract = result.contract
        rows.append(
            {
                "case_id": member.case_id,
                "pool": member.pool,
                "skills_path": member.skills_path.as_posix(),
                "parsed_case_id": contract.case_id if contract else "",
                "parsed_pool": contract.pool if contract else "",
                "atom_count": len(contract.atoms) if contract else 0,
                "operation_atom_count": len(contract.operation_atoms) if contract else 0,
                "semantic_guard_atom_count": len(contract.semantic_guard_atoms) if contract else 0,
                "has_required_candidate_annotation_shape": str(contract.has_required_candidate_annotation_shape).lower()
                if contract
                else "false",
                "has_review_boundaries": str(contract.has_review_boundaries).lower() if contract else "false",
                "validation_status": "pass" if result.ok else "fail",
                "issue_count": len(result.issues),
                "notes": "parse-only; no POCR computation",
            }
        )
    _write_csv(path, fields, rows)


def _write_atom_inventory(inventory: CommonCoreSkillInventory, path: Path) -> None:
    fields = [
        "case_id",
        "pool",
        "skills_path",
        "atom_id",
        "category",
        "type",
        "risk",
        "weight",
        "requirement",
        "source_row_number",
        "notes",
    ]
    rows = []
    for member, result in zip(inventory.members, inventory.parse_results, strict=True):
        if not result.contract:
            continue
        for atom in result.contract.atoms:
            rows.append(
                {
                    "case_id": member.case_id,
                    "pool": member.pool,
                    "skills_path": member.skills_path.as_posix(),
                    "atom_id": atom.atom_id,
                    "category": atom.category,
                    "type": atom.atom_type,
                    "risk": atom.risk,
                    "weight": atom.weight_raw,
                    "requirement": atom.requirement,
                    "source_row_number": atom.source_row_number or "",
                    "notes": "atom parsed from skills.md Atom Protocol only",
                }
            )
    _write_csv(path, fields, rows)


def _write_validation_issues(inventory: CommonCoreSkillInventory, path: Path) -> None:
    fields = ["case_id", "pool", "skills_path", "severity", "code", "message"]
    rows = []
    for result in inventory.parse_results:
        for issue in result.issues:
            rows.append(
                {
                    "case_id": issue.case_id or "",
                    "pool": issue.pool or "",
                    "skills_path": issue.skills_path.as_posix() if issue.skills_path else "",
                    "severity": issue.severity,
                    "code": issue.code,
                    "message": issue.message,
                }
            )
    _write_csv(path, fields, rows)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
