# PORT_0024 Formal Sanitized Evidence Mapping Pilot

Date: 2026-05-15

## Selection Rationale

PORT_0024 was selected last among the simple and near-simple blocked PORT cases because it adds one extra evidence class beyond the repeated PORT_0008, PORT_0012, PORT_0013, PORT_0022, and PORT_0025 pattern. It has the same two validated sanitized Spark plan copies, plus a validated sanitized Spark result-check summary for stdout/stderr log-reference handling.

This pilot applies the accepted evidence-mapping-only pattern while explicitly retaining the original Spark result-check record through mapping and exposing only the sanitized summary in public retained evidence.

## Trial Artifacts Promoted

| Trial artifact | Formal public path | SHA256 |
|---|---|---|
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0024/spark/plans/rewrite_neg_01.sanitized.txt` | `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_neg_01.sanitized.txt` | `a817ef84cbb90b8e78c5b5f083a19f3e99ddfee8b87597af9552aa9f79bf149b` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0024/spark/plans/rewrite_pos_01.sanitized.txt` | `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_pos_01.sanitized.txt` | `46903965a592b0c33af93187bd23de12fa4e6b4b2770635de01376e9d8bcb4a1` |
| `audits/port_manual_review_resolution/sanitized_trial/PORT_0024/spark/result_check.sanitized_summary.json` | `cases/PORT/PORT_0024/evidence/retained_controls/spark_result_check.sanitized_summary.json` | `da9cd4a81b4eae12ac2327608b0f4b1e62051977e86cf5c5178c43009f1aac02` |

## Original Legacy Files Mapped

| Original legacy file | Evidence role | Original SHA256 | Original status |
|---|---|---|---|
| `cases/PORT/PORT_0024/runs/spark/plans/rewrite_neg_01.txt` | hard-negative rejection evidence; plan/failure observability | `a8a258f87a1ef14609200c386a7b632dacf33d14b6bc264bc4b8467bb7b711dc` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0024/runs/spark/plans/rewrite_pos_01.txt` | plan/failure observability | `7367c17e13107a19fd52106c3254aff8d322c73a2e6885de11e847fec6e6cec4` | do-not-delete; retained through mapping |
| `cases/PORT/PORT_0024/runs/spark/result_check.json` | control validation | `c282f7678f45380212f0db883d130ee6b70a5d5bdfc4f730370835b003e511f1` | do-not-delete; retained through mapping |

## Future Public Paths Realized

The following paths proposed by the sanitized trial mapping are now realized:

- `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0024/evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `cases/PORT/PORT_0024/evidence/retained_controls/spark_result_check.sanitized_summary.json`

The case-local retention mapping is now realized at:

- `cases/PORT/PORT_0024/evidence/runs_retention.yaml`

## Result-Check Log-Reference Handling

The public retained result-check artifact is a sanitized summary, not a raw log export. It preserves non-sensitive Spark control-validation fields and replaces stdout/stderr log path values with placeholders.

Raw stdout/stderr logs were not copied, inspected, or exposed. Raw log references and any raw logs that exist in legacy remain private/archive-only unless separately reviewed and approved.

## Validation Results

The formal sanitized plan copies and result-check summary match the validated trial artifacts by SHA256. The case-local `runs_retention.yaml` parses as YAML. The formal result-check summary parses as JSON. The formal public pilot files passed the configured hygiene scan for maintainer-local paths, local URI traces, host endpoints, platform traces, credential-keyword traces, and raw stdout/stderr log path traces.

## Pilot Boundary

This remains an evidence-mapping pilot, not a full case migration. It does not migrate source SQL, rewrite SQL, schema, checker, validation scripts, manifest, raw runs, provenance, taxonomy files, or raw stdout/stderr logs. It does not rerun engines, regenerate plans, change Common-core membership, change denominators, change paper results, change case admission, change benchmark claims, or modify route evidence.

No legacy evidence was modified, sanitized in place, moved, deleted, renamed, overwritten, or copied as raw retained public evidence.

## Remaining Work Before Full PORT_0024 Case Migration

- Decide and execute the full case package layout for PORT_0024.
- Migrate source SQL, rewrite SQL, schema, checker, validation, manifest, provenance, and taxonomy files through an approved copy-first process.
- Preserve or archive all raw legacy evidence through reviewed mapping.
- Resolve private/archive handling for raw stdout/stderr logs if full migration needs those references.
- Re-run package-level public hygiene checks after full migration.
- Keep denominator, paper results, case admission, benchmark claims, and Common-core membership unchanged unless separately approved.
