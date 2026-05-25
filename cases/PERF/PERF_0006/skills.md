# Baseline Rewrite Audit Skill
<!-- skills to compute metric "Positive Operation Coverage" -->
<!-- generated-by: tools/baseline_audit/run_case_audit.py develop -->

## Scope

- case_id: `PERF_0006`
- pool: `PERF`
- opportunity_family: `staged_filter_or_projection_rewrite`

Use this file when reviewing a baseline-produced SQL rewrite candidate for this case. The audit is diagnostic only: it may support observability, explainability, and failure analysis, but it does not change benchmark membership or create paper metrics.

## Canonical Case Evidence

- Source SQL: `source.sql`
- Canonical positive rewrite (legacy): `rewrite_pos_01.sql`
- Baseline positive rewrite (preferred positive control): `pos_baseline.sql`
- Canonical hard-negative rewrite: `rewrite_neg_01.sql`
- Manifest: `manifest.yaml`
- Taxonomy: `taxonomy_trial_v0.2.yaml`
- Supporting evidence: `data_profile.json`
- Retained evidence: `analysis/`, `metadata/`, `provenance/`, `schema/`, `validation/`, `runs/`

## Audit Procedure

1. Read the source SQL, legacy positive rewrite, baseline positive rewrite, hard-negative rewrite, manifest, taxonomy or metadata, validation assets, and retained evidence before judging a candidate.
2. Use the atoms below; they are derived by comparing `source.sql`, `rewrite_pos_01.sql`, `pos_baseline.sql`, and `rewrite_neg_01.sql`, not from the candidate under review.
3. Mark each atom as `satisfied`, `partially_satisfied`, `missing`, or `violated`, with SQL-span evidence where possible.
4. Compute operation coverage from operation atoms only.
5. Treat semantic guard atoms as validity gates. A high-risk missing or violated guard sets the final observability score to zero while preserving raw operation coverage for diagnosis.
6. Do not claim speedup, admission, or paper-facing metric changes from this audit alone.

## Atom Protocol

Preferred positive-control basis: `pos_baseline.sql`; legacy positive evidence: `rewrite_pos_01.sql`; hard-negative boundary: `rewrite_neg_01.sql`. The atom rows below should be judged against operations and guards visible in the positive controls, with the negative rewrite used to identify semantic failure boundaries.

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| A1 | `operation_atom` | `filter_stage_extraction` | medium | 1.0 | Candidate moves the source `lineitem` filtering or qualifying-row selection into a staged relation such as a derived table or CTE. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A2 | `operation_atom` | `projection_pruning_or_expression_precompute` | medium | 1.0 | Candidate stages only columns needed by downstream grouping and aggregate expressions, or precomputes equivalent aggregate inputs before aggregation. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A3 | `operation_atom` | `aggregate_input_rebinding` | medium | 1.0 | Candidate rebinds the downstream `SUM`, `AVG`, and `COUNT` aggregates to the staged filtered relation rather than scanning the base relation directly. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A4 | `semantic_guard_atom` | `shipdate_predicate_preservation` | high | 1.0 | Candidate preserves the source ship-date filter boundary `l_shipdate <= DATE '1998-08-27'` and does not exclude rows shipped exactly on that date. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A5 | `semantic_guard_atom` | `relational_boundary_preservation` | high | 1.0 | Candidate preserves selected columns, aggregate definitions, grouping by `l_returnflag` and `l_linestatus`, ordering, and result boundaries. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |

Status values:

| status | score value | meaning |
|---|---:|---|
| `satisfied` | 1.0 | clear SQL span or canonical evidence supports the atom |
| `partially_satisfied` / `uncertain` | 0.5 | incomplete implementation or incomplete evidence |
| `missing` | 0.0 | expected atom is absent |
| `violated` | 0.0 | candidate changes a semantic guard in a result-changing way |

## Required Candidate Annotation Shape

Return valid JSON if an LLM or human reviewer provides an external annotation:

```json
{
  "schema_version": "llm_annotation_v1",
  "case_id": "PERF_0006",
  "baseline_method_id": "<method>",
  "target_engine": "<engine>",
  "annotation_protocol": "skills.md",
  "canonical_positive_paths": ["rewrite_pos_01.sql", "pos_baseline.sql"],
  "hard_negative_path": "rewrite_neg_01.sql",
  "atoms": [
    {
      "atom_id": "A1",
      "category": "operation_atom | semantic_guard_atom",
      "type": "filter_stage_extraction",
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
