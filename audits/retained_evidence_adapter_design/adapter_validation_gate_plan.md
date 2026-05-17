# Adapter Validation Gate Plan

Date: 2026-05-17

## Purpose

Define validation gates that future retained-evidence adapters must pass before any metrics computation or paper table rendering is considered.

This plan does not implement adapters or compute metrics.

## Stage 1: Input Manifest Checks

- Confirm `case_sets/common_core_v0/cases.csv` has 40 rows.
- Confirm `denominator_same_engine_120.csv` has 120 planned rows.
- Confirm `controls_360.csv` has 360 planned control rows.
- Confirm `inventory/case_registry.csv` includes the 40 Common-core cases.
- Confirm retained-evidence maps are present and readable.
- Confirm no adapter writes to legacy paths or case-local `runs/`.

Failure behavior: stop adapter run and emit a validation failure report.

## Stage 2: Row Count And Identity Checks

- Count rows by `record_type`.
- Count rows by `case_set`, `pool`, `engine`, `route`, and `method_role`.
- Check that every emitted row has a stable `candidate_id` or artifact identifier.
- Check uniqueness for each record-type grain.
- Check that failed, unsupported, timing-missing, and manual-review rows are represented explicitly.

Failure behavior: reject duplicate-grain outputs unless explicitly marked as multiple candidates.

## Stage 3: Denominator Join Checks

- `rewrite_candidate_cell` rows in same-engine scope must join to `denominator_same_engine_120.csv` when denominator eligible.
- `control_cell` rows must join to `controls_360.csv`.
- `portability_candidate_cell` rows must not reuse Track A denominator IDs unless a future portability denominator policy authorizes it.
- `plan_observability_artifact`, `verifier_support_pair`, and `retained_summary_artifact` rows must not use same-engine performance denominator IDs by default.

Failure behavior: block output from metric computation and require manual review.

## Stage 4: Record-type Required Field Checks

- Validate required fields for `control_cell`.
- Validate required fields for `rewrite_candidate_cell`.
- Validate required fields for `plan_observability_artifact`.
- Validate required fields for `portability_candidate_cell`.
- Validate required fields for `verifier_support_pair`.
- Validate required fields for `retained_summary_artifact`.
- Validate future `user_run_candidate_cell` only when public runner ingestion is authorized.

Failure behavior: reject rows with missing required identity fields. Preserve rows with missing evidence fields only if the missingness is explicit.

## Stage 5: No-global-leaderboard Guard

- Confirm outputs preserve `record_type`.
- Confirm route-specific and method-specific slices are not collapsed.
- Confirm controls are not mixed with rewrite candidates.
- Confirm verifier support is not counted as a rewrite baseline.
- Confirm plan artifacts are not counted as speedup denominator rows.

Failure behavior: reject aggregation output and block metrics computation.

## Stage 6: No-metric-computation Guard

The adapter layer may normalize retained values but must not compute:

- Generation Rate.
- Execution Coverage Rate.
- Result Consistency Rate.
- Semantic Equivalence Rate.
- GM_Speedup.
- Speedup Ratio Percentiles.
- Attribution Coverage.
- Cross-Engine Execution.
- Cross-Engine Consistency.
- Speedup Retention.
- Regression@20 diagnostics.

Failure behavior: reject adapter output that contains aggregate metric rows or rendered paper-table values.

## Stage 7: No Reports/Results Mutation Guard

- Confirm no release `reports/` or `results/` files are created by adapter design or dry-run tasks unless a later reports/results migration task authorizes them.
- Confirm no legacy reports/results files are copied or modified.
- Confirm `copy_now=false` retained candidates remain unchanged.

Failure behavior: stop and report unauthorized mutation.

## Stage 8: Public Hygiene Guard

If a future adapter writes public outputs, scan for:

- absolute local paths;
- raw stdout/stderr paths;
- WSL or host-specific traces;
- localhost or private endpoint traces;
- API keys or token-like strings;
- prompt or model trace leakage;
- unsanitized raw logs.

Failure behavior: block public output publication until sanitized or marked private/archive-only.

## Stage 9: Review Gate Before Metrics

Before metrics computation:

- Adapter output schema must be approved.
- Row-grain validation must pass.
- Denominator joins must pass.
- Metrics Contract v1 must remain the active contract.
- Paper table rendering must be separately authorized.

Failure behavior: metrics implementation remains blocked.
