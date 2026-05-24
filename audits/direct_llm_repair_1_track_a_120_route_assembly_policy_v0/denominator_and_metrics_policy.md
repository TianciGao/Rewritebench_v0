# Denominator And Metrics Policy

## Denominator

The selected/planned denominator for the future Repair-1 Track A local diagnostic remains 120 rows:

```text
40 common-core v0 cases x 3 same-engine targets = 120 selected rows
```

Rows are not removed when original Direct LLM failed, when Repair-1 is not attempted, when a row is unsupported, or when a final candidate fails closed.

## Local metric formulas

After the future 120 run, `local_metrics.py` remains the only canonical calculator for local diagnostic route metrics.

Required formulas for the route card:

```text
Generation Rate = final_candidate_generated / selected
Execution Coverage Rate = final_candidate_executable / selected
Result Consistency Rate = final_exact / selected
```

The final candidate can come from either:

- original Direct LLM candidate for original exact rows; or
- repaired candidate for Repair-1 attempted rows.

The numerator must be evaluated from the final Repair-1 route outputs, not copied from the Direct LLM original route.

## Performance

Performance remains exact-gated and timed-gated:

```text
GM Speedup Ratio: strict final exact + timed rows only
Speedup Ratio Percentiles: P10/P25/P50/P75/P90 over strict final exact + timed rows only
```

No speedup may be computed over incorrect, mismatch, execution-failed, unsupported, fail-closed, or timing-ineligible rows.

Regression@20 is not formal local metrics v0. It may appear only as separately labeled legacy/reporting diagnostic if separately authorized.

## SER and POCR

No official SER is computed by this route assembly policy.

SER remains `N.A.` or `coverage_limited` unless formal verifier evidence exists. Local result-checker exactness is Result Consistency evidence only and must not be used as SER evidence.

POCR remains deferred and must report `N.A.` or deferred unless separately authorized external operation-atom evidence exists.

## Boundary

The future 120 Repair-1 run and local metrics remain local diagnostic only unless a separate retained-evidence or paper-promotion task authorizes promotion. Local metric outputs must not update top-level `reports/`, top-level `results/`, paper files, retained evidence, denominators, or case membership.
