# Route Engine Readiness Matrix

The machine-readable matrix is:

- `track_a_route_engine_readiness_matrix.csv`

It contains 21 rows:

- 5 same-engine routes x 3 engines = 15 rows
- 2 support-layer tools x 3 engine contexts = 6 rows

Status vocabulary:

- `ready_local_diagnostic_rerun`: ready for local diagnostic rerun with fail-visible boundaries.
- `ready_pg_only_local_diagnostic`: PostgreSQL-only route-card path is ready, but full 120 is not.
- `partially_ready_bounded_smoke_only`: route has bounded evidence but needs current D035 route-card refresh before larger run.
- `partially_ready_support_layer`: support tool is integrated but blocked by user-facing run-candidates facade.
- `partially_ready_coverage_limited_support`: support tool is integrated but coverage/identity limits block promotion.
- `blocked`: route/tool should not be run at that scope until blockers are addressed.

Main conclusion:

- Only `sqlglot_noop` is ready for a first local diagnostic Track A 120 rerun candidate.
- No route is ready for paper-facing Track A evidence promotion.
