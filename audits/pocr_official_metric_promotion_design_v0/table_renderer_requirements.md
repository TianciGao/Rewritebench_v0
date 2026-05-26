# Table Renderer Requirements

No top-level `reports/` or `results/` files are updated in this task. Future renderer output must be separately authorized.

A future POCR table renderer should include:

| Column | Purpose |
| --- | --- |
| `route_id` | Route identity used for replay and aggregation. |
| `method_id` | Method identity. |
| `scope` | PG40, Track A 120, curated, or other predeclared scope. |
| `planned_rows` | Planned denominator rows. |
| `generated_rows` | Rows with generated or captured candidate output. |
| `candidate_bound_rows` | Rows with deterministic candidate identity. |
| `executed_rows` | Execution rows when available from a separate metric layer. |
| `exact_rows` | Exact rows when available from a separate metric layer. |
| `timed_rows` | Timed rows when available from a separate metric layer. |
| `expected_operation_atoms` | Count of operation atoms from `skills.md`. |
| `stage_b_supported_operation_atoms` | Count of Stage-B-supported operation atoms. |
| `POCR@planned` | Planned-denominator macro view. |
| `POCR@candidate` | Candidate-bound macro view. |
| `POCR@curated_status` | `NA` / `curated_manifest_missing` until frozen curated manifest exists. |
| `annotation_valid_rate` | Annotation schema-valid rows over attempted rows. |
| `fail_closed_annotation_rows` | Annotation rows retained as fail-closed. |
| `no_candidate_rows` | Planned rows without candidate SQL. |
| `possible_overaccept_cases` | Manual-review count for possible over-accept. |
| `boundary` | Diagnostic, pilot, official-promotion candidate, or frozen paper-facing. |

The renderer must keep POCR beside generation, execution, exact, and timed denominators. It must not imply that POCR measures correctness or speed.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required. Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
