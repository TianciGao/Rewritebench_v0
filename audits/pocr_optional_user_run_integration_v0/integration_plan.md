# Integration Plan

Chosen integration point: `src/cli/main.py` plus a focused helper module at `src/cli/pocr_diagnostic.py`.

Why this path:
- `src/cli` is already the public user-facing facade surface.
- `sqlrb user evaluate` remains unchanged, so default user-run evaluation behavior is preserved.
- D035 output-root validation is reused through `sql_rewrite_bench.user_output.build_output_paths`.
- The existing internal facade `run_pocr_diagnostic_user_facade()` remains the core POCR implementation surface.

Default-off behavior:
- New subcommand: `user pocr-diagnostic`.
- Required opt-in flag: `--enable-pocr-diagnostic`.
- Without the flag, the command returns successfully and does not call the POCR facade.

Enabled behavior:
- Requires `--candidate-root`, `--method-id`, `--route-id`, `--engine`, `--run-id`, and `--output-root`.
- Optional `--annotation-jsonl` replays existing annotation JSONL.
- Optional `--case-list` filters Common-core case IDs for bounded diagnostics.
- `live_enabled` is fixed to `false` in this task.
- The command writes only D035 local diagnostic output files.

No integration was added to default user-run execution, DB/checker/timing, local metrics, verifier, paper renderer, retained-evidence promotion, or leaderboard flows.
