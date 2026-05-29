# Smoke Pair Selection

Preferred bounded SQLSolver smoke scope when the tool is available:

- Equivalent synthetic support pair: `SELECT 1` vs `SELECT 1`.
- Non-equivalent synthetic support pair: `SELECT 1` vs `SELECT 2`.

These are `support_pair_smoke` pairs and do not use Common-core rows, method-generated candidates, or retained evidence.

Actual local smoke:

- SQLSolver was unavailable.
- Ran only a fail-closed temp-root smoke with one synthetic `support_pair_smoke` pair.
- The pair produced `not_attempted`; no fake equivalent or non-equivalent result was fabricated.
