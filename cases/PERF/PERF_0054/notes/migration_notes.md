# PERF_0054 Migration Notes

Migration date: 2026-05-16.

This package was migrated with a copy-first canonical layout principle. Public-safe files were copied from the legacy case package; generated metadata summarizes retained legacy facts only. Legacy repo unchanged: yes. Raw legacy evidence unchanged: yes.

Performance boundary: no timing run was executed, and no speedup, latency, timing, ranking, leaderboard, denominator, or paper-result claim is created by this migration.

Hard-negative static explanation: changes the item manufacturer predicate from 436 to 437. Expected rejection reason: `manufacturer_id_predicate_changed`. Approval status: migration planning static inference needs review if not explicit in legacy.

Spark plan sanitization: Sanitized Spark plan copies were generated under evidence/retained_plans/spark/; raw Spark plan text remains mapped as do-not-delete legacy evidence and was not copied raw.

Validation script output-policy caveat: copied/adapted scripts are retained legacy validation assets, were not executed during migration, and future public runners should write outputs outside case-local runs by default.

Denominator unchanged: yes. Paper results unchanged: yes. Common-core membership unchanged: yes.
