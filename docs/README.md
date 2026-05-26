# Documentation

Start with the top-level `README.md` for the public repository entrypoint.

User-facing documentation:

- `guide/user_quickstart.md`: short D035-shaped user quickstart.
- `USER_BENCHMARK_GUIDE.md`: user-entry smoke runs, adapter capture, and optional local diagnostics.
- `USER_ENTRY_DATA_FLOW.md`: user-entry data flow, internal staging, and exported output locations.
- `baseline_reproduction.md`: local diagnostic baseline reproduction manual for deterministic, LLM, prior-method, and verifier-support routes.
- `candidate_sql_outputs.md`: D035-aligned candidate SQL output tree and manifest contract.
- `pocr_diagnostic.md`: optional default-off POCR diagnostic command and replay examples.
- `spec/output_contract.md`: D035 local user-output contract.
- `spec/cli_contract.md`: user-facing CLI and implementation boundary.
- `templates/adapter_template.md`: minimal adapter contract template.

The current user-facing output contract is:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

`runs/user/<run_id>/` is internal transitional staging used by the current
implementation before export. It is not the public-facing output contract.

This index does not define official metrics, paper tables, reports/results, retained evidence, or leaderboard output.
