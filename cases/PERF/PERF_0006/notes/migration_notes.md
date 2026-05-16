# PERF_0006 Migration Notes

Date: 2026-05-16

This is a copy-first canonical-layout migration for `PERF_0006` only. Legacy source files and raw retained evidence remain unchanged in the legacy repo and are mapped through `evidence/runs_retention.yaml`.

The migration preserves the performance boundary: no timing run was executed, no speedup was computed, no ranking was created, and no paper-result claim changed. The hard negative changes the cutoff predicate from less-than-or-equal to strict less-than, excluding the cutoff-date witness row.

Raw Spark plan text was not published as retained public evidence because it contained local temporary Spark path traces. Sanitized plan derivatives are published under `evidence/retained_plans/spark/` and original raw legacy plans remain do-not-delete mapped evidence.

Validation scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner output must not write to case-local runs/ by default.

Denominator unchanged. Paper results unchanged. Common-core membership unchanged. Raw legacy evidence unchanged. No global leaderboard is introduced.
