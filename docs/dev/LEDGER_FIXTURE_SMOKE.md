# Ledger Fixture Smoke

Developer-facing note. This is not public runner documentation.

## Purpose

`scripts/dev/smoke_ledger_fixtures.py` is a short developer-only entrypoint for running the synthetic ledger fixture validator with the base and hardening fixture sets.

The smoke check is synthetic-fixture only. It does not parse production retained evidence, implement adapters, compute metrics, run DB engines, or render paper tables.

## Command

```bash
python scripts/dev/smoke_ledger_fixtures.py
```

Optional overrides are available:

```bash
python scripts/dev/smoke_ledger_fixtures.py \
  --fixtures-dir audits/ledger_schema_validation_fixtures \
  --extra-fixtures audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv \
  --extra-expected audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv \
  --out-dir audits/ledger_fixture_dev_smoke
```

## Expected Outputs

The default smoke run writes:

- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_validation_results.csv`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_validator_hardening_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_summary.json`

## What It Validates

- Synthetic fixture safety flags.
- Expected-valid and expected-invalid fixture outcomes.
- Record-type required and forbidden field behavior.
- Duplicate ID detection.
- Status vocabulary and obvious status consistency checks.
- Static denominator scaffold joins used by the fixture validator.

## What It Does Not Validate

- Real retained evidence.
- Legacy reports/results/runs.
- Real case package evidence.
- Production ledger adapters.
- Metric aggregates.
- Paper tables.
- Public runner behavior.

## If It Fails

Check:

- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_validation_results.csv`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_validator_hardening_report.md`

A non-zero smoke exit means the underlying fixture validator failed. Do not treat this as a production benchmark failure; it only indicates that synthetic schema/validator expectations need review.
