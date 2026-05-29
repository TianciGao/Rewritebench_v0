# Nightly User Reproduction SQLGlot/Calcite Track A 120 Metrics

This packet records local diagnostic user-side reproduction for SQLGlot no-op, SQLGlot optimize schema-aware, and Calcite HEP fail-closed over Common-core v0 Track A 120.

It is not POCR annotation generation, not official paper metric promotion, not a global leaderboard, and it does not update top-level reports/results.

## Route Summary

- sqlglot_noop: planned 120, generated 115, executable 107, exact 97, timed 97, GM 1.0580321436582178, RCR 0.8083333333333333.
- sqlglot_optimize_schema_aware: planned 120, generated 105, executable 91, exact 66, timed 66, GM 0.9893206632563172, RCR 0.55.
- calcite_hep_fail_closed: planned 120, generated 0, executable 0, exact 0, timed 0, GM N.A., RCR 0.0.

Local D035 outputs were written under `output/` and intentionally left uncommitted.
