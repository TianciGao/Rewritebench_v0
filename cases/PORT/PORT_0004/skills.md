# Baseline Rewrite Audit Skill
<!-- skills to compute metric "Positive Operation Coverage" -->
<!-- generated-by: tools/baseline_audit/run_case_audit.py develop -->

## Scope
- case_id: `PORT_0004`
- pool: `PORT`
- opportunity_family: $family`

Use this file when reviewing a baseline-produced SQL rewrite candidate for this case. The audit is diagnostic only and does not change benchmark membership or create paper metrics.

## Canonical Case Evidence
- Source SQL: `source.sql`
- Canonical positive rewrite (legacy): `rewrite_pos_01.sql`
- Baseline positive rewrite (preferred positive control): `pos_baseline.sql`
- Canonical hard-negative rewrite: `rewrite_neg_01.sql`
- Additional positive rewrite: `rewrite_pos_02_spark.sql`
- Additional hard-negative rewrite: `rewrite_neg_02_spark.sql`
- Manifest: `manifest.yaml`
- Taxonomy: `taxonomy_trial_v0.3.yaml`
- Supporting evidence: `README.md`, `risk_notes.md`, `witness_design_notes.md`
- Retained evidence: `data/`, `provenance/`, `schema/`, `validation/`, `runs/`

## Audit Procedure
1. Read source, legacy positive, baseline positive, negative, manifest, taxonomy, validation assets, and retained evidence before judging a candidate.
2. Use the atoms below; they are derived by comparing `source.sql`, `rewrite_pos_01.sql`, `pos_baseline.sql`, and `rewrite_neg_01.sql`, not from the candidate under review.
3. Mark each atom as `satisfied`, `partially_satisfied`, `missing`, or `violated`, with SQL-span evidence where possible.
4. Compute operation coverage from operation atoms only.
5. Treat high-risk semantic guards as validity gates.
6. Do not claim speedup, admission, or paper-facing metric changes from this audit alone.

## Atom Protocol

Preferred positive-control basis: `pos_baseline.sql`; legacy positive evidence: `rewrite_pos_01.sql`; hard-negative boundary: `rewrite_neg_01.sql`. The atom rows below should be judged against operations and guards visible in the positive controls, with the negative rewrite used to identify semantic failure boundaries.

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| A1 | `operation_atom` | `target_normalized_percentage_expression` | medium | 1.0 | Candidate uses the target-normalized female percentage expression with `CAST(SUM(CASE WHEN sex = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100`. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A2 | `operation_atom` | `extract_year_date_predicate_form` | medium | 1.0 | Candidate uses target-normalized `EXTRACT(YEAR FROM CAST(birthday AS DATE)) = 1980` year filtering. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A3 | `operation_atom` | `nullif_denominator_preservation_operation` | medium | 1.0 | Candidate preserves `NULLIF(COUNT(id), 0)` or equivalent divide-by-zero protection in the percentage denominator. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A4 | `semantic_guard_atom` | `year_literal_preservation` | high | 1.0 | Candidate preserves the birthday year `1980` and does not change it to another year. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A5 | `semantic_guard_atom` | `diagnosis_and_gender_count_preservation` | high | 1.0 | Candidate preserves diagnosis `RA`, female count numerator, count denominator, and percentage expression. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |

Status values:
| status | score value | meaning |
|---|---:|---|
| `satisfied` | 1.0 | clear SQL span or canonical evidence supports the atom |
| `partially_satisfied` / `uncertain` | 0.5 | incomplete implementation or incomplete evidence |
| `missing` | 0.0 | expected atom is absent |
| `violated` | 0.0 | candidate changes a semantic guard in a result-changing way |

## Required Candidate Annotation Shape
```json
{
  "schema_version": "llm_annotation_v1",
  "case_id": "PORT_0004",
  "baseline_method_id": "<method>",
  "target_engine": "<engine>",
  "annotation_protocol": "skills.md",
  "canonical_positive_paths": ["rewrite_pos_01.sql", "pos_baseline.sql"],
  "hard_negative_path": "rewrite_neg_01.sql",
  "atoms": [
    {
      "atom_id": "A1",
      "category": "operation_atom | semantic_guard_atom",
      "type": "target_normalized_percentage_expression",
      "status": "satisfied | partially_satisfied | missing | violated",
      "semantic_risk": "low | medium | high",
      "weight": 1.0,
      "sql_span": "<candidate SQL span supporting the judgment>",
      "rationale": "<short explanation>"
    }
  ],
  "claim_boundary": [
    "LLM annotation only; requires runner validation.",
    "No speedup claim without plan/runtime evidence.",
    "No human_verified claim without reviewer sign-off."
  ]
}
```

## Review Boundaries
- Equivalent rewrites need not match the canonical positive SQL surface exactly.
- Prefer clause-level evidence over general descriptions.
- Retained plans and controls support observability context, but this generated skill does not rerun engines.
