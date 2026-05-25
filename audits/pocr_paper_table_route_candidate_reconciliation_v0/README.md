# POCR Paper Table Route Candidate Reconciliation v0

This packet reconciles the paper-facing Table 1 route rows against existing local candidate SQL roots. It uses `audits/pocr_candidate_sql_inventory_v0/` as the source map and performs only targeted read-only checks.

No candidate SQL was moved, copied, deleted, normalized, regenerated, or rewritten. No live API call, annotation JSONL generation, DB/checker/timing run, baseline rerun, official POCR computation, route-level POCR aggregation, paper metric promotion, or leaderboard generation occurred.

## Routes Reconciled

- Track A 120: Direct LLM original
- Track A 120: Direct LLM + Repair-1
- Track A 120: SQLGlot no-op
- Track A 120: SQLGlot optimize schema-aware
- Track A 120: Calcite HEP fail-closed
- PG40 prior: LearnedRewrite
- PG40 prior: R-Bot adapted GPT-5.4
- PG40 prior: LLM-R2 adapted GPT-5.4

## Main Findings

Direct LLM original and Direct LLM Repair-1 have complete tri-engine candidate-root families for Track A 120. They are candidates for future diagnostic Track A 120 POCR annotation generation, but Table 1 POCR remains N.A. because no tri-engine annotation JSONL and no official POCR promotion are authorized.

SQLGlot no-op has a complete PostgreSQL-only PG40 control root at `runs/user/common_core_pg_noop_db_checker/candidate_sql`, but its canonical Track A 120 candidate roots are incomplete. PG40 no-op evidence cannot fill a Track A 120 POCR cell.

SQLGlot optimize schema-aware and Calcite HEP fail-closed have incomplete candidate SQL roots for both PG40 and Track A 120. They require a no-candidate/fail-closed artifact policy before any POCR diagnostic annotation attempt.

For PG40 prior methods, R-Bot adapted GPT-5.4 and LLM-R2 adapted GPT-5.4 have complete PG40 candidate roots. LearnedRewrite has only 29 generated PG40 candidate files and cannot support full-denominator PG40 POCR without a separately scoped no-candidate policy.

## Next Recommended Route

If POCR work continues, the safest next route is Direct LLM Repair-1 PostgreSQL PG40 diagnostic annotation generation plus user-facing replay. It has a complete PostgreSQL Common-core candidate root and avoids immediately expanding to the full Track A 120 tri-engine denominator.
