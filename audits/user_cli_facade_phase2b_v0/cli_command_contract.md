# CLI Command Contract

Primary command:

```bash
sqlrb user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id <run_id>
```

Supported Phase 2B commands:

- `sqlrb user evaluate`
- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- `sqlrb user show-boundary`
- `sqlrb user compute-local-metrics`
- `sqlrb user summarize`

Reserved but not implemented:

- `--verifier verieql`
- `--verifier sqlsolver`

The reserved verifier flags fail closed and do not invoke the local diagnostic runner.

No command exists for:

- leaderboard
- ranking
- winner selection
- official metrics
- paper table rendering
- retained evidence promotion

Output boundary:

- `output/` is local/user-run output.
- Top-level `reports/` and `results/` remain official/paper-facing surfaces and are not touched by the CLI facade.
