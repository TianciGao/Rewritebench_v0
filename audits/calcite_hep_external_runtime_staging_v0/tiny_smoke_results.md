# Tiny Smoke Results

Runtime output root:

- `/tmp/sqlrb_calcite_hep_external_runtime_staging_v0/`

Command:

```bash
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke \
SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep \
SQLRB_CALCITE_HEP_JAVA=/usr/bin/java \
SQLRB_CALCITE_HEP_TIMEOUT=30 \
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool all \
  --engines postgres \
  --case-list /tmp/sqlrb_calcite_hep_external_runtime_staging_v0/case_list.txt \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_external_runtime_staging_v0/smoke_output \
  --run-id calcite_hep_external_runtime_smoke \
  --adapter-timeout 40
```

Rows:

| case_id | engine | status | candidate_generated |
| --- | --- | --- | --- |
| `CONS_0036` | postgres | `calcite_invocation_succeeded` | true |
| `CONS_0037` | postgres | `calcite_invocation_succeeded` | true |
| `PERF_0006` | postgres | `calcite_invocation_succeeded` | true |

Summary:

- Selected rows: 3
- Adapter-invoked rows: 3
- Candidate-generated rows: 3
- Failure buckets: `none`
- Transient `runs/user/calcite_hep_external_runtime_smoke` workspace was copied to `/tmp/.../workspaces_snapshot` for local review and then removed from the release repo.

This smoke is candidate-generation and output-contract evidence only. It does not run database execution, checkers, verifier passes, timing, official metrics, or paper reports.
