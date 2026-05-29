# Five Failure Mapping

## Original Failures

The PostgreSQL Common-core no-op local diagnostic run selected 40 rows and produced 35 exact rows. The five source-execution failures were:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

The targeted triage reproduced all five as `source_execution_failed`.

## Mapping to Proposed Metadata

All five map to:

```yaml
local_diagnostic:
  diagnostic_mode: cross_dialect_reference
  source_reference:
    engine: mysql
    query: sql/source.sql
  target_candidate:
    engine: postgres
    role: adapter_output
```

Their `sql/source.sql` files are MySQL-like source-reference queries. Their PostgreSQL local diagnostic failures occurred because the current runner executed those MySQL-like queries directly with PostgreSQL.

For these cases, `sql/pos_01.sql` may be declared only as a target-side positive reference or sanity control if P2 confirms that role. It must not be used as the source oracle.

## Why This Is Not a Rewriter-Quality Failure

The no-op adapter emitted source-like candidate SQL. The failing stage was source execution before candidate execution and checker comparison. The failure came from executing MySQL-like source-reference SQL on PostgreSQL, not from an incorrect rewrite decision.

## Why This Is Not Official Metrics

The run and this design are local diagnostics only. They do not compute official metrics, update paper results, update reports/results, change denominators, or create leaderboard inputs.

## Next Safe Action

Patch explicit manifest role metadata for all 9 Common-core PORT cases in P2 after this design is accepted. Then implement runner consumption and MySQL source-side execution in separate tasks.
