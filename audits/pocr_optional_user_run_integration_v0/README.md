# Optional POCR User-Run Integration

This packet records `pocr_optional_user_run_integration_v0`.

The implementation adds a default-off public facade command:

```text
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic ...
```

When `--enable-pocr-diagnostic` is absent, no POCR facade code runs. When the flag is present, the command writes diagnostic POCR user-output files under the caller-provided D035 output root only:

```text
output/results/<run_id>/pocr/
output/logs/<run_id>/pocr/
output/reports/<run_id>/
```

This remains diagnostic support only. It does not call live APIs, read API keys, run DB/checker/timing, rerun baselines, compute official Positive Operation Coverage Rate, aggregate route-level POCR, promote paper-facing metrics, or create leaderboard output.

Next safe action: run one optional user-run smoke using an existing candidate root and annotation-missing mode, then decide whether to add annotation JSONL replay support for the Direct LLM PG40 diagnostic artifact.
