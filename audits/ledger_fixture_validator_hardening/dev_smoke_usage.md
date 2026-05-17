# Ledger Fixture Validator Dev Smoke Usage

This is a developer-facing smoke check for synthetic ledger fixtures. It is not public runner documentation.

## Command

Base fixtures only:

```bash
python scripts/dev/validate_ledger_fixtures.py \
  --fixtures-dir audits/ledger_schema_validation_fixtures \
  --out-dir audits/ledger_fixture_validator_hardening
```

Base plus hardening fixtures:

```bash
python scripts/dev/validate_ledger_fixtures.py \
  --fixtures-dir audits/ledger_schema_validation_fixtures \
  --extra-fixtures audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv \
  --extra-expected audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv \
  --out-dir audits/ledger_fixture_validator_hardening
```

## Expected Outputs

- `ledger_fixture_hardening_validation_results.csv`
- `ledger_fixture_hardening_summary.json`
- `ledger_fixture_validator_hardening_report.md`

The summary JSON should report `metrics_computed=false`, `production_retained_evidence_parsed=false`, and `adapter_implemented=false`.

## What Failure Means

A non-zero exit means at least one expected-valid synthetic row failed, one expected-invalid synthetic row passed unexpectedly, a required fixture file was missing, a denominator join expectation failed, fixture safety flags were missing, or a disallowed read path was detected.

## What It Does Not Validate

This smoke check does not validate real retained evidence, legacy reports/results, real case runs, migrated case packages, paper tables, production ledgers, or metric aggregates.

## Position In The Workflow

Use this before production retained-evidence adapter work to confirm the schema and record-type validator skeleton can reject known-bad synthetic rows and accept known-good synthetic rows. Production adapter implementation and metrics computation remain unauthorized until a separate task approves them.
