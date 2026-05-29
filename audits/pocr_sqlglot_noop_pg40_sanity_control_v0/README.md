# SQLGlot No-Op PG40 POCR Sanity Control

SQLGlot no-op PostgreSQL PG40 was run as a diagnostic sanity/control route using the checkpointed POCR annotation runner and user-facing replay.

Selected candidate root: `runs/user/common_core_pg_noop_db_checker/candidate_sql`.

Candidate root readiness: ready, 40/40 Common-core PostgreSQL candidate files resolved read-only.

Annotation result: 40 manifest rows, 34 schema-valid rows, 5 malformed JSON rows, and 1 provider-call-failed rows.

Replay result: 40 diagnostic rows, 0 transformation-supported operation atoms, 15 presence-only operation atoms, 75 insufficient-transformation-evidence atoms, and 0 rejected-noop-equivalent atoms.

This is not official POCR.
No route-level POCR score is emitted.
No paper-facing metric is promoted.
Stage A annotation alone is not counted.
Stage B transformation-aware validation is diagnostic only.
Semantic guard atoms are not part of operation coverage numerator.
No global leaderboard is produced.
