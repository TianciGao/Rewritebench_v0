# Dependency Gap Handling

## Known Dependency Gap

Prior probe found the active Python environment missing:

- `ujson`
- `z3`
- `ordered_set`
- `lark`
- `prettytable`
- `mysql.connector`

This task did not install any dependencies.

## Runtime Handling

When JSONL batch mode launches and stderr indicates a missing import, the wrapper records:

- per-pair `normalized_verdict=tool_error`
- per-pair `invocation_status=tool_error`
- artifact path field `dependency_missing=true`
- summary `semantic_equivalence_rate=null`
- summary `semantic_equivalence_rate_status=not_applicable`
- summary `na_reason=verieql_dependency_missing`

## Dry-Run Handling

When `dry_run=True`, the wrapper:

- writes `verieql_pairs.jsonl`
- records the command line in verdict artifact paths
- does not invoke VeriEQL
- emits per-pair `not_attempted`
- sets `na_reason=verieql_dry_run_not_executed`

## Boundary

Missing dependencies are a local availability condition, not a benchmark failure, not a method failure, and not official metric evidence.
