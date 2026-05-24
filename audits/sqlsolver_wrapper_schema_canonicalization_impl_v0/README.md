# SQLSolver Wrapper/Schema Canonicalization Implementation

This packet records the narrow implementation of SQLSolver input canonicalization based on `audits/sqlsolver_wrapper_schema_canonicalization_design_v0/`.

## Scope

- Implemented wrapper/schema canonicalization utilities in verifier support.
- Added focused fixture tests for SQL line shaping, comments, semicolon handling, schema DDL shaping, feature guards, and fail-closed behavior.
- Ran only non-benchmark SQLSolver identity canaries.
- Did not run SQLSolver on benchmark pairs.
- Did not run VeriEQL, adapters, DB execution, checker execution, timing, LLM calls, local metrics, official metrics, paper rendering, or Repair-1.

## Files changed

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `tests/verifier_support/test_sqlsolver_canonicalization.py`

## Audit files created

- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/README.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/implementation_summary.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canonicalization_rules.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/fixture_test_matrix.csv`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canary_inputs_manifest.csv`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canary_sqlsolver_results.jsonl`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canary_summary.json`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/fail_closed_policy.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/no_ser_boundary.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/command_log.txt`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/validation_notes.md`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canary_inputs/`
- `audits/sqlsolver_wrapper_schema_canonicalization_impl_v0/canary_runtime/`

## Canary result summary

- Selected canaries: `5`
- Attempted identity checks: `10`
- Identity passed: `6`
- Identity unknown: `4`
- Identity timeout: `0`
- Identity unsupported: `0`
- Identity tool error: `0`
- `ready_to_rerun_same_8_pairs`: `false`

## Blockers

The remaining blockers are the quoted identifier / NULL ordering canary and the DENSE_RANK / CTE ranking canary, both with SQLSolver `UNKNOWN` identity outcomes.

## Next safe action

Do not rerun the same 8 benchmark pairs yet. First decide whether the quoted identifier / NULL ordering and DENSE_RANK / CTE families should be scoped out or addressed by additional wrapper/modeling work. Broader SQLSolver coverage and Repair-1 remain blocked.
