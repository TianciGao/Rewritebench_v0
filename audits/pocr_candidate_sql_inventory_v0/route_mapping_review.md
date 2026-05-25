# Route Mapping Review

The inventory scanned every existing `runs/user/**/candidate_sql` directory read-only.

## Summary

- Candidate roots inventoried: 1,660.
- Candidate files inventoried: 2,377.
- PG40-complete PostgreSQL roots: 5.
- Track-A-120-complete route-family component roots: 6.
- Ambiguous roots: 1,579.

The `track_a_120_complete` column marks roots whose source-run family has complete 40-case coverage for `postgres`, `mysql`, and `spark` across companion per-engine candidate roots. It does not mean a single per-engine root contains 120 files.

## PG40-Complete PostgreSQL Roots

- `runs/user/common_core_pg_noop_db_checker/candidate_sql/`
  Inferred method: `sqlglot_noop`. Scope: PostgreSQL no-op sanity/control root.

- `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql/`
  Inferred method: `direct_llm_original`. Scope: canonical Track A PostgreSQL component; already used for Direct LLM PG40 POCR diagnostic replay.

- `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql/`
  Inferred method: `direct_llm_repair_1`. Scope: canonical Track A PostgreSQL component; recommended next real-route diagnostic candidate.

- `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/`
  Inferred method: `llm_r2_gpt54_adapted`. Scope: PostgreSQL-only PG40 prior-method manual-inspection rerun.

- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/`
  Inferred method: `rbot_gpt54_adapted`. Scope: PostgreSQL-only PG40 prior-method bounded diagnostic rerun.

## Track A 120 Complete Route Families

Complete tri-engine candidate families were found for:

- `direct_llm_original_track_a_120_canonical_v0`
- `direct_llm_repair_1_track_a_120_canonical_v0`

Each family has 40 Common-core candidate SQL files for each of `postgres`, `mysql`, and `spark`.

Other Track A candidate roots are present but not complete as preserved candidate SQL roots:

- `sqlglot_noop_track_a_120_canonical_v0`: `mysql=40`, `postgres=35`, `spark=40`.
- `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`: `mysql=32`, `postgres=34`, `spark=39`.
- `calcite_hep_track_a_120_canonical_v0`: `mysql=33`, `postgres=33`, `spark=33`.

Those missing candidate files correspond to fail-closed or no-candidate rows; they remain visible in existing canonical audit metrics, but there is no per-case candidate SQL file to replay for those rows.

## Prior-Method Roots

- LearnedRewrite manual rerun root: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/` has 29 candidate SQL files. This preserves generated rows only; it is not PG40 complete as a file root.
- R-Bot adapted GPT-5.4 root: `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/` is PG40 complete.
- LLM-R2 adapted GPT-5.4 root: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/` is PG40 complete.

## Ambiguous Roots

Most ambiguous roots are unit-test artifacts or bounded smokes. They are inventoried for preservation visibility, but they should not be used for POCR route diagnostics without human selection.

Ambiguous roots are marked in `candidate_root_inventory.csv` with `ambiguous=yes`.

## Recommended First Real-Route Diagnostic After Inventory

The recommended next route is Direct LLM Repair-1 PostgreSQL PG40, using:

```text
runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql/
```

Reason:

- It is PG40 complete.
- Its tri-engine candidate family is complete.
- It is a direct companion to the already completed Direct LLM original POCR diagnostic.
- It provides the most useful near-term contrast for paper-aligned diagnostic support without expanding to a global leaderboard.
