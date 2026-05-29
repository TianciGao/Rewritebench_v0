# Baseline Rewrite Audit Skill
<!-- skills to compute metric "Positive Operation Coverage" -->
<!-- generated-by: tools/baseline_audit/run_case_audit.py develop -->

## Scope
- case_id: `PERF_0052`
- pool: `PERF`
- opportunity_family: `customer_total_return_cte_threshold_rewrite`

Use this file when reviewing a baseline-produced SQL rewrite candidate for this case. The audit is diagnostic only and does not change benchmark membership or create paper metrics.

## Canonical Case Evidence
- Source SQL: `source.sql`
- Canonical positive rewrite (legacy): `rewrite_pos_01.sql`
- Baseline positive rewrite (preferred positive control): `pos_baseline.sql`
- Canonical hard-negative rewrite: `rewrite_neg_01.sql`
- Manifest: `manifest.yaml`
- Supporting evidence: `data_profile.json`
- Retained evidence: `provenance/`, `schema/`, `validation/`, `runs/`

## Audit Procedure
1. Read source, legacy positive, baseline positive, negative, manifest, validation assets, and retained evidence before judging a candidate.
2. Use the atoms below; they are derived by comparing `source.sql`, `rewrite_pos_01.sql`, `pos_baseline.sql`, and `rewrite_neg_01.sql`, not from the candidate under review.
3. Mark each atom as `satisfied`, `partially_satisfied`, `missing`, or `violated`, with SQL-span evidence where possible.
4. Compute operation coverage from operation atoms only.
5. Treat high-risk semantic guards as validity gates.
6. Do not claim speedup, admission, or paper-facing metric changes from this audit alone.

## Atom Protocol

Preferred positive-control basis: `pos_baseline.sql`; legacy positive evidence: `rewrite_pos_01.sql`; hard-negative boundary: `rewrite_neg_01.sql`. The atom rows below should be judged against operations and guards visible in the positive controls, with the negative rewrite used to identify semantic failure boundaries.

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| A1 | `operation_atom` | `customer_total_return_cte_preservation` | medium | 1.0 | Candidate preserves the CTE that groups store returns by customer and store. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A2 | `operation_atom` | `store_threshold_subquery_preservation` | medium | 1.0 | Candidate preserves the store-level average return threshold comparison. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A3 | `operation_atom` | `customer_store_join_rebinding` | medium | 1.0 | Candidate joins the CTE result to customer, store, and address metadata using equivalent keys. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A4 | `semantic_guard_atom` | `return_year_and_state_preservation` | high | 1.0 | Candidate preserves return year and state filters. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |
| A5 | `semantic_guard_atom` | `threshold_multiplier_and_order_preservation` | high | 1.0 | Candidate preserves the threshold multiplier, output columns, ordering, and limit. Positive-control basis: `pos_baseline.sql` and `rewrite_pos_01.sql`; semantic boundary: `rewrite_neg_01.sql`. |

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
  "case_id": "PERF_0052",
  "baseline_method_id": "<method>",
  "target_engine": "<engine>",
  "annotation_protocol": "skills.md",
  "canonical_positive_paths": ["rewrite_pos_01.sql", "pos_baseline.sql"],
  "hard_negative_path": "rewrite_neg_01.sql",
  "atoms": [
    {
      "atom_id": "A1",
      "category": "operation_atom | semantic_guard_atom",
      "type": "customer_total_return_cte_preservation",
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
