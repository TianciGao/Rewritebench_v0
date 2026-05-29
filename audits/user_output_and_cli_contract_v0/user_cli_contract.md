# User CLI Contract

Preferred public command shape:

```bash
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

## Core Command

`sqlrb user evaluate` should:

- select cases through case-set metadata;
- invoke the adapter command;
- capture candidate SQL;
- run candidate preflight;
- optionally run local DB/checker diagnostics;
- optionally collect exact-gated local timing;
- optionally run verifier support;
- write artifacts under the D035 output roots.

## Convenience Commands

- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- `sqlrb user compute-local-metrics --run-id <run_id> --output-root output`
- `sqlrb user summarize --run-id <run_id> --output-root output`
- `sqlrb user show-boundary --run-id <run_id> --output-root output`

## Boundary

This contract does not implement these commands. It defines the intended interface for future implementation.
