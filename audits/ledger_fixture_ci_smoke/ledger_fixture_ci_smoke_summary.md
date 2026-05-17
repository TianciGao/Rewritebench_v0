# Ledger Fixture CI Smoke Summary

Date: 2026-05-17

## Purpose And Scope

This task adds lightweight GitHub Actions wiring for the synthetic ledger fixture smoke validator.

The workflow is developer/CI protection for ledger schema, fixture, and validator changes. It does not parse production retained evidence, implement retained-evidence adapters, compute metrics, run DB engines, update reports/results, render paper tables, change denominators, change paper results, or modify raw legacy evidence.

## Workflow Created

- `.github/workflows/ledger-fixture-smoke.yml`
- Workflow name: `Ledger fixture smoke`
- Triggers: `pull_request`, `push`, `workflow_dispatch`
- Runner: `ubuntu-latest`
- Python: `3.11`

## Commands Run

The workflow runs:

```bash
python -m py_compile scripts/dev/validate_ledger_fixtures.py
python -m py_compile scripts/dev/smoke_ledger_fixtures.py
python scripts/dev/smoke_ledger_fixtures.py
```

It uploads the synthetic smoke outputs from `audits/ledger_fixture_dev_smoke/` as a workflow artifact.

## Local Validation Result

Local validation passed:

- `python -m py_compile scripts/dev/validate_ledger_fixtures.py`
- `python -m py_compile scripts/dev/smoke_ledger_fixtures.py`
- `python scripts/dev/smoke_ledger_fixtures.py`

The local smoke run checked 38 synthetic fixture rows, passed 17/17 expected-valid rows, rejected 21/21 expected-invalid rows as expected, and reported zero unexpected passes or failures.

## Non-Goals

- No production retained evidence parsing.
- No retained-evidence adapter implementation.
- No metrics computation.
- No unified reproduction CLI or public runner implementation.
- No paper table rendering.
- No reports/results migration or mutation.
- No DB engine setup or validation.
- No denominator, paper-result, case membership, case package, or raw legacy evidence changes.

## Next Safe Action

Monitor the CI workflow on subsequent pushes and pull requests. The next safe planning task is production ledger validation-gate design only; do not parse production retained evidence, implement adapters, compute metrics, or render paper tables without separate authorization.
