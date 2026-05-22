# Formula Decision Summary

## Coverage

- Generation Rate: `candidate_generated / selected`.
- Execution Coverage Rate: `candidate_executable / selected`.

`preflight_passed` remains a funnel diagnostic. It is not part of Generation Rate.

`source_executable` remains an environment guard and diagnostic. It is not a numerator condition for Execution Coverage Rate.

## Correctness

- Result Consistency Rate: `exact / selected`.

`label_only_mismatch` remains mismatch under the strict-label policy and must not be counted as exact.

## Semantic Equivalence

Semantic Equivalence Rate is `N.A.` unless formal verifier evidence exists. Local result checker exactness is result consistency evidence, not formal semantic equivalence verification.

## Performance

- GM Speedup Ratio is computed only over strict exact + timed rows.
- Speedup Ratio Percentiles are computed only over strict exact + timed rows.

Rows without complete local timing artifacts are not in the timed performance denominator.

## Cross-Engine Performance

Cross-Engine GM Speedup Ratio replaces old Speedup Retention in latest-paper alignment. It is `N.A.` unless target-engine paired timing exists.
