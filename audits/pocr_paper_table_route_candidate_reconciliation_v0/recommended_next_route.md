# Recommended Next Route

The recommended next POCR diagnostic annotation route is Direct LLM Repair-1 PostgreSQL PG40.

Reasons:

- It has a complete PostgreSQL Common-core candidate root at `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql`.
- It is a paper-facing Track A route family, but the PostgreSQL-only PG40 slice keeps the next diagnostic step bounded.
- Direct LLM original has already exercised the real-route diagnostic and user-facing replay path.
- A Repair-1 PG40 diagnostic can test whether the documented replay workflow generalizes to the repaired route before considering any tri-engine Track A 120 POCR pass.

This recommendation does not authorize live API calls, annotation generation, official POCR computation, route-level POCR aggregation, paper metric promotion, or candidate SQL movement. It only identifies the next route if a separately scoped diagnostic annotation task is approved.
