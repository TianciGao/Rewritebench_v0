# Output Policy

All real user-adapter local diagnostic outputs must stay under:

```text
runs/user/{run_name}/
```

Expected local outputs may include `config.yaml`, `selected_cases.csv`, `candidate_sql/`, `workspaces/`, execution artifacts, checker artifacts, `ledger.csv`, `failures.csv`, `summary.json`, `report.md`, `quality_summary.json`, `quality_report.md`, and `tag_slices.csv`.

Policy:

- Do not commit `runs/user/` outputs.
- Do not write to case-local `runs/`.
- Do not write to `reports/` or `results/`.
- Do not update `case_sets/`.
- Do not change cases, manifests, SQL files, schemas, checker configs, validation scripts, inventory, benchmark specs, repository specs, denominators, paper results, case membership, or raw retained evidence.
- Audit packets may summarize commands, selected rows, and local diagnostic schema, but must label outputs as local diagnostic only.
- Controlled target-reference runs must use separate run names and summaries from real user-adapter runs.
- Timing fields must remain absent or explicitly not timed unless a separate timing task is authorized.
