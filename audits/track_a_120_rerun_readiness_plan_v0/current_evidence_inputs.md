# Current Evidence Inputs

Required packets confirmed present:

- `audits/sqlglot_noop_pg_current_route_card_refresh_v0/`
- `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`
- `audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/`
- `audits/verieql_bound4_pg_noop_support_closeout_v0/`
- `audits/sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/`
- `audits/verifier_user_facing_rerun_contract_v0/`
- `audits/user_surface_d035_layout_inventory_v0/`
- `audits/d035_user_docs_output_wording_cleanup_v0/`

Additional evidence reviewed:

- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/`
- `audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/`
- `audits/sqlglot_optimize_cons0005_triage_v0/`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/`
- `baselines/sqlglot/README.md`
- `baselines/calcite_hep_fail_closed/README.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`

Evidence boundaries:

- PostgreSQL route-card evidence for SQLGlot noop and Calcite HEP is current and D035-shaped.
- SQLGlot noop tri-engine evidence exists, but MySQL/Spark route-card evidence is older than the current PG D035 refresh.
- Calcite HEP MySQL/Spark evidence is not current and remains blocked for full Track A.
- Verifier evidence is support-layer evidence only; it does not make a rewrite route ready.
