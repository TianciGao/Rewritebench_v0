# Non-Common-core Risk Summary

Date: 2026-05-17

## Runs Retention Risk

Detected cases with legacy `runs/`: 156 of 197. These require retention mapping before public migration. Case-local `runs/` remains legacy retained evidence and must not be deleted or overwritten.

## Local Path / Spark Plan Risk

Local path or host trace risk detected: 184 cases. Future migration must sanitize Spark plans and local-path traces or keep raw artifacts private/archive-only.

## Prompt/API/Token Risk

Prompt/API/token term risk detected: 0 cases. The static scan found no such cases, but future migration should still rescan selected batches.

## Raw Log / Debug Risk

Raw log/debug/tmp risk detected: 162 cases. Raw logs should not be copied into public retained evidence by default.

## Missing Package Assets

- Missing schema directory: 6 cases.
- Missing checker assets by static scan: 112 cases.

Missing checker assets do not automatically exclude a case, but they require checker/hard-negative review before canonical public migration.

## Duplicate / Alias / Unregistered Risk

Detected but unregistered directories: 7. These must be reconciled before staged/backlog membership.

## Paper Denominator Contamination Risk

The largest governance risk is accidentally treating non-Common-core cases as public v0 denominator rows. This audit keeps them outside Common-core v0 and writes no `case_sets/` files.

## Workload-frequency Overclaim Risk

Non-Common-core cases may contain useful structural or source-family coverage, but this audit does not create production-frequency, workload-frequency, ranking, leaderboard, speedup, or benchmark-result claims.
