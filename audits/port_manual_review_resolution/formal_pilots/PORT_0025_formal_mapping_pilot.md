# PORT_0025 Formal Sanitized Evidence Mapping Pilot

Date: 2026-05-15

## Selection Rationale

PORT_0025 was selected after PORT_0008, PORT_0012, PORT_0013, and PORT_0022 because those formal pilots established and repeated the accepted case-local evidence-mapping-only pattern. PORT_0025 has the same simple Route B trial shape: two validated sanitized Spark plan copies, no result-check summary, and no full case migration requirement.

This pilot applies the accepted pattern to the next blocked PORT case while preserving the same boundaries: promote validated sanitized trial plan copies into a case-local release evidence slice without migrating the full case package.

## Trial Artifacts Promoted

| Trial artifact | Formal public path | SHA256 |
|---|---|---|
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0025/spark/plans/rewrite_neg_01.sanitized.txt` | `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_neg_01.sanitized.txt` | `fe1b371ffa252ffc79a4eb86c78ddf2ad127d5c11328731eb730ef15bf9391f5` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0025/spark/plans/rewrite_pos_01.sanitized.txt` | `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_pos_01.sanitized.txt` | `1c97873f0a2a689dfd79cbef886daf7cab50651c7b0cd74e8c1b3bcc7dbe1650` |

## Original Legacy Files Mapped

| Original legacy file | Evidence role | Original SHA256 | Original status |
|---|---|---|---|
| `cases/PORT/PORT_0025/runs/spark/plans/rewrite_neg_01.txt` | hard-negative rejection evidence; plan/failure observability | `e864de8e4663e4d260efb6cc1130c553a9480fe6c33c9052f9cee3e4ee3d35af` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0025/runs/spark/plans/rewrite_pos_01.txt` | plan/failure observability | `1284d645eb258ca97172cece2fe95f02b59e9dc40f794d432310a3423ec8145a` | do-not-delete; retained through mapping |

## Future Public Paths Realized

The following paths proposed by the sanitized trial mapping are now realized:

- `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0025/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

The case-local retention mapping is now realized at:

- `cases/PORT/PORT_0025/evidence/runs_retention.yaml`

## Validation Results

The formal sanitized plan copies match the validated trial artifacts by SHA256. The case-local `runs_retention.yaml` parses as YAML. The formal public pilot files passed the configured hygiene scan for maintainer-local paths, local URI traces, host endpoints, platform traces, and credential-keyword traces.

## Pilot Boundary

This remains an evidence-mapping pilot, not a full case migration. It does not migrate source SQL, rewrite SQL, schema, checker, validation scripts, manifest, raw runs, provenance, or taxonomy files. It does not rerun engines, regenerate plans, change Common-core membership, change denominators, change paper results, change case admission, change benchmark claims, or modify route evidence.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw retained public evidence.

## Remaining Work Before Full PORT_0025 Case Migration

- Decide and execute the full case package layout for PORT_0025.
- Migrate source SQL, rewrite SQL, schema, checker, validation, manifest, provenance, and taxonomy files through an approved copy-first process.
- Preserve or archive all raw legacy evidence through reviewed mapping.
- Re-run package-level public hygiene checks after full migration.
- Keep denominator, paper results, case admission, benchmark claims, and Common-core membership unchanged unless separately approved.
