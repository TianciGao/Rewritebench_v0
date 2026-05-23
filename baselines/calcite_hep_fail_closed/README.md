# Calcite HEP Fail-Closed Baseline

This directory contains the route-specific Calcite HEP fail-closed baseline
adapter for local user-entry runs.

Run through the existing user facade by passing the adapter as a command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_run \
  --run-id calcite_hep_fail_closed_smoke
```

Runtime discovery is environment-variable based:

- `SQLRB_CALCITE_HEP_CMD`: external command that accepts `--case-id`,
  `--source-sql`, `--ddl`, `--output-sql`, and `--mode`.
- `SQLRB_CALCITE_HEP_JAR`: optional runnable JAR using the same argument shape.
- `SQLRB_CALCITE_HEP_ROOT`: optional external runtime working directory.
- `SQLRB_CALCITE_HEP_JAVA`: optional Java command, defaulting to `java`.
- `SQLRB_CALCITE_HEP_MODE`: optional runtime mode, defaulting to
  `real_route_canary`.
- `SQLRB_CALCITE_HEP_TIMEOUT`: optional invocation timeout in seconds,
  defaulting to `30`.

The adapter writes a per-row `calcite_hep_status.json` file in the user-run
workspace. It emits candidate SQL only when the external runtime exits
successfully and writes a non-empty candidate file. Missing runtime, missing
schema DDL, command failure, timeout, or empty output all fail closed without
candidate SQL.

No Calcite source code, JARs, native libraries, build outputs, or dependency
caches belong in this repository.
