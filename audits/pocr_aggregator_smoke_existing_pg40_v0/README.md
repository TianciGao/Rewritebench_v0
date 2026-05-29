# POCR Aggregator Smoke Existing PG40 v0

This audit records a no-API smoke of the POCR row-metrics exporter plus POCR@planned / POCR@candidate aggregator over existing PostgreSQL PG40 diagnostic artifacts.

Routes checked:
- Direct LLM Repair-1 PostgreSQL PG40.
- SQLGlot no-op PostgreSQL PG40 sanity/control.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

This smoke verifies promotion-diagnostic POCR@planned / POCR@candidate aggregator behavior only.

POCR@curated remains deferred until a predeclared curated manifest exists.

Smoke result:
- Repair-1 reproduced `POCR@planned=0.395833333333`, `POCR@candidate=0.395833333333`, and diagnostic micro-average `0.383177570093`.
- SQLGlot no-op reproduced `POCR@planned=0.000000000000`, `POCR@candidate=0.000000000000`, and diagnostic micro-average `0.000000000000`.

No live API call, API key read, annotation JSONL generation, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, paper-facing reports/results update, retained-evidence promotion, or leaderboard output occurred.
