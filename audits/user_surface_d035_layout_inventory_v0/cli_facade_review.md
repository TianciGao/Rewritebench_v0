# CLI Facade Review

`src/cli/` is the current user-facing facade.

Files:

- `src/cli/__init__.py`
- `src/cli/__main__.py`
- `src/cli/main.py`

Current user commands:

- `sqlrb user evaluate`
- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- `sqlrb user show-boundary`
- `sqlrb user compute-local-metrics`
- `sqlrb user summarize`
- `sqlrb user verify`

D035 alignment:

- The facade is under `src/cli/`.
- `evaluate` delegates to the internal user-run pipeline and exports to D035 output roots.
- `show-output-schema` prints the D035 output path shape.
- `show-boundary` keeps the local-only, non-paper, non-leaderboard boundary visible.
- `verify` exists as a bounded local synthetic-smoke facade and is fail-closed for broader pair scopes.

Known transitional behavior:

- `evaluate` still uses `runs/user/<run_id>/` as an internal source-run staging path before export.
- This should be treated as implementation debt for a future narrow cleanup, not as a reason to move broad directories now.

Verdict:

- `src/cli` is the current public facade and is D035-compliant in location and output-export intent.
