# User-Entry External-Schema Repair

## Purpose

This packet records the narrow user-entry repair that preserves the working non-DB adapter-capture path, adds a public smoke convenience, and repairs optional PostgreSQL DB/checker diagnostics to resolve executable schema assets through the current manifest/external-schema contract.

This task did not implement full paper reproduction, compute official metrics, render paper tables, update reports/results, parse retained evidence, or create a global leaderboard.

## Changes

- Added `--smoke` to the user-entry CLI. It selects the deterministic tiny Common-core subset `PERF_0006` and `CONS_0005` for the requested engine without requiring a case-list file.
- Added a public no-op adapter example at `examples/user/noop_adapter.py`.
- Updated PostgreSQL diagnostic schema resolution to read `manifest.yaml`, resolve `schema.external_profile`, and use the external schema profile `engines.postgres.ddl` / `engines.postgres.load` paths.
- Added fail-closed behavior for missing manifest schema metadata, missing external schema profiles, missing PostgreSQL engine entries, missing DDL/load fields, and missing external schema files.
- Updated `docs/USER_BENCHMARK_GUIDE.md` to separate supported non-DB public smoke, optional local PostgreSQL diagnostics, and deferred paper reproduction/metrics/reporting work.
- Added user-entry tests for smoke selection, output-root behavior, external schema resolution, and fail-closed DB execution when external schema metadata is missing.

## Public Smoke

Dry-run smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dry_run \
  --dry-run
```

Adapter-capture smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dummy_adapter
```

Both smoke commands are non-DB by default and write only local user-run diagnostics under `runs/user/`.

## Optional DB/Checker Diagnostics

Optional PostgreSQL diagnostics now resolve DDL/load files through external schema profiles. They remain local diagnostics only and require explicit opt-in with `--enable-db-execution` and, if desired, `--enable-checker`.

Live DB/checker execution was not run by this task.

## Boundaries

- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results changed: no.
- Global leaderboard created: no.
