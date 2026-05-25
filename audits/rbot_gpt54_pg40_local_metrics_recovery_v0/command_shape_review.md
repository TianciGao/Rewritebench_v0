# Command Shape Review

`src/cli/main.py` supports two `user compute-local-metrics` modes:

- single-run mode: requires `--run-id` and must not use aggregate options
- aggregate mode: requires `--run-id-prefix`, `--engines`, and `--aggregate-run-id`, and cannot be combined with `--run-id`

Correct command shape for this recovery:

```bash
python -m cli.main user compute-local-metrics \
  --run-id rbot_gpt54_pg40_bounded_diagnostic_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_rbot_gpt54_pg40_bounded_local_diagnostic_v0/output
```

Aggregate options intentionally not used:

- `--run-id-prefix`
- `--engines`
- `--aggregate-run-id`

Execution result: not executed, because `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0` was missing. Running the command without source artifacts would not recover canonical metrics and would not satisfy the source-of-truth boundary.
