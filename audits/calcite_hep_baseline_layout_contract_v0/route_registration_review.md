# Route Registration Review

User-entry invocation remains adapter-command based.

Current command shape:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/d035_output \
  --run-id calcite_hep_layout_smoke
```

Route identity handling:

- `src/sql_rewrite_bench/local_timing.py` recognizes `baselines/calcite_hep_fail_closed/adapter.py`.
- D035 `run_manifest.json` records:
  - `route_id=calcite_hep_fail_closed`
  - `method_id=calcite_hep_fail_closed`

CLI surface:

- No new CLI option was added.
- `src/cli/` was not modified.
- The existing `sqlrb user evaluate --adapter-command ...` facade remains the correct user-facing path.
