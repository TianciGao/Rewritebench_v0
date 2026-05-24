# Runtime Blockers

Synthetic preflight was attempted exactly once and failed to produce candidate SQL.

Primary blocker:

- `runtime_missing_workdir_asset`: `rules_for_selected/standard.txt` was not found from the temporary working directory.

Secondary blockers:

- Custom port flag was not confirmed. A diagnostic startup with `--server.port=26336` did not bind port `26336`; running without the flag bound the official default port `6336`.
- Current `baselines/learnedrewrite/adapter.py` has fail-closed real `http` and `cmd` hooks; it cannot yet call the runtime.
- Schema JSON compatibility is not proven beyond the runtime receiving a JSON payload and echoing the synthetic SQL.
- Response shape for successful synthetic input remains unproven because the runtime failed before producing `rewritten_sql`.

Not attempted:

- Starting the server from `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/`, because the runtime writes `request.txt` to its working directory and modifying the external upstream source clone is not authorized.
- Copying `rules_for_selected/standard.txt` into a temp runtime workdir, because copying upstream runtime assets into a new workdir was outside this task's safe preflight boundary.

Recommended setup fix:

1. Authorize a temp-only runtime staging task that can copy the minimal non-source runtime asset directory `rules_for_selected/` from the external source clone into a temporary runtime working directory, without copying it into the release repo.
2. Start the JAR from that temp staged working directory.
3. Repeat exactly one synthetic request.
4. Only if that succeeds, implement adapter HTTP mode and run a 1-2 row PostgreSQL-only user-facade smoke without DB/checker/timing.
