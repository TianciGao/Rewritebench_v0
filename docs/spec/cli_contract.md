# D035 CLI Contract

The public user-facing facade lives under `src/cli/`.

Installed command shape:

```bash
sqlrb user <command> ...
```

Checkout command shape:

```bash
PYTHONPATH=src python -m cli.main user <command> ...
```

## Current User Commands

- `user evaluate`: run a local diagnostic adapter workflow and export D035 output.
- `user list-cases`: list selected case metadata without running adapters.
- `user explain-selection`: explain selected rows without running adapters.
- `user show-output-schema`: print the local output schema and D035 roots.
- `user show-boundary`: print the local-only output boundary.
- `user compute-local-metrics`: compute non-official local diagnostics for an existing run.
- `user summarize`: summarize existing local diagnostic output.
- `user verify`: bounded local verifier smoke/fail-closed support.

## Implementation Boundary

- Public CLI facade: `src/cli/`.
- Core reusable implementation: `src/sql_rewrite_bench/`.
- Route-specific baseline adapters: `baselines/`.
- Public adapter examples: `examples/`.
- Development scripts remain under `scripts/dev/` until a separate physical migration.

The lower-level `src/sql_rewrite_bench/user_run.py` pipeline remains an
internal implementation path. It may stage artifacts under `runs/user/<run_id>/`
before `src/sql_rewrite_bench/user_output.py` exports them to
`output/results/<run_id>/`, `output/logs/<run_id>/`, and
`output/reports/<run_id>/`.

## Non-goals

The user CLI does not create official metrics, paper tables, retained evidence,
or leaderboard output. Any promotion to top-level `reports/`, top-level
`results/`, or retained evidence requires separate authorization.
