# Future Prompt: b_line_user_entry_mvp_v0

Implement only a minimal B-line user runner skeleton if separately authorized.

Use:

- `audits/b_line_user_entry_contract_v0/b_line_user_entry_contract_summary.md`
- `audits/b_line_user_entry_contract_v0/user_entry_case_selection_contract.csv`
- `audits/b_line_user_entry_contract_v0/user_algorithm_adapter_contract.csv`
- `audits/b_line_user_entry_contract_v0/user_run_output_schema.csv`
- `audits/b_line_user_entry_contract_v0/user_run_report_contract.csv`
- `audits/b_line_user_entry_contract_v0/user_entry_mvp_task_plan.md`

Required MVP behavior:

- Resolve `--case-set common_core_v0`, optional `--pool`, optional `--case-list`, and `--engine postgres|mysql|spark|all` from release metadata.
- Invoke a user adapter command in a per-row workspace.
- Capture candidate SQL from stdout or `candidate.sql`.
- Write only under `runs/user/<run_id>/`.
- Produce `config.yaml`, `selected_cases.csv`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md`.
- Include no-global-leaderboard and paper-evidence separation warnings.

Hard boundaries:

- Do not modify `cases/`.
- Do not modify `case_sets/`.
- Do not modify `inventory/`.
- Do not write to `reports/`.
- Do not write to `results/`.
- Do not compute official metrics.
- Do not render paper tables.
- Do not run DB engines unless a later task explicitly authorizes execution.
- Do not parse retained paper evidence.
- Do not write into case-local `runs/`.
- Do not modify raw legacy evidence or the legacy repository.

Validation:

- Run unit tests for selection and output-root enforcement.
- Run `python scripts/dev/smoke_ledger_fixtures.py`.
- Parse generated JSON/YAML outputs.
- Check no files changed under forbidden paths.
- Run `git diff --check`.
