# Production Ledger Validator Future CLI Design

Status: future design only, not implemented

## Purpose

Design a future non-mutating production ledger validator interface. This file does not create `scripts/dev/validate_production_ledger.py` and does not authorize production retained-evidence parsing.

## Proposed Command

```bash
python scripts/dev/validate_production_ledger.py \
  --ledger results/retained/common_core_v0/evidence_ledger.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --case-registry inventory/case_registry.csv \
  --out audits/production_ledger_validation/<run_id>/
```

## Required Behavior

- Read one materialized production ledger and static release scaffolds.
- Write validation reports only under the explicit `--out` directory.
- Fail closed on schema, record-type, denominator, status, provenance, public hygiene, or no-global-leaderboard violations.
- Never auto-fix a production ledger.
- Never compute metrics.
- Never render paper tables.
- Never write to `reports/`, `results/`, `case_sets/`, `inventory/`, case packages, or case-local `runs/`.
- Never parse raw legacy reports/results/runs unless a separate adapter task has already produced the ledger input.

## Suggested Outputs

- `production_ledger_validation_summary.json`
- `production_ledger_validation_results.csv`
- `production_ledger_denominator_join_results.csv`
- `production_ledger_record_type_results.csv`
- `production_ledger_hygiene_results.csv`
- `production_ledger_validation_report.md`

## Exit-code Policy

Return non-zero if any fail-closed gate fails:

- missing required columns;
- unknown record type;
- missing required record-type fields;
- forbidden populated fields;
- denominator join mismatch;
- invalid status or inconsistent status combination;
- unsafe local path or sensitive trace;
- unexpected metric aggregate output;
- mutation attempt;
- global leaderboard or mixed-denominator aggregate row.

Warnings may be allowed only for explicitly nullable support fields with an approved status or N.A. reason.

## Relationship To Fixture Smoke

The future production validator should be developed after the synthetic fixture smoke workflow remains green. Fixture smoke validates policy shape; the production validator validates adapter output. Passing fixture smoke is necessary but not sufficient for production ledger readiness.
