# SQLGlot Optimize Missing Rows Review

SQLGlot optimize schema-aware remains candidate-present only. Missing optimize candidates remain fail-closed for POCR@planned and no-op substitutions were not used.

- postgres: candidate rows present 34/40; missing cases: CONS_0009;PORT_0004;PORT_0013;PORT_0022;PORT_0024;PORT_0025
- mysql: candidate rows present 32/40; missing cases: PERF_0008;PERF_0013;PERF_0017;PERF_0019;CONS_0005;CONS_0009;CONS_0010;CONS_0011
- spark: candidate rows present 39/40; missing cases: CONS_0009

The route is safe to include as a diagnostic route with fail-closed missing rows, but MySQL and Spark annotation quality requires targeted retry or provider-quality review before any paper-facing promotion review.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@curated remains deferred until a predeclared curated manifest exists.
