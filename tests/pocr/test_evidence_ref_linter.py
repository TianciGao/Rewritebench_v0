from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.evidence_ref_linter import lint_annotation, lint_jsonl_annotation_rows, summarize_lint_rows


def _annotation(atoms):
    return annotation_from_mapping(
        {
            "case_id": "PERF_0006",
            "pool": "PERF",
            "engine": "postgres",
            "method_id": "direct_llm_repair_1",
            "route_id": "direct_llm_repair_1_pg40_pocr_diagnostic",
            "candidate_id": "candidate",
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "atoms": atoms,
        }
    )


def test_linter_reports_missing_refs_for_implemented_operation() -> None:
    rows = lint_annotation(
        _annotation(
            [
                {
                    "atom_id": "A1",
                    "atom_type": "operation_atom",
                    "expected": True,
                    "observed_status": "implemented",
                    "rationale_short": "implemented",
                    "evidence_refs": [],
                    "confidence": "high",
                }
            ]
        )
    )

    assert {row.issue_type for row in rows} == {"missing_evidence_refs", "missing_source_candidate_diff"}
    assert any(row.severity == "error" for row in rows)


def test_linter_reports_unsupported_duplicate_vague_and_too_long_refs() -> None:
    long_ref = "candidate_sql_span:" + "x" * 501
    rows = lint_annotation(
        _annotation(
            [
                {
                    "atom_id": "A1",
                    "atom_type": "operation_atom",
                    "expected": True,
                    "observed_status": "implemented",
                    "rationale_short": "implemented",
                    "evidence_refs": ["bad_prefix:value", "candidate_sql_span:...", long_ref, long_ref],
                    "confidence": "high",
                }
            ]
        )
    )

    issue_types = {row.issue_type for row in rows}
    assert "unsupported_prefix" in issue_types
    assert "duplicate_evidence_refs" in issue_types
    assert "vague_evidence_ref" in issue_types
    assert "evidence_ref_too_long" in issue_types
    assert "missing_source_candidate_diff" in issue_types


def test_linter_reports_span_only_operation_boundaries() -> None:
    rows = lint_annotation(
        _annotation(
            [
                {
                    "atom_id": "A1",
                    "atom_type": "operation_atom",
                    "expected": True,
                    "observed_status": "implemented",
                    "rationale_short": "implemented",
                    "evidence_refs": ["candidate_sql_span:WHERE x = 1"],
                    "confidence": "high",
                }
            ]
        )
    )

    assert "candidate_sql_span_only" in {row.issue_type for row in rows}


def test_linter_marks_semantic_guard_as_not_operation_numerator() -> None:
    rows = lint_annotation(
        _annotation(
            [
                {
                    "atom_id": "A4",
                    "atom_type": "semantic_guard_atom",
                    "expected": True,
                    "observed_status": "implemented",
                    "rationale_short": "guard",
                    "evidence_refs": ["candidate_sql_span:WHERE x = 1"],
                    "confidence": "high",
                }
            ]
        )
    )

    assert any(row.issue_type == "semantic_guard_not_operation_numerator" and row.severity == "info" for row in rows)


def test_jsonl_linter_skips_fail_closed_rows_and_summarizes() -> None:
    annotation = _annotation(
        [
            {
                "atom_id": "A1",
                "atom_type": "operation_atom",
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "implemented",
                "evidence_refs": ["positive_sql_span:WHERE x = 1"],
                "confidence": "high",
            }
        ]
    )
    rows = lint_jsonl_annotation_rows(
        [
            {
                "annotation_status": "schema_valid",
                "annotation": {
                    "case_id": annotation.case_id,
                    "pool": annotation.pool,
                    "engine": annotation.engine,
                    "method_id": annotation.method_id,
                    "route_id": annotation.route_id,
                    "candidate_id": "candidate",
                    "annotation_schema_version": annotation.annotation_schema_version,
                    "atoms": [
                        {
                            "atom_id": atom.atom_id,
                            "atom_type": atom.atom_type,
                            "expected": atom.expected,
                            "observed_status": atom.observed_status,
                            "rationale_short": atom.rationale_short,
                            "evidence_refs": list(atom.evidence_refs),
                            "confidence": atom.confidence,
                        }
                        for atom in annotation.atoms
                    ],
                },
            },
            {"annotation_status": "timeout", "annotation": {}},
        ]
    )

    summary = summarize_lint_rows(rows)

    assert rows
    assert any(row["issue_type"] == "positive_sql_span_only" for row in summary)
