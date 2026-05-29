# VeriEQL CONS_0007 One-Pair Canary V0

Verdict: `canary_ran_unsupported_no_decidable_verdict`.

This task ran one bounded local VeriEQL canary using the staged external VeriEQL environment:

- Tool: VeriEQL only.
- Case: `CONS_0007` only.
- Pair: `source_vs_positive` only.
- Source SQL: `cases/CONS/CONS_0007/sql/source.sql`
- Positive SQL: `cases/CONS/CONS_0007/sql/pos_01.sql`
- Schema context: `schemas/calcite_core_sql_tests_cons0007_v0/postgres/ddl.sql`
- Output root used for runtime artifacts: `/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0`

Environment:

- `SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL`
- `SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python`
- `SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python`

The VeriEQL batch CLI ran in JSONL mode and wrote a result record. The normalized verdict was:

```text
unsupported
```

Raw VeriEQL output reported:

```text
states=["NSE"]
err="Not supported feature: EXISTS"
```

The local semantic-equivalence summary remains non-decidable:

- `semantic_equivalence_rate=null`
- `semantic_equivalence_rate_status=not_applicable`
- `decidable_count=0`
- `unsupported_count=1`
- `result_checker_exactness_used=false`

This is local verifier-support evidence only. It is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
