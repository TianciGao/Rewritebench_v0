# Static Case Package Validator v0.1 Report

Date: 2026-05-15

Mode: `evidence-pilot`

Validator command:

```bash
python scripts/dev/validate_case_package.py \
  --mode evidence-pilot \
  --case cases/PORT/PORT_0008 \
  --case cases/PORT/PORT_0012 \
  --case cases/PORT/PORT_0013 \
  --case cases/PORT/PORT_0022 \
  --case cases/PORT/PORT_0025 \
  --case cases/PORT/PORT_0024 \
  --json-output audits/port_manual_review_resolution/static_case_package_validator_v0_1_results.json
```

## Scope

This report records the first formal static case-package validator run for the completed blocked-PORT formal sanitized evidence-mapping pilot series.

Cases checked:

- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `PORT_0024`

This is a static release-repo check only. It is not DB validation, full case migration, evidence regeneration, denominator update, paper-result update, or case admission.

## Validation Summary

| case_id | status | YAML | sanitized plan scan | formal validation CSV | result-check summary |
|---|---:|---:|---:|---:|---:|
| `PORT_0008` | pass | pass | pass | pass | not required |
| `PORT_0012` | pass | pass | pass | pass | not required |
| `PORT_0013` | pass | pass | pass | pass | not required |
| `PORT_0022` | pass | pass | pass | pass | not required |
| `PORT_0025` | pass | pass | pass | pass | not required |
| `PORT_0024` | pass | pass | pass | pass | pass |

Overall result: pass, 6 of 6 cases passed.

## What v0.1 Checks

- Required evidence-pilot files exist under each release-repo case slice.
- `evidence/runs_retention.yaml` parses and declares `status: formal_evidence_mapping_pilot`.
- Full case migration remains false.
- Denominator and paper-result flags remain false.
- Human approval for the formal pilot is recorded.
- Original Spark plan artifacts are mapped as `do_not_delete_original: true`.
- Sanitized public Spark plan copies are present and marked public-safe.
- Public retained evidence files do not contain forbidden local path, host, or credential-keyword traces.
- Formal validation CSVs exist and record public-safe rows with no raw local path or prompt/API/token traces.
- `PORT_0024` has a JSON-parseable sanitized result-check summary with placeholder log references and no raw stdout/stderr log paths.
- No raw `.log` files are present under the release-repo evidence-pilot case slices.

## Boundaries Confirmed

- Legacy repository modified: no.
- Raw legacy evidence changed: no.
- Full case package migration started: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.

## Artifacts

- Validator implementation: `scripts/dev/validate_case_package.py`
- Validator specification: `repository_spec/static_case_package_validator_v0_1.md`
- Machine-readable result: `audits/port_manual_review_resolution/static_case_package_validator_v0_1_results.json`

## Next Safe Action

Use `validate_case_package.py --mode evidence-pilot` as the static gate for evidence-pilot slices, then design the next validator mode for a copy-first full case migration pilot before migrating a complete case package.
