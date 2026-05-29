# PG40 vs Track A 120 Scope Review

PG40 diagnostic evidence cannot fill a Track A 120 row. PG40 uses only PostgreSQL Common-core cases and has a 40-row denominator. Track A 120 requires the tri-engine denominator across MySQL, PostgreSQL, and Spark for 120 rows.

Direct LLM original and Direct LLM Repair-1 PostgreSQL diagnostics are useful software diagnostics. They show that the POCR user-facing replay path can operate on PostgreSQL candidate roots, but they are not equivalent to tri-engine Track A 120 POCR.

To fill a Track A 120 POCR cell diagnostically, a route needs complete route-bound candidate SQL for all three engines, route-bound annotation JSONL covering the same denominator, transformation-aware Stage B validation, and a decision that any displayed value remains diagnostic-only unless official promotion is separately authorized.

To fill a PG40 prior-method POCR cell diagnostically, a route needs complete PostgreSQL Common-core candidate SQL, route-bound annotation JSONL for the same route label and case denominator, transformation-aware Stage B validation, and explicit PG40-only labeling.

No official Positive Operation Coverage Rate is computed in this task. No paper-facing metric is promoted. No route-level POCR aggregation is authorized here.
