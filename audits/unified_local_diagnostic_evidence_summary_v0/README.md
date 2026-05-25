# Unified Local Diagnostic Evidence Summary v0

This packet provides a compact evidence summary for paper writing without running experiments, recomputing metrics, rendering paper tables, or creating a leaderboard.

Included Track A 120 canonical local diagnostic routes:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_noop`
- `sqlglot_optimize_schema_aware`
- `calcite_hep_fail_closed`

Included PostgreSQL-only PG40 prior-method bounded evidence:

- `learnedrewrite`
- `rbot_gpt54_adapted`
- `llm_r2_gpt54_adapted`

Tables produced:

- `unified_route_evidence_ledger.csv`
- `failure_frontier_summary.csv`
- `tag_failure_summary.csv`
- `timing_slice_summary.csv`
- `evidence_location_index.csv`

Supporting notes:

- `paper_table_plan.md`
- `claim_extraction_notes.md`
- `no_leaderboard_boundary.md`

Next safe action: use this unified evidence summary to draft or update paper result tables and appendix artifact index. Do not run additional experiments unless a specific gap is identified.
