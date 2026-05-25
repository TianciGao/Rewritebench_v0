# Recommended Next Routes

This file recommends a diagnostic-only order for later POCR annotation-generation and replay tasks. It does not authorize running any route.

## Recommended Order

1. Direct LLM Repair-1 PostgreSQL PG40
   - Candidate root: `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql/`
   - Reason: PG40 complete and tri-engine family complete; direct comparison with the completed Direct LLM original diagnostic.

2. Direct LLM original additional replay or route-bound documentation, only if needed
   - Candidate root: `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql/`
   - Reason: already used for real-route POCR diagnostic; further work should avoid duplicate live annotation unless a gap is identified.

3. SQLGlot no-op PostgreSQL sanity control
   - Candidate root: `runs/user/common_core_pg_noop_db_checker/candidate_sql/`
   - Reason: PG40 complete source-like/no-op control. It is useful for validating that transformation-aware Stage B does not over-accept source preservation.

4. R-Bot and LLM-R2 PostgreSQL prior-method bounded routes
   - Candidate roots:
     - `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/`
     - `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/`
   - Reason: PG40 complete prior-method candidate SQL roots exist, but they are PostgreSQL-only bounded evidence and not Track A 120.

5. LearnedRewrite generated-row diagnostic only
   - Candidate root: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/`
   - Reason: 29 generated candidate files exist; missing candidate rows must remain visible as no-candidate/fail-closed rows.

6. SQLGlot optimize and Calcite HEP only after output-contract planning
   - Reason: canonical candidate roots are incomplete as file roots. A future diagnostic runner must explicitly represent missing candidate rows rather than silently dropping them.

## Non-Authorization Boundary

This recommendation does not authorize live API calls, annotation JSONL generation, baseline reruns, DB/checker/timing, official POCR computation, route-level aggregation, paper metric promotion, retained-evidence promotion, reports/results updates, or leaderboard output.
