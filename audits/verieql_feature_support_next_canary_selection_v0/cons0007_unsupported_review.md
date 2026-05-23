# CONS_0007 Unsupported Review

Prior canary:

- Task: `verieql_cons0007_one_pair_canary_v0`
- Tool: VeriEQL
- Pair: `CONS_0007_source_vs_positive_pos_01`
- Pair type: `source_vs_positive`
- Source SQL: `cases/CONS/CONS_0007/sql/source.sql`
- Positive SQL: `cases/CONS/CONS_0007/sql/pos_01.sql`
- Schema context: `schemas/calcite_core_sql_tests_cons0007_v0/postgres/ddl.sql`

Raw tool output:

```text
states=["NSE"]
err="Not supported feature: EXISTS"
```

Normalized output:

```text
verdict=unsupported
invocation_status=unsupported
semantic_equivalence_rate=null
semantic_equivalence_rate_status=not_applicable
decidable_count=0
unsupported_count=1
```

Interpretation:

- VeriEQL was successfully invoked through the staged root and external venv.
- The batch command completed and produced a tool-native output row.
- The row failed because the SQL used a feature that VeriEQL reports as unsupported.
- This is not an equivalence or non-equivalence verdict.
- This is not official Semantic Equivalence Rate evidence.

Selection consequence:

- `CONS_0007` should not be repeated as the next support-discovery canary unless the goal is specifically to validate unsupported-feature handling.
- The next canary should avoid `EXISTS`, nested subqueries, and other known high-risk syntax.
