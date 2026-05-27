# No-Op Control Role Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

SQLGlot no-op is a candidate/control route, not a reference.

Checks:

- The PG40 pilot records SQLGlot no-op with `method_id=sqlglot_noop` and `route_id=sqlglot_noop_pg40_pocr_sanity_control`.
- The no-op candidate root is used as candidate SQL under evaluation, not as positive/reference SQL.
- The SQLGlot optimize boundary review explicitly states no-op candidates were not used as optimize substitutes.
- PG40 no-op row metrics reported `stage_b_supported_operation_atoms=0`.
- PG40 no-op possible over-accept cases: 0.
- Future no-op routes with transformation-supported operation atoms must enter manual review before any promotion.

Verdict: `pass`.

Boundary retained: SQLGlot no-op is a candidate/control route, not a reference.
