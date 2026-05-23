# Tiny Validation Results

Runtime root:

- `/tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/`

Command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool all \
  --engines postgres \
  --case-list /tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/case_list.txt \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/d035_output \
  --run-id calcite_hep_layout_smoke \
  --adapter-timeout 10
```

Rows:

- `CONS_0036`
- `CONS_0037`
- `PERF_0006`

Result:

- Command exit status: 0
- Selected rows: 3
- Adapter-invoked rows: 3
- Candidate-generated rows: 0
- No-candidate-SQL rows: 3
- Ledger rows: 3
- Ledger extraction statuses: `no_candidate_sql`
- Ledger failure buckets: `no_candidate_sql`
- Manifest route id: `calcite_hep_fail_closed`
- Manifest method id: `calcite_hep_fail_closed`

The transient `runs/user/calcite_hep_layout_smoke` source-run directory was removed after copying smoke evidence to `/tmp`.
