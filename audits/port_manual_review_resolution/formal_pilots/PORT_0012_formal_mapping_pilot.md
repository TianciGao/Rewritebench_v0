# PORT_0012 Formal Sanitized Evidence Mapping Pilot

Date: 2026-05-15

## Selection Rationale

PORT_0012 was selected after PORT_0008 because the PORT_0008 formal evidence-mapping pilot established the accepted case-local pattern, and PORT_0012 has the same simple Route B trial shape: two validated sanitized Spark plan copies, no result-check summary, and no full case migration requirement.

This pilot applies the accepted pattern to the next blocked PORT case while preserving the same boundaries: promote validated sanitized trial plan copies into a case-local release evidence slice without migrating the full case package.

## Trial Artifacts Promoted

| Trial artifact | Formal public path | SHA256 |
|---|---|---|
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0012/spark/plans/rewrite_neg_01.sanitized.txt` | `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_neg_01.sanitized.txt` | `27690fa27aae026bd753ae819a9f33bf94dbf044af89d10ff969bf921779dcff` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0012/spark/plans/rewrite_pos_01.sanitized.txt` | `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_pos_01.sanitized.txt` | `d35497911d20b8234c873fa197968d2001cc98afc0066b2cde81fb5d823879ee` |

## Original Legacy Files Mapped

| Original legacy file | Evidence role | Original SHA256 | Original status |
|---|---|---|---|
| `cases/PORT/PORT_0012/runs/spark/plans/rewrite_neg_01.txt` | hard-negative rejection evidence; plan/failure observability | `4e433dfa12f87f328dae4f78dc657dbb069b90b362127a790dd02551204fdf44` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0012/runs/spark/plans/rewrite_pos_01.txt` | plan/failure observability | `f919e498a14741bc34a19d1e259e6f1cd33ed954ba34a158400872a708639dfe` | do-not-delete; retained through mapping |

## Future Public Paths Realized

The following paths proposed by the sanitized trial mapping are now realized:

- `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0012/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

The case-local retention mapping is now realized at:

- `cases/PORT/PORT_0012/evidence/runs_retention.yaml`

## Validation Results

The formal sanitized plan copies match the validated trial artifacts by SHA256. The case-local `runs_retention.yaml` parses as YAML. The formal public pilot files passed the configured hygiene scan for maintainer-local paths, local URI traces, host endpoints, platform traces, and credential-keyword traces.

## Pilot Boundary

This remains an evidence-mapping pilot, not a full case migration. It does not migrate source SQL, rewrite SQL, schema, checker, validation scripts, manifest, raw runs, provenance, or taxonomy files. It does not rerun engines, regenerate plans, change Common-core membership, change denominators, change paper results, change case admission, change benchmark claims, or modify route evidence.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw retained public evidence.

## Remaining Work Before Full PORT_0012 Case Migration

- Decide and execute the full case package layout for PORT_0012.
- Migrate source SQL, rewrite SQL, schema, checker, validation, manifest, provenance, and taxonomy files through an approved copy-first process.
- Preserve or archive all raw legacy evidence through reviewed mapping.
- Re-run package-level public hygiene checks after full migration.
- Keep denominator, paper results, case admission, benchmark claims, and Common-core membership unchanged unless separately approved.
