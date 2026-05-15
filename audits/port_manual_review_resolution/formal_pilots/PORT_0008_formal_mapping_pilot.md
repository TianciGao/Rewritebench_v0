# PORT_0008 Formal Sanitized Evidence Mapping Pilot

Date: 2026-05-15

## Selection Rationale

PORT_0008 was selected as the first formal sanitized evidence mapping pilot because it was one of the PORT manual-review cases blocked by Spark plan local-path traces, and its Route B sanitized trial produced exactly two validated Spark plan copies with clean validation results.

This pilot tests the smallest approved public evidence step: promote validated sanitized trial plan copies into a case-local release evidence slice without migrating the full case package.

## Trial Artifacts Promoted

| Trial artifact | Formal public path | SHA256 |
|---|---|---|
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0008/spark/plans/rewrite_neg_01.sanitized.txt` | `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_neg_01.sanitized.txt` | `df0bcc0de1632e7133d9a77e3595b2dd60101dc2f91b29ac58410c84a9f1e729` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0008/spark/plans/rewrite_pos_01.sanitized.txt` | `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_pos_01.sanitized.txt` | `e8317a249410ee59f5e402fe19215b65091d372983e2ea73bca0f060d5f04714` |

## Original Legacy Files Mapped

| Original legacy file | Evidence role | Original SHA256 | Original status |
|---|---|---|---|
| `cases/PORT/PORT_0008/runs/spark/plans/rewrite_neg_01.txt` | hard-negative rejection evidence; plan/failure observability | `2146046367e919a55fff5dda9397c609e1c3e02193d775199d7bade555bc27e4` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0008/runs/spark/plans/rewrite_pos_01.txt` | plan/failure observability | `993254c3463361a374300a240949ac7bc6b9662b3c36a7b2579b716fb0ee49af` | do-not-delete; retained through mapping |

## Future Public Paths Realized

The following paths proposed by the sanitized trial mapping are now realized:

- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

The case-local retention mapping is now realized at:

- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`

## Validation Results

The formal sanitized plan copies match the validated trial artifacts by SHA256. The case-local `runs_retention.yaml` parses as YAML. The formal public pilot files passed the configured hygiene scan for maintainer-local paths, local URI traces, host endpoints, platform traces, and credential-keyword traces.

## Pilot Boundary

This remains an evidence-mapping pilot, not a full case migration. It does not migrate source SQL, rewrite SQL, schema, checker, validation scripts, manifest, raw runs, provenance, or taxonomy files. It does not rerun engines, regenerate plans, change Common-core membership, change denominators, change paper results, or modify route evidence.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw retained public evidence.

## Remaining Work Before Full PORT_0008 Case Migration

- Decide and execute the full case package layout for PORT_0008.
- Migrate source SQL, rewrite SQL, schema, checker, validation, manifest, provenance, and taxonomy files through an approved copy-first process.
- Preserve or archive all raw legacy evidence through reviewed mapping.
- Re-run package-level public hygiene checks after full migration.
- Keep denominator, paper results, and Common-core membership unchanged unless separately approved.
