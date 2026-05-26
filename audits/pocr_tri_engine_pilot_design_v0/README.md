# POCR Tri-Engine Pilot Design v0

This is a design/readiness audit only.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

No API, annotation, replay, DB/checker/timing, or baseline rerun occurred.

POCR@planned and POCR@candidate remain D039 promotion views.

POCR@curated remains deferred until a predeclared curated manifest exists.

Pilot design result:
- Selected cases: `PERF_0006`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`, `LONGTAIL_0022`.
- Planned surface: 5 cases x 3 engines x 2 routes = 30 planned pilot route-engine rows.
- Routes: Direct LLM Repair-1 and SQLGlot no-op sanity/control.
- Engines: PostgreSQL, MySQL, Spark.
- Candidate-bound ready rows: 30/30.
- Blocked rows: 0/30.
- Fallback candidates proposed: no.

The pilot can proceed to a separately authorized checkpointed annotation/replay/aggregation run. This packet does not run that pilot.
