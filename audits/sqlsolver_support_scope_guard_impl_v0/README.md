# SQLSolver Support-Scope Guard Implementation

This packet records the narrow support-scope guard implementation for SQLSolver blocker families found by the previous non-benchmark canaries.

## Scope

- Added pre-invocation support-scope guards for quoted identifier / NULL ordering and DENSE_RANK / CTE ranking.
- Kept existing canonicalization behavior for already-passing canaries.
- Reran only non-benchmark canaries from `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/`.
- Did not run any benchmark pair, broader SQLSolver pass, VeriEQL, adapter, DB/checker/timing, LLM, local metrics, official metrics, paper rendering, or Repair-1.

## Canary rerun summary

- Selected canaries: `5`
- Attempted checks: `10`
- SQLSolver-invoked checks: `6`
- Guard-blocked checks: `4`
- Identity equivalent: `6`
- Unclassified identity unknown: `0`
- `no_verifier_support`: `4`
- `ready_to_rerun_same_8_pairs`: `true`

## Verdict

The support-scope guard removed unclassified `UNKNOWN` outcomes from the non-benchmark canaries. The same 8-pair bounded SQLSolver benchmark rerun can be separately authorized next, but broader coverage remains blocked until that rerun is stable.
