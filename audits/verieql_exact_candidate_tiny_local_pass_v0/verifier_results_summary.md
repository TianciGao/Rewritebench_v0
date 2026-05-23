# Verifier Results Summary

Command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f <pairs.jsonl> -s 10 -t 30 -c 1 -o <output.jsonl>
```

Environment:
- `SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL`
- `SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python`
- `SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python`

Per-row verdicts:

| case_id | raw states | normalized verdict | interpretation |
| --- | --- | --- | --- |
| CONS_0036 | `EQU` repeated 10 times | equivalent | Clean finite-bound equivalent over a real exact candidate row. |
| PERF_0077 | `NIE` | not_implemented | VeriEQL reached the row but did not implement the `LIKE` predicate shape. |
| PERF_0082 | `NIE` | not_implemented | VeriEQL reached the row but did not implement the `LIKE` predicate shape. |

Summary counts:
- selected_candidate_rows: 3.
- exact_candidate_rows: 3.
- verifier_attempted_rows: 3.
- equivalent_count: 1.
- non_equivalent_count: 0.
- unknown_count: 0.
- timeout_count: 0.
- unsupported_count: 0.
- syntax_error_count: 0.
- not_implemented_count: 2.
- out_of_memory_count: 0.
- tool_error_count: 0.
- not_attempted_count: 0.
- decidable_count: 1.
- local_tiny_semantic_equivalence_rate: 1.0.
- verifier_decidability_rate: 0.3333333333333333.

The local tiny semantic equivalence rate is a diagnostic readiness signal over one decidable row only. It is not official Semantic Equivalence Rate and is not paper evidence.

