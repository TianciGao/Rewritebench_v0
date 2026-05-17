# Ledger Fixture Dev Smoke Report

## Command Run

```bash
/usr/bin/python scripts/dev/validate_ledger_fixtures.py --fixtures-dir audits/ledger_schema_validation_fixtures --out-dir audits/ledger_fixture_dev_smoke --extra-fixtures audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv --extra-expected audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv
```

## Files Read

- `audits/ledger_schema_validation_fixtures/fixture_all_record_types.csv`
- `audits/ledger_schema_validation_fixtures/fixture_expected_validation_results.csv`
- `audits/ledger_schema_validation_fixtures/record_type_required_fields_matrix.csv`
- `audits/ledger_schema_validation_fixtures/allowed_status_values.csv`
- `audits/ledger_schema_validation_fixtures/fixture_denominator_join_examples.csv`
- `audits/ledger_fixture_validator_hardening/fixture_hardening_extra_rows.csv`
- `audits/ledger_fixture_validator_hardening/fixture_hardening_expected_results.csv`
- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `case_sets/common_core_v0/controls_360.csv`

## Files Written

- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_validation_results.csv`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_validator_hardening_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_report.md`
- `audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_summary.json`

## Validation Summary

- Smoke passed: true
- Validator return code: 0
- Total fixture rows checked: 38
- Expected-valid rows passed: 17
- Expected-invalid rows failed as expected: 21
- Unexpected pass count: 0
- Unexpected fail count: 0
- Production retained evidence parsed: false
- Metrics computed: false
- Adapter implemented: false

## Explicit Non-Goals

- No production retained evidence was parsed.
- No retained-evidence adapter was implemented.
- No metrics were computed.
- No reports/results were migrated or mutated.
- No DB engines, LLM calls, timing workloads, or paper table renderers were run.
- No denominator values, paper results, case membership, case packages,
  or raw legacy evidence were changed.

## Next Safe Action

Use this developer smoke entrypoint for fixture-only validation before
any separately authorized production ledger validation work. Do not
parse production retained evidence, implement adapters, compute metrics,
or render paper tables without explicit authorization.
