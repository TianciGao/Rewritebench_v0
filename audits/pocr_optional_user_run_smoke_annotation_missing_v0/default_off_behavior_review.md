# Default-Off Behavior Review

Default-off check command:

```text
PYTHONPATH=src python -m cli.main user pocr-diagnostic
```

Observed output:

```text
POCR diagnostic disabled: --enable-pocr-diagnostic was not supplied; no POCR code ran.
boundary: pocr diagnostic support only; official_pocr_computed=false; route_level_pocr_aggregated=false; paper_metric_promoted=false
```

Interpretation:
- The user-facing POCR diagnostic path remains default-off.
- Without `--enable-pocr-diagnostic`, no candidate root, method ID, route ID, engine, run ID, output root, annotation JSONL, API key, or provider configuration is required.
- No POCR facade execution, live API call, DB/checker/timing run, baseline rerun, official POCR computation, route-level POCR aggregation, paper-facing metric promotion, or leaderboard output occurs.
