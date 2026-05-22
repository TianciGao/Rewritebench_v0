# Metric Definitions Used

Definitions follow D033.

## Coverage

- Generation Rate: `candidate_generated / selected`.
- Execution Coverage Rate: `candidate_executable / selected`.

`preflight_passed` is recorded as a funnel diagnostic and is not part of Generation Rate.

`source_executable` is recorded as a diagnostic/environment guard and is not a numerator condition for Execution Coverage Rate.

## Correctness

- Result Consistency Rate: `exact / selected`.

`label_only_mismatch` remains mismatch under the strict-label policy and is not counted as exact.

## Performance

- GM Speedup Ratio: geometric mean of `speedup_ratio` over strict exact + timed rows only.
- Speedup Ratio Percentiles: P10, P25, P50, P75, P90 over strict exact + timed rows only.

Rows are excluded from performance if they are non-exact, label-only mismatches, unsupported/fail-closed, not timed, partial timing failures, or have missing/non-positive speedup or median values.

## N.A. / Deferred

- Semantic Equivalence Rate: `N.A.` without formal verifier evidence.
- Cross-Engine GM Speedup Ratio: `N.A.` without target-engine paired timing.
- POCR: deferred, `skill_adapter_pending=true`.
- Regression@20: not implemented in formal local metrics v0.
