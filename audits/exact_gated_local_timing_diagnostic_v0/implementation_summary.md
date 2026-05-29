# Implementation Summary

## Files Changed

- `src/sql_rewrite_bench/local_timing.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `tests/user_entry/test_local_timing.py`

## CLI/API

Timing is opt-in through:

```bash
--collect-timing
--timing-warmup 1
--timing-repetitions 5
--timing-timeout 30
```

`--collect-timing` requires both `--enable-db-execution` and `--enable-checker`.

## Artifact Layout

When timing is enabled, the runner writes:

```text
runs/user/{run_name}/timing/timing_policy.json
runs/user/{run_name}/timing/environment_metadata.json
runs/user/{run_name}/timing/timing_summary.json
runs/user/{run_name}/timing/rows/{case_id}__{engine}__{route_id}__{candidate_id}.json
```

Engine-specific timing workspaces are local implementation details under:

```text
runs/user/{run_name}/timing/workspaces/
```

## Exact Gate

Rows are timing eligible only when candidate generation, preflight, source execution, candidate execution, checker status, strict exactness, failure bucket, label-only diagnostic status, and engine/role support all pass.

Rows that do not pass remain visible in timing row JSON with:

- `timing_eligible=false`
- `timing_status=not_eligible`
- `speedup_ratio=null`
- explicit `timing_na_reason`

## Local Speedup Field

`speedup_ratio` is a per-row local diagnostic field only. It is present only when:

- timing is eligible;
- timing status is `timed`;
- source and candidate sample arrays are complete;
- source and candidate medians are positive.

No route-level metric is computed.
