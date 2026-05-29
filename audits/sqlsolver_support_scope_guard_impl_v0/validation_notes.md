# Validation Notes

Task: `sqlsolver_support_scope_guard_impl_v0`

Date: 2026-05-24

## Targeted tests

- `pytest tests/verifier_support/test_sqlsolver_canonicalization.py -q`: passed, `12 passed`.
- `python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py`: passed.
- `pytest tests/user_entry/test_sqlsolver_support.py tests/verifier_support/test_sqlsolver_canonicalization.py -q`: passed, `23 passed`.

## Non-benchmark canary rerun

- Selected canary families: 5.
- Attempted identity checks: 10.
- SQLSolver-invoked checks: 6.
- Guard-blocked checks: 4.
- Identity equivalent checks: 6.
- Unclassified identity unknown checks: 0.
- `no_verifier_support` checks: 4.
- `ready_to_rerun_same_8_pairs`: true.

Guard-blocked families:

- `quoted_identifier_null_ordering`
- `dense_rank_cte_ranking`

## Parse checks

- `guard_decision_matrix.csv`: parsed successfully.
- `fixture_test_matrix.csv`: parsed successfully.
- `canary_rerun_results.jsonl`: parsed successfully with 10 rows.
- `canary_guard_summary.json`: parsed successfully.

## Markdown non-empty checks

Non-empty checks passed for:

- `README.md`
- `implementation_summary.md`
- `guard_policy.md`
- `blocked_family_boundary.md`
- `no_ser_boundary.md`
- `command_log.txt`

## Benchmark-path checks

`canary_rerun_results.jsonl` and `canary_guard_summary.json` contain no `runs/user`, Track A manifest, Common-core case SQL, top-level `reports`, or top-level `results` paths.

## Prohibited command checks

- No SQLSolver benchmark-pair run occurred.
- No SQLSolver run on the original 8 bounded SQLGlot no-op PostgreSQL benchmark pairs occurred.
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
