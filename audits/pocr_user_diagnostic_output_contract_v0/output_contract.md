# Diagnostic POCR Output Contract

The diagnostic row schema is implemented by `POCRDiagnosticRow` in `src/sql_rewrite_bench/pocr/diagnostic_output_schema.py`.

Required row fields:
- `run_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_path`
- `candidate_present`
- `skill_present`
- `annotation_status`
- `stage_b_status`
- `expected_operation_atoms_count`
- `stage_a_implemented_operation_atoms_count`
- `transformation_supported_operation_atoms_count`
- `presence_only_operation_atoms_count`
- `insufficient_transformation_evidence_operation_atoms_count`
- `rejected_noop_equivalent_operation_atoms_count`
- `schema_invalid_atoms_count`
- `semantic_guard_atoms_count`
- `diagnostic_only`
- `official_pocr_computed`
- `route_level_pocr_aggregated`
- `paper_metric_promoted`
- `boundary_notes`

Required constants:
- `diagnostic_only=true`
- `official_pocr_computed=false`
- `route_level_pocr_aggregated=false`
- `paper_metric_promoted=false`

The user-output adapter writes only under a caller-provided output root:
- `output/results/<run_id>/pocr/diagnostic_rows.csv`
- `output/results/<run_id>/pocr/diagnostic_summary_by_pool.csv`
- `output/logs/<run_id>/pocr/pocr_diagnostic.log`
- `output/reports/<run_id>/pocr_diagnostic.md`

For repository tests, these paths are written under a temporary output root only. The task did not create or commit `output/`, top-level `reports/`, top-level `results/`, or case-local `runs/` outputs.

The Markdown report must state that this is Positive Operation Coverage diagnostic support, not official POCR; Stage A annotation alone is not counted; Stage B transformation-aware validation is diagnostic only; semantic guard atoms are not part of the operation coverage numerator; and no route-level POCR score is emitted.
