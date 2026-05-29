# Equivalent Timeout Hypotheses

## Observed Behavior

Known local evidence before this audit:

- `CONS_0007 source_vs_positive`: `NSE`, `Not supported feature: EXISTS`.
- `PERF_0062 source_vs_positive`: `EQU,TMO`, normalized to `timeout`.
- `SELECT 1` synthetic pairs: `NSE`, because VeriEQL requires `FROM`.
- `SELECT a FROM T` vs `SELECT a FROM T`: repeated `EQU` states followed by `TMO`.
- `SELECT a FROM T` vs `SELECT b FROM T`: `NEQ`, normalized to `non_equivalent`.
- Timeout-policy probe at 30, 120, and 300 seconds: all remained `EQU...TMO`.

## Most Likely Cause

The most likely cause is timeout-mode's increasing finite-bound loop. Each `EQU` confirms no counterexample at the current finite bound. The runner then tries the next larger bound. Eventually the next bound times out, so the state list ends with `TMO`.

This is consistent with historical VeriEQL output files, which contain many `EQU...TMO` rows and no obvious clean all-`EQU` timeout-mode rows in the inspected `.out` files.

## Alternative Hypotheses

Timeout too short:

- Less likely as the only cause because 30, 120, and 300 second probes all ended in `EQU...TMO`.
- Still possible for larger bound sizes.

Missing constraints:

- Possible contributor for larger cases.
- Less likely for identical `SELECT a FROM T` queries.

Unbounded domain:

- Possible in solver performance terms, but VeriEQL already uses finite symbolic rows and type bounds for each bound size.

Schema encoding issue:

- Not the leading explanation because `NEQ` worked for `SELECT a FROM T` vs `SELECT b FROM T` under the same schema.

VeriEQL internal multi-branch behavior:

- Plausible. The tool's timeout runner deliberately explores increasing bounds after each `EQU`.

Known verifier limitation:

- Plausible for practical clean-equivalence reporting in timeout mode. A finite-bound or direct API mode may be needed to produce clean equivalent smoke results.

## Policy Consequence

Do not classify `EQU...TMO` as `equivalent` in SQL-RewriteBench outputs. The correct local normalized status remains `timeout`, with the raw state history retained for diagnostics.
