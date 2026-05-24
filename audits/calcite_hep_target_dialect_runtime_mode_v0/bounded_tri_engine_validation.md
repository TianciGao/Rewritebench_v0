# Bounded Tri-Engine Validation

Run id prefix:

`calcite_hep_target_dialect_runtime_mode_v0`

User-facade command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list /tmp/sqlrb_calcite_hep_target_dialect_runtime_mode_cases.txt \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_target_dialect_runtime_mode_v0/output \
  --run-id calcite_hep_target_dialect_runtime_mode_v0 \
  --enable-db-execution \
  --enable-checker
```

No timing or metrics command was run.

Summary:

| engine | selected | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch | unsupported |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| postgres | 6 | 5 | 1 | 5 | 5 | 5 | 4 | 1 | 0 |
| mysql | 6 | 5 | 1 | 5 | 5 | 5 | 3 | 2 | 0 |
| spark | 6 | 5 | 1 | 4 | 4 | 4 | 4 | 0 | 1 |

PostgreSQL stability:

- Same selected/generated/exact shape as the prior bounded readiness smoke.
- `CONS_0036` remains a label-only checker mismatch.
- `PORT_0004` remains no-candidate.

MySQL:

- Five candidates were generated with MySQL backtick identifiers.
- No MySQL candidate was blocked by the PostgreSQL-dialect guard.
- No MySQL candidate execution failure occurred.
- Exact rows: `PERF_0006`, `CONS_0005`, `CONS_0036`.
- Mismatch rows: `CONS_0037`, `PORT_0024`, both label-only in the local checker
  output.
- `PORT_0004` remained no-candidate.

Spark:

- Five candidates were generated with Spark backtick identifiers.
- No Spark candidate was blocked by the PostgreSQL-dialect guard.
- Exact rows: `PERF_0006`, `CONS_0005`, `CONS_0036`, `CONS_0037`.
- `PORT_0004` remained no-candidate.
- `PORT_0024` generated a candidate but remained unsupported because the Spark
  target-reference/source-role policy was not declared for that row.

Target-dialect check:

- Grep for PostgreSQL double-quoted identifiers and `DOUBLE PRECISION` in
  MySQL/Spark generated candidate files returned no matches.
