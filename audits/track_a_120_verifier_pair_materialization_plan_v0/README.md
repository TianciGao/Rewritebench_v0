# Track A 120 Verifier Pair Materialization Plan

Task: `track_a_120_verifier_pair_materialization_plan_v0`

Routes covered:

- `direct_llm_original` / `direct_llm_original_track_a_120_canonical_v0`
- `sqlglot_noop` / `sqlglot_noop_track_a_120_canonical_v0`
- `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`
- `calcite_hep_fail_closed` / `calcite_hep_track_a_120_canonical_v0`

Exact/result-consistent pair counts:

- `direct_llm_original`: 102 eligible exact/result-consistent pairs
- `sqlglot_noop`: 97 eligible exact/result-consistent pairs
- `sqlglot_optimize_schema_aware`: 66 eligible exact/result-consistent pairs
- `calcite_hep_fail_closed`: 81 eligible exact/result-consistent pairs

Materialization readiness:

- `verifier_pair_inventory.csv` records all 480 selected route rows with exact/candidate/schema blockers where applicable.
- `verifier_pair_materialization_manifest.csv` records 346 eligible exact/result-consistent pairs using `path_reference_plus_hash` mode.
- No large SQL text was copied into the audit packet.
- Source SQL, candidate SQL, and schema references are recoverable for every eligible pair.

Likely first bounded verifier target: SQLSolver on a 5-10 pair deterministic subset of `sqlglot_noop` PostgreSQL exact pairs, with source-vs-source and candidate-vs-candidate identity guards.

Unresolved blockers:

- Exact-candidate user-facing verifier facade may need a separate implementation task if not already exposed.
- Non-PostgreSQL verifier modeling for MySQL and Spark remains deferred.
- VeriEQL remains coverage-limited based on prior notes and should follow SQLSolver-first planning.

Next safe action: authorize a bounded SQLSolver-first verifier pass on a small deterministic exact-pair subset, with identity guards and fail-closed boundary reporting, before broader verifier coverage or any Repair-1 execution.
