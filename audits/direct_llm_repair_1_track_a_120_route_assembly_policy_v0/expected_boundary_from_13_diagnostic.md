# Expected Boundary From 13-Row Diagnostic

The completed 13-row live Repair-1 diagnostic is evidence that the actionable-frontier repair path works end to end on a bounded scope.

Observed diagnostic counts:

```text
selected rows: 13
unsupported excluded rows: 5
live calls: 13
repaired candidates generated: 13
extraction passed: 13
preflight passed: 13
source executable: 13
candidate executable: 13
exact: 9
mismatch: 4
candidate execution failed after repair: 0
timed exact rows: 9
fail closed rows: 0
```

The selected rows consisted of:

- 10 original `mismatch` rows
- 3 original `candidate_execution_failed` rows

The excluded rows consisted of:

- 5 original `unsupported_engine` Spark rows

Interpretation:

- These are not Track A 120 metrics.
- These counts must not be projected to official route results.
- These counts must not update paper reports or retained evidence.
- They justify proceeding to route assembly policy and then a separately authorized full 120 local diagnostic run.

Expected future effect:

- The 120 Repair-1 route should still include all 120 planned rows.
- Original exact rows should contribute final original candidates when rerun in the Repair-1 route.
- The 13 actionable rows should be eligible for live Repair-1 attempts.
- Unsupported rows should remain visible denominator rows.
