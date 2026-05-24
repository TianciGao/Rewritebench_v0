# Track A 120 Tag-Aware Failure Slices

Task: `track_a_120_tag_failure_slices_v0`

Routes analyzed:

- `direct_llm_original` / `direct_llm_original_track_a_120_canonical_v0`
- `sqlglot_noop` / `sqlglot_noop_track_a_120_canonical_v0`
- `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`
- `calcite_hep_fail_closed` / `calcite_hep_track_a_120_canonical_v0`

Input artifacts used:

- Existing source-run `ledger.csv`, `failures.csv`, `tag_slices.csv`, and `selected_cases.csv` under `runs/user/`.
- Existing inventory packet `audits/track_a_120_existing_baseline_evidence_inventory_v0/`.
- Case manifest taxonomy referenced by `selected_cases.csv`, used only to recover the same retained taxonomy consumed by `tag_slices.py` for per-case diagnostic joins.

Outputs created:

- `route_tag_slice_summary.csv`
- `route_failure_by_tag.csv`
- `route_failure_by_axis.csv`
- `non_exact_frontier_by_tag.csv`
- `cross_route_failure_hotspots.md`
- per-route diagnostic notes
- `schema_notes.md`
- `tag_failure_boundary.md`
- `command_log.txt`
- `validation_notes.md`

Top diagnostic findings:

- Direct LLM mismatch tags concentrate around dialect_adaptation=5, null_semantics_gap=3, subquery_decorrelation=3, correlated_subquery=3, identifier_quoting=3, literal_predicate_boundary=3, type_semantics_gap=3, date_filter_semantics=2.
- SQLGlot optimize execution/unsupported frontier tags concentrate around dialect_adaptation=8, correlated_subquery=6, date_time_semantics=4, type_coercion=4, expression_complexity=4, subquery_in_from=3, subquery_decorrelation=3, outer_join=3.
- Calcite HEP fail-closed frontier tags concentrate around dialect_adaptation=24, identifier_quoting=14, date_time_semantics=9, type_semantics_gap=8, expression_complexity=8, literal_predicate_boundary=7, type_coercion=7, limit_fetch_gap=6.
- MySQL mismatch and Spark unsupported/execution frontiers show different profiles: MySQL is mismatch-heavy, while Spark carries unsupported/execution/no-candidate boundary rows.

Reruns needed: no. Existing ledgers, failures, tag slices, and manifest taxonomy references are sufficient for this diagnostic slice analysis.

Next safe action: proceed to verifier-phase exact-candidate pair inventory/materialization design or bounded verifier pass planning, without running Repair-1 yet.
