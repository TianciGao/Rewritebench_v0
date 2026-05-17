# Candidate Status Completion Round 1 Risk Register

## Overlap Policy Risk

A source-priority rule could accidentally let an enrichment source override a primary source. Mitigation: P003 may enrich Repair-1 failure fields only and must not override P002 success/exactness.

## SQLGlot No-Op Vs Optimize Route Confusion

SQLGlot source names use optimize, transpile, same-dialect, and no-op wording inconsistently. Future parser approval must map `route_id`/`method_id` deterministically to `sqlglot_optimize` or `sqlglot_noop`.

## Mixed PORT/Same-Engine Risk

Several SQLGlot files are marked `sqlglot;portability` in release metadata or use PORT-resolved paths. Future parser inputs must isolate Track-A same-engine rows only.

## Engine-Expansion Risk

P006 has `engines_eligible` rather than explicit engine rows. Expanding this to `case_id x engine` would be a policy decision, not a parser default.

## Timing Leakage Risk

P007 and P009 expose speedup/timing eligibility or runtime columns. Any future parser input must use a sanitized non-timing projection only.

## Route-Level Summary To Row-Level Risk

P010 is route-level aggregate only. Its counts must not be distributed into row-level statuses.

## Candidate-ID Derivation Risk

SQLGlot sources may use `rewrite_id`, `route_id`, `method_id`, or no explicit candidate id. Future parser approval must specify deterministic candidate-id construction or leave rows unresolved.

## Evidence Pointer Hygiene Risk

SGL011/SGL012 and P009 contain artifact/path pointer columns. Future parser use must keep pointers as strings only and must not open raw payloads.

## Raw Log Debug Risk

SGL013 contains `stdout_log` and `stderr_log` columns. Direct parser use is unsafe unless a sanitized projection removes those columns.

## Risk Of Converting Dry-Run Into Official Metric Too Early

Existing dry-run and inference outputs are audit-only. Official metrics remain blocked until separate metric-readiness and computation authorization.
