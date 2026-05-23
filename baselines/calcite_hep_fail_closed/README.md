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

The adapter is intentionally fail-closed until a separately authorized Calcite
HEP runtime invocation contract is available. It writes a per-row
`calcite_hep_status.json` file in the user-run workspace and emits no candidate
SQL when Calcite is unavailable or unsupported.

No Calcite source code, JARs, native libraries, build outputs, or dependency
caches belong in this repository.
