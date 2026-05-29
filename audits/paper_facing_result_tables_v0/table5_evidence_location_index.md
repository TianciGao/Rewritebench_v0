# Table 5. Evidence Location Index

| evidence_area | method_or_route | scope | audit_packet_path | canonical_metric_source | tables_supported | status | claim_boundary |
|---|---|---|---|---|---|---|---|
| Track A 120 canonical metrics | direct_llm_original | Track A same-engine 120 | `audits/direct_llm_original_track_a_120_canonical_user_rerun_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 4; Table 5 | complete local diagnostic | local diagnostic only |
| Track A 120 canonical metrics | direct_llm_repair_1 | Track A same-engine 120 | `audits/direct_llm_repair_1_track_a_120_canonical_user_rerun_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 4; Table 5 | complete local diagnostic | local diagnostic only |
| Track A 120 canonical metrics | sqlglot_noop | Track A same-engine 120 | `audits/sqlglot_noop_track_a_120_canonical_user_rerun_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 4; Table 5 | complete local diagnostic | local diagnostic only |
| Track A 120 canonical metrics | sqlglot_optimize_schema_aware | Track A same-engine 120 | `audits/sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 4; Table 5 | complete local diagnostic | local diagnostic only |
| Track A 120 canonical metrics | calcite_hep_fail_closed | Track A same-engine 120 | `audits/calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 4; Table 5 | complete local diagnostic | local diagnostic only |
| PG40 prior-method metrics | learnedrewrite | PostgreSQL Common-core 40 | `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 3; Table 4; Table 5 | complete bounded diagnostic | not Track A 120 |
| PG40 prior-method metrics | rbot_gpt54_adapted | PostgreSQL Common-core 40 | `audits/rbot_gpt54_pg40_bounded_local_diagnostic_rerun_with_metrics_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 3; Table 4; Table 5 | complete bounded diagnostic | not original R-Bot reproduction |
| PG40 prior-method metrics | llm_r2_gpt54_adapted | PostgreSQL Common-core 40 | `audits/llm_r2_gpt54_pg40_bounded_local_diagnostic_v0` | `local_metrics_summary_review.md` | Table 1; Table 2; Table 3; Table 4; Table 5 | complete bounded diagnostic | not original LLM-R2 reproduction |
| Failure/tag slice packet | Track A 120 routes | Track A same-engine 120 | `audits/track_a_120_tag_failure_slices_v0` | N.A. | Table 3; Table 5 | complete diagnostic/support packet | not Positive Operation Coverage Rate |
| Failure/tag slice packet | PG40 prior methods | PostgreSQL Common-core 40 | `audits/prior_methods_pg40_tag_failure_slices_v0` | N.A. | Table 3; Table 5 | complete diagnostic/support packet | not Positive Operation Coverage Rate |
| Verifier/support | SQLSolver | coverage-limited verifier support | `audits/sqlsolver_coverage_limited_boundary_v0` | N.A. | Table 1; Table 4; Table 5 | coverage_limited | not official Semantic Equivalence Rate |
| Verifier/support | VeriEQL | coverage-limited verifier support | `audits/verieql_support_layout_config_contract_v0` | N.A. | Table 1; Table 4; Table 5 | coverage_limited | not official Semantic Equivalence Rate |
| Metric contract patch | metrics_contract_d032_d033_patch_v0 | metrics contract | `audits/metrics_contract_d032_d033_patch_v0` | `repository_spec/metrics_contract_v1.md` | Table 1; Table 4; Table 5 | complete policy patch | no metric recomputation |
| Project control | migration control files | repository control | `project_control/` | N.A. | Table 5 | current | provenance only |

The full index, including route-boundary and frontier support packets, is in `table5_evidence_location_index.csv`.
