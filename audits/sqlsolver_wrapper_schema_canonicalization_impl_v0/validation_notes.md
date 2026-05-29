# Validation Notes

Task: `sqlsolver_wrapper_schema_canonicalization_impl_v0`

Date: 2026-05-24

## Targeted tests

- `pytest tests/verifier_support/test_sqlsolver_canonicalization.py -q`: passed, `10 passed`.
- `python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py`: passed.
- `pytest tests/user_entry/test_sqlsolver_support.py tests/verifier_support/test_sqlsolver_canonicalization.py -q`: passed, `21 passed`.

## Non-benchmark SQLSolver canaries

- SQLSolver availability for the external non-repo installation: available.
- Canaries selected: 5.
- Identity checks attempted: 10.
- Equivalent identity checks: 6.
- Unknown identity checks: 4.
- Timeout identity checks: 0.
- Unsupported identity checks: 0.
- Tool-error identity checks: 0.
- `ready_to_rerun_same_8_pairs`: false.

Remaining blockers:

- `quoted_identifier_null_ordering__source_identity`: `unknown`.
- `quoted_identifier_null_ordering__candidate_identity`: `unknown`.
- `dense_rank_cte_ranking__source_identity`: `unknown`.
- `dense_rank_cte_ranking__candidate_identity`: `unknown`.

## Parse checks

- `fixture_test_matrix.csv`: parsed successfully with 10 rows.
- `canary_inputs_manifest.csv`: parsed successfully with 10 rows.
- `canary_sqlsolver_results.jsonl`: parsed successfully with 10 rows.
- `canary_summary.json`: parsed successfully.

## Markdown non-empty checks

Non-empty checks passed for:

- `README.md`
- `implementation_summary.md`
- `canonicalization_rules.md`
- `fail_closed_policy.md`
- `no_ser_boundary.md`
- `command_log.txt`

## Source/path checks

- All paths recorded in `canary_inputs_manifest.csv` exist.
- Canary inputs are synthetic non-benchmark SQL/schema files under the audit packet.
- No Common-core case SQL path, Track A manifest path, `runs/user`, top-level `reports`, or top-level `results` path was used for canary execution.

## Prohibited command checks

- No broader SQLSolver pass was run.
- No SQLSolver benchmark-pair run occurred.
- No SQLSolver run on the same 8 bounded SQLGlot no-op PostgreSQL benchmark pairs occurred.
- No SQLSolver run on the SQLGlot no-op PostgreSQL 35 exact subset occurred.
- No SQLSolver run on the 346-pair manifest occurred.
- No VeriEQL command was run.
- No adapter, DB execution, checker execution, timing collection, LLM, `compute-local-metrics`, official metrics, paper rendering, or Repair-1 command was run.

## Boundary checks

- No official SER was produced.
- No bounded SER was promoted.
- No local metrics were recomputed.
- No paper result changed.
- No retained evidence was promoted.
- No denominator, case membership, or raw legacy evidence changed.

## Secret and protected-path checks

- Changed-file secret scan: passed.
- Protected-path review: passed.
- `git diff --check`: passed.
