# PORT_0013 Formal Sanitized Evidence Mapping Pilot

Date: 2026-05-15

## Selection Rationale

PORT_0013 was selected after PORT_0008 and PORT_0012 because those formal pilots established and repeated the accepted case-local evidence-mapping-only pattern. PORT_0013 has the same simple Route B trial shape: two validated sanitized Spark plan copies, no result-check summary, and no full case migration requirement.

This pilot applies the accepted pattern to the next blocked PORT case while preserving the same boundaries: promote validated sanitized trial plan copies into a case-local release evidence slice without migrating the full case package.

## Trial Artifacts Promoted

| Trial artifact | Formal public path | SHA256 |
|---|---|---|
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0013/spark/plans/rewrite_neg_01.sanitized.txt` | `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_neg_01.sanitized.txt` | `8ae6c607b5fe2ddfad5d63894b99434b256e718d565f902e7d39a503123955c7` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0013/spark/plans/rewrite_pos_01.sanitized.txt` | `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_pos_01.sanitized.txt` | `69ce09402cb6c16d29da5fff45e1fbe06f018fc3c68a991709e59b4fc2600404` |

## Original Legacy Files Mapped

| Original legacy file | Evidence role | Original SHA256 | Original status |
|---|---|---|---|
| `cases/PORT/PORT_0013/runs/spark/plans/rewrite_neg_01.txt` | hard-negative rejection evidence; plan/failure observability | `bd328ea7e167ad3b935ad39eabf5a0b84b94481184f6656fbbc625ed2bd4e7ac` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0013/runs/spark/plans/rewrite_pos_01.txt` | plan/failure observability | `e4ed8f4908a7356054c56c13fe293bbad624e2606a6dfec188fbde54d0d7e227` | do-not-delete; retained through mapping |

## Future Public Paths Realized

The following paths proposed by the sanitized trial mapping are now realized:

- `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0013/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

The case-local retention mapping is now realized at:

- `cases/PORT/PORT_0013/evidence/runs_retention.yaml`

## Validation Results

The formal sanitized plan copies match the validated trial artifacts by SHA256. The case-local `runs_retention.yaml` parses as YAML. The formal public pilot files passed the configured hygiene scan for maintainer-local paths, local URI traces, host endpoints, platform traces, and credential-keyword traces.

## Pilot Boundary

This remains an evidence-mapping pilot, not a full case migration. It does not migrate source SQL, rewrite SQL, schema, checker, validation scripts, manifest, raw runs, provenance, or taxonomy files. It does not rerun engines, regenerate plans, change Common-core membership, change denominators, change paper results, change case admission, change benchmark claims, or modify route evidence.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw retained public evidence.

## Remaining Work Before Full PORT_0013 Case Migration

- Decide and execute the full case package layout for PORT_0013.
- Migrate source SQL, rewrite SQL, schema, checker, validation, manifest, provenance, and taxonomy files through an approved copy-first process.
- Preserve or archive all raw legacy evidence through reviewed mapping.
- Re-run package-level public hygiene checks after full migration.
- Keep denominator, paper results, case admission, benchmark claims, and Common-core membership unchanged unless separately approved.
