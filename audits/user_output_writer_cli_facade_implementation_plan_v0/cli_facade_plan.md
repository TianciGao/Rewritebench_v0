# CLI Facade Plan

## Target Package

Future public facade target:

```text
src/cli
```

The internal implementation package remains:

```text
src/sql_rewrite_bench
```

The facade should call existing internal modules and should not duplicate case selection, adapter execution, DB execution, checking, timing, or metrics business logic.

## Public Command Shape

Primary command:

```text
sqlrb user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id <run_id> \
  [--collect-timing] \
  [--verifier verieql] \
  [--verifier sqlsolver]
```

Convenience commands:

```text
sqlrb user list-cases
sqlrb user explain-selection
sqlrb user show-output-schema
sqlrb user compute-local-metrics --run-id <run_id> --output-root output
sqlrb user summarize --run-id <run_id> --output-root output
sqlrb user show-boundary --run-id <run_id> --output-root output
```

## Internal Mapping

| CLI command | Internal implementation target | Notes |
| --- | --- | --- |
| `sqlrb user evaluate` | `sql_rewrite_bench.user_run.run_user_benchmark` plus future `user_output.py` export | Use existing runner first, then export to `output/`. |
| `sqlrb user list-cases` | existing `user_run` selection helpers | Preserve metadata-driven selection. |
| `sqlrb user explain-selection` | existing `user_run` selection explanation | No case scanning. |
| `sqlrb user show-output-schema` | existing schema text plus `user_output_contract_v0` material | Should describe the D035 `output/results|logs|reports` shape. |
| `sqlrb user compute-local-metrics` | `sql_rewrite_bench.local_metrics.compute_and_write_local_metrics` | Keep local-only metrics and route grouping. |
| `sqlrb user summarize` | read output results/reports artifacts | No recomputation unless explicitly requested. |
| `sqlrb user show-boundary` | read or render `boundary.md` | Make local-only status visible. |

## CLI Implementation Notes

- Add `src/cli` only in the implementation task, not in this planning task.
- Keep argument parsing thin and focused on public UX.
- Reuse existing environment checks and internal validation where possible.
- Preserve existing developer module invocation during transition.
- Treat verifier flags as unsupported or placeholder until VeriEQL and SQLSolver integration is separately authorized.
- Keep `output/` local-user output distinct from top-level `reports/` and `results/`.
