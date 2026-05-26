# Quality Gate Plan

Required gates before a future pilot can expand toward Track A 120:

- Candidate root readiness reviewed for all 30 planned rows.
- Route mismatch rows must be 0 or fail-closed and manually reviewed.
- Candidate mismatch rows must be 0 or fail-closed and manually reviewed.
- SQLGlot no-op possible over-accept must be 0 or fully justified.
- Schema-valid or fail-closed rows must be fully accounted.
- MySQL/Spark evidence refs must not over-accept dialect-only spans.
- Stage A annotation alone is not counted.
- Stage B transformation-aware validation is required.
- Semantic guard atoms remain excluded from operation coverage numerator and denominator.
- POCR@curated remains NA.
- No official POCR or paper metric is allowed until a separate promotion freeze.

Additional review gates:
- inspect any no-op transformation-supported atoms before promotion;
- inspect high Repair-1 support on non-exact or unknown-correctness rows;
- retain provider failures and malformed JSON rows explicitly after retry;
- compare macro POCR@planned / POCR@candidate to diagnostic micro-average without replacing macro with micro.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.
