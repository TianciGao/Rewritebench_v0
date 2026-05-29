# Default-Off Behavior Review

Default-off behavior is enforced in `src/cli/pocr_diagnostic.py`.

Observed behavior:
- `python -m cli.main user pocr-diagnostic` returns without calling `run_pocr_diagnostic_user_facade()`.
- The command prints that POCR diagnostic output is disabled because `--enable-pocr-diagnostic` was not supplied.
- No candidate root, method ID, route ID, engine, run ID, or output root is required unless the opt-in flag is supplied.

Enabled fail-closed behavior:
- If `--enable-pocr-diagnostic` is present and required inputs are missing, the command raises an error before calling the POCR facade.
- If a top-level `reports` or `results` output root is supplied, D035 output-root validation rejects it before calling the POCR facade.

Runtime boundary:
- No live API call is available from this command.
- No API key is read.
- No DB/checker/timing command is run.
- No baseline is run.
- No official POCR, route-level POCR score, paper metric, or leaderboard output is produced.
