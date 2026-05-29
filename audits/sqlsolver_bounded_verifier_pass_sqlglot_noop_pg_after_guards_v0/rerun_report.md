# Rerun Report

## Authorization Context

The previous non-benchmark canary task reported `ready_to_rerun_same_8_pairs=true` after support-scope guards eliminated unclassified canary UNKNOWN outcomes. This rerun used exactly the same eight selected benchmark pairs from `audits/sqlsolver_bounded_verifier_pass_sqlglot_noop_pg_v0/selected_pairs.csv` with no additions, removals, or reordering.

## Same-8 Selection Confirmation

- Prior selected rows: `8`
- Current selected rows: `8`
- Same order: `true`
- Source/candidate hashes matched prior manifest: `true`
- Schema DDL references existed: `true`

## Identity Guard Before/After

Before guards, 3/8 pairs passed both identity guards and 5/8 had at least one identity `unknown`.

After guards:

- Both identity guards passed: `2/8`
- Identity guards blocked by explicit `no_verifier_support`: `3/8`
- Unclassified identity UNKNOWN: `3/8`

## Actual Source-Candidate Verdicts

- Attempted actual checks: `2`
- Equivalent: `2`
- Non-equivalent: `0`
- Unknown: `0`
- Timeout: `0`
- Tool error: `0`
- No verifier support: `3`
- Identity guard failed: `3`

## Support-Scope Effects

Unclassified identity UNKNOWN was eliminated: `False`. Known unsupported families are now reported as `no_verifier_support` instead of allowing unexplained SQLSolver UNKNOWN to drive the boundary.

## Broader PostgreSQL No-Op Readiness

`ready_for_sqlglot_noop_pg_35=false`.

This readiness means the same-8 stability gate passed with no unclassified identity UNKNOWN or actual non-equivalence. It does not authorize cross-route coverage, the 346-pair manifest, VeriEQL, official SER, or Repair-1.

## Not Official SER

The bounded ratio, if present, is local diagnostic verifier-support only. Guarded `no_verifier_support`, unknown, timeout, unsupported, tool-error, and not-attempted rows are excluded from any decidable support denominator and reported separately. Local checker exactness remains Result Consistency evidence only.
