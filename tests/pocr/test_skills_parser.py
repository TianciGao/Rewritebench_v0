from pathlib import Path

from sql_rewrite_bench.pocr.skills_parser import parse_skills_text


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0001`
- pool: `PERF`

## Atom Protocol

Intro text.

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| A1 | `operation_atom` | `join_elimination` | medium | 1.0 | Candidate removes redundant join without changing projected rows. |
| A2 | `semantic_guard_atom` | `null_preservation` | high | 1.0 | Candidate preserves null-sensitive predicates. |

Status values:

| status | score value | meaning |
|---|---:|---|
| `satisfied` | 1.0 | clear evidence |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def test_parse_skills_text_extracts_scope_and_atom_protocol_table() -> None:
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/PERF/CASE_0001/skills.md"),
        expected_case_id="CASE_0001",
        expected_pool="PERF",
    )

    assert result.ok
    assert result.contract is not None
    assert result.contract.case_id == "CASE_0001"
    assert result.contract.pool == "PERF"
    assert len(result.contract.atoms) == 2
    assert [atom.atom_id for atom in result.contract.operation_atoms] == ["A1"]
    assert [atom.atom_id for atom in result.contract.semantic_guard_atoms] == ["A2"]
    assert result.contract.operation_atoms[0].atom_type == "join_elimination"
    assert result.contract.semantic_guard_atoms[0].risk == "high"
    assert result.contract.operation_atoms[0].weight == 1.0


def test_parse_skills_text_reports_missing_contract_sections() -> None:
    result = parse_skills_text(
        "# Bad\n\n## Scope\n\n- case_id: `CASE_0001`\n- pool: `PERF`\n",
        skills_path=Path("cases/PERF/CASE_0001/skills.md"),
        expected_case_id="CASE_9999",
        expected_pool="PERF",
    )

    codes = {issue.code for issue in result.issues}
    assert not result.ok
    assert "case_id_mismatch" in codes
    assert "missing_atom_protocol" in codes
    assert "missing_operation_atom" in codes
    assert "missing_semantic_guard_atom" in codes
    assert "missing_required_candidate_annotation_shape" in codes
    assert "missing_review_boundaries" in codes
