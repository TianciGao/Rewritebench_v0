# PERF Wave-2 Final Sanitized-Plan Canonical Migration Batch

Date: 2026-05-16
Batch id: `perf_wave_2_final_batch`
Selected cases: `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`

## Scope

This was a bounded six-case final PERF wave migration following the completed `PERF_0006` canonical-layout pattern and successful PERF wave-2 batch 001/002/003 patterns. It was not blind Common-core 40 migration and it was not full Common-core 40 migration. No DB validation, evidence regeneration, timing rerun, speedup computation, benchmark result row creation, denominator change, paper-result change, case membership change, or raw legacy evidence mutation was performed.

## Legacy State Snapshot

- Legacy repo path: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.
- Legacy branch: `artifact/case-package-contract-alignment-clean`.
- Legacy HEAD at preflight: `7e438b5d767922007a1ca456fed0bf2e237a8952`.
- Legacy status: pre-existing dirty report/script files under `reports/evaluation/common_core_v0/`; unchanged by this task.

## Why This Batch Follows PERF_0006 And Prior PERF Batches

The selected cases are the remaining PERF Common-core cases in the same sanitized-plan risk class. They have root-level legacy SQL, engine DDL/load scripts, retained result evidence, retained plan evidence, hard-negative outputs, and Spark plan text files containing local temporary path traces. The batch reused the canonical SQL/schema/checker/evidence/metadata layout, sanitized public Spark plan evidence, no raw `runs/` wholesale copy, and explicit no-speedup boundary.

## Per-Case Migration Result

- `PERF_0052`: migrated; hard-negative reason static-inferred as `store_state_predicate_changed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `PERF_0054`: migrated; hard-negative reason static-inferred as `manufacturer_id_predicate_changed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `PERF_0056`: migrated; hard-negative reason static-inferred as `having_count_threshold_changed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `PERF_0062`: migrated; hard-negative reason static-inferred as `year_filter_predicate_changed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `PERF_0077`: migrated; hard-negative reason static-inferred as `keyword_like_predicate_narrowed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.
- `PERF_0082`: migrated; hard-negative reason static-inferred as `company_type_predicate_changed`; sanitized Spark source, positive, and hard-negative plans; validation scripts adapted with output-policy caveat.

All six selected cases were attempted and completed as canonical public-release packages. No cases were failed or deferred.

## Validation Result

- SHA256 copy validation: PASS for copied legacy files; generated, adapted, and sanitized derivatives are recorded separately in the file inventory.
- Public hygiene scan: PASS for all six migrated case directories.
- YAML validation: PASS for all migrated case YAML files.
- JSON validation: PASS for all migrated case evidence/metadata JSON files.
- Validator v0.3 full-case: PASS 6/6 for the new final PERF batch.
- Validator v0.3 canonical-case: PASS 6/6 for the new final PERF batch.
- Evidence-pilot regression: PASS 6/6.
- Full-case regression: PASS 20/20. This regression included the six new cases after migration.
- Canonical-case regression: PASS 19/19. This regression included the six new cases after migration.

## Sanitized Spark Plan Handling

Raw Spark plan text files were not copied into public retained evidence. Sanitized public copies were generated under each case's `evidence/retained_plans/spark/` directory with local temporary paths redacted. Raw originals are mapped in `evidence/runs_retention.yaml` as do-not-delete originals retained in the legacy repository.

## Performance Boundary

No timing run was executed. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation remains limited to retained denominator-aware paper evidence.

## Validation Script Caveat

Validation scripts are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.

## Invariants

- Legacy repo modified: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Speedup/timing claim created: no.

## Remaining Risks

- Hard-negative reasons are static-inferred unless later maintainer review records stronger approval.
- Adapted validation scripts remain legacy assets and should not be treated as final public runners.
- The PERF pool Common-core canonical migration is complete at case-package level after all six final batch cases passed validators. This does not mean Common-core 40 migration is complete.

## Next Safe Action

Human review the completed PERF pool canonical migration. Next safe action is to select the next reviewed non-PERF wave from the readiness audit; do not start blind full Common-core 40 migration.
