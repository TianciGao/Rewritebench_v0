from pathlib import Path

from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt
from sql_rewrite_bench.pocr.skills_parser import parse_skills_text


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0002`
- pool: `CONS`

## Atom Protocol

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| O1 | `operation_atom` | `predicate_pushdown` | medium | 1.0 | Candidate pushes a safe predicate. |
| S1 | `semantic_guard_atom` | `duplicate_preservation` | high | 1.0 | Candidate preserves duplicate multiplicity. |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def _inputs() -> AnnotationPromptInputs:
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/CONS/CASE_0002/skills.md"),
        expected_case_id="CASE_0002",
        expected_pool="CONS",
    )
    assert result.contract is not None
    return AnnotationPromptInputs(
        contract=result.contract,
        source_sql="select * from t where x > 1",
        candidate_sql="select * from t where x > 1",
        positive_sql="select * from t where x > 1",
        negative_sql="select * from t",
        engine="postgres",
        method_id="fixture_method",
        route_id="fixture_route",
        candidate_id="candidate_001",
    )


def test_prompt_is_deterministic_and_contains_required_boundaries() -> None:
    prompt_a = build_annotation_prompt(_inputs())
    prompt_b = build_annotation_prompt(_inputs())

    assert prompt_a == prompt_b
    assert "Judge only the atoms explicitly defined" in prompt_a
    assert "Do not invent atoms" in prompt_a
    assert "operation_atom" in prompt_a
    assert "semantic_guard_atom" in prompt_a
    assert "strict JSON" in prompt_a
    assert "unclear rather than guessing" in prompt_a
    assert "Do not use speedup, timing, runtime performance, taxonomy tags, or checker exactness" in prompt_a
    assert "LLM rationale is not evidence" in prompt_a
    assert "semantic_guard_atom is not an operation coverage numerator" in prompt_a
    assert "O1" in prompt_a
    assert "S1" in prompt_a
    assert "Optional positive SQL context" in prompt_a
    assert "Optional negative SQL context" in prompt_a


def test_prompt_requires_candidate_reference() -> None:
    inputs = _inputs()
    bad_inputs = AnnotationPromptInputs(
        contract=inputs.contract,
        source_sql=inputs.source_sql,
        candidate_sql=inputs.candidate_sql,
        engine=inputs.engine,
        method_id=inputs.method_id,
        route_id=inputs.route_id,
    )

    try:
        build_annotation_prompt(bad_inputs)
    except ValueError as exc:
        assert "candidate_id or candidate_path" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_prompt_aligns_evidence_refs_with_static_stage_b_contract() -> None:
    prompt = build_annotation_prompt(_inputs())

    for prefix in (
        "candidate_sql_span:<literal substring>",
        "source_sql_span:<literal substring>",
        "positive_sql_span:<literal substring>",
        "candidate_token_span:<normalized tokens>",
        "source_candidate_diff:changed",
    ):
        assert prefix in prompt
    assert "Unsupported refs" in prompt
    assert "will be rejected by Stage B" in prompt
    assert "Do not cite vague phrases" in prompt
    assert "Do not invent atoms" in prompt
    assert "infer atoms from taxonomy" in prompt
    assert "Return strict JSON only" in prompt
    assert "Do not mark an operation_atom as implemented merely because the candidate preserves a source-side SQL fragment" in prompt
    assert "do not cite candidate_sql_span merely because a SQL fragment exists" in prompt
    assert "actually implements that transformation relative to the source" in prompt
    assert "source_candidate_diff:changed when the candidate differs from source in the atom-relevant region" in prompt
    assert "candidate_sql_span:<literal substring>, positive_sql_span:<literal substring>, and source_candidate_diff:changed" in prompt
    assert "positive-aligned static refs only as comparison evidence" in prompt
    assert "source-like/no-op" in prompt
    assert "If only source-preserved text exists, do not call the operation_atom implemented" in prompt
