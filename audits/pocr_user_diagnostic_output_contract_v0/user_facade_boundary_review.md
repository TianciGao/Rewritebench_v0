# User Facade Boundary Review

The new facade function is `run_pocr_diagnostic_user_facade()` in `src/sql_rewrite_bench/pocr/user_facade.py`.

Default behavior:
- `live_enabled=false`.
- No API key is read.
- No live API call is made.
- No DB, checker, or timing command is run.
- No baseline or adapter is run.
- No official Positive Operation Coverage Rate is computed.
- No route-level POCR aggregation is produced.
- No paper-facing metric is promoted.

If `annotation_jsonl` is absent, the facade emits row-level diagnostics with `annotation_status=annotation_missing` and `stage_b_status=annotation_missing`. This preserves user-output shape without pretending POCR evidence exists.

If `output_root` is absent, the facade returns rows and summaries in memory only. If `output_root` is provided, files are written only under that caller-provided root using D035-style subpaths.

The facade is not wired into the default user-run flow in this task. Any future CLI integration should remain optional and default-off.
