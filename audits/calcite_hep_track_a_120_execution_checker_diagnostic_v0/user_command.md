# User Command

Run id:

`calcite_hep_track_a_120_execution_checker_v0`

Command used:

```bash
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
export SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep
export SQLRB_CALCITE_HEP_TIMEOUT=30
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/output \
  --run-id calcite_hep_track_a_120_execution_checker_v0 \
  --enable-db-execution \
  --enable-checker
```

No `--collect-timing` flag was passed.

No `python -m cli.main user compute-local-metrics` command was run.
