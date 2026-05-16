# CONS Hard-Negative Approved Canonical Migration Batch 002

Date: 2026-05-16
Batch id: `cons_hard_negative_approved_batch_002`
Selected cases: `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`

## Scope

This was a bounded four-case CONS canonical migration following the completed `CONS_0005` canonical checker/hard-negative pattern, the CONS approval sweep, and successful CONS batch 001. It was not blind Common-core 40 migration and it was not full Common-core 40 migration. No DB validation, evidence regeneration, timing rerun, metric computation, benchmark result row creation, denominator change, paper-result change, case membership change, or raw legacy evidence mutation was performed.

## Legacy State Snapshot

- Legacy repo path: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.
- Legacy branch: `artifact/case-package-contract-alignment-clean`.
- Legacy HEAD at preflight: `7e438b5d767922007a1ca456fed0bf2e237a8952`.
- Legacy status: pre-existing dirty report/script files under `reports/evaluation/common_core_v0/`; unchanged by this task.

## Why This Batch Follows CONS_0005, Approval Sweep, And Batch 001

`CONS_0005` established the canonical CONS package pattern for checker-heavy hard-negative cases. CONS batch 001 proved the pattern for four approved CONS cases. This final CONS batch records the maintainer-approved expected rejection reasons for the remaining four CONS Common-core cases.

## Per-Case Migration Result
- `CONS_0012`: migrated; approved hard-negative reason `limit_offset_existence_threshold_lowered`; rewrite_neg_01 lowers the LIMIT/OFFSET-derived existence threshold from at least three matching rows to at least two matching rows. This changes the order/limit boundary. Therefore neg_01 is an intentional hard negative and should be rejected by the checker. Sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `CONS_0024`: migrated; approved hard-negative reason `outer_join_row_preservation_changed`; rewrite_neg_01 changes a LEFT JOIN that preserves left-side employee rows into an INNER JOIN constrained by aggregate EXISTS/HAVING logic. This filters out employee rows that should have been preserved. Therefore neg_01 is an intentional hard negative and should be rejected by the checker. Sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `CONS_0036`: migrated; approved hard-negative reason `group_filter_literal_changed`; rewrite_neg_01 changes the aggregate filter predicate literal from Charlie to Alice. This changes the grouped result. Therefore neg_01 is an intentional hard negative and should be rejected by the checker. Sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `CONS_0037`: migrated; approved hard-negative reason `distinct_aggregate_multiplicity_changed`; rewrite_neg_01 removes DISTINCT from COUNT(DISTINCT dept.name). Under LEFT JOIN, duplicate department-name rows can change the aggregate count. Therefore neg_01 is an intentional hard negative and should be rejected by the checker. Sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.

All four selected cases were attempted and completed as canonical public-release packages. No cases were failed or deferred.

## Validation Result

- SHA256 copy validation: PASS for copied legacy files; generated, adapted, and sanitized derivatives are recorded separately in the file inventory.
- Public hygiene scan: PASS for all four migrated case directories.
- YAML validation: PASS for all migrated case YAML files.
- JSON validation: PASS for all migrated case evidence/metadata JSON files.
- Validator v0.3 full-case: PASS 4/4 for the new CONS batch.
- Validator v0.3 canonical-case: PASS 4/4 for the new CONS batch.
- Evidence-pilot regression: PASS 6/6.
- Full-case regression: PASS 28/28. This regression included the four new CONS batch 002 cases after migration.
- Canonical-case regression: PASS 27/27. This regression included the four new CONS batch 002 cases after migration.
- `python -m py_compile scripts/dev/validate_case_package.py` passed.

## Sanitized Spark Plan Handling

Raw Spark plan text files were not copied into public retained evidence. Sanitized public copies were generated under each case's `evidence/retained_plans/spark/` directory with local temporary paths redacted. Raw originals are mapped in `evidence/runs_retention.yaml` as do-not-delete originals retained in the legacy repository.

## Validation Script Caveat

Validation scripts are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.

## CONS Pool Completion Boundary

All four cases passed validation, so the CONS pool Common-core migration is complete at canonical-layout case-package level. This does not mean Common-core 40 migration is complete.

## Invariants

- Legacy repo modified: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Expected rejection approvals recorded: yes.
- Common-core 40 blind/bulk migration started: no.

## Remaining Risks

- The copied/adapted validation scripts remain retained legacy assets and should not be treated as final public runners.
- Spark raw plan originals remain mapped in legacy and should not be published raw.
- Common-core 40 still has non-CONS pools to complete after this batch.

## Next Safe Action

Human review CONS batch 002 and the completed CONS pool canonical migration. Do not start blind full Common-core 40 migration.
