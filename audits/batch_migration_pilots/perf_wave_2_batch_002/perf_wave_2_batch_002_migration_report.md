# PERF Wave-2 Sanitized-Plan Canonical Migration Batch 002

Date: 2026-05-16
Batch id: `perf_wave_2_sanitized_plan_batch_002`
Selected cases: `PERF_0017`, `PERF_0019`, `PERF_0024`

## Scope

This was a bounded three-case PERF migration batch following the completed `PERF_0006` canonical-layout pattern and the successful PERF wave-2 batch 001 pattern. It was not blind Common-core 40 migration and it was not full Common-core 40 migration. No DB validation, evidence regeneration, timing rerun, speedup computation, benchmark result row creation, denominator change, paper-result change, case membership change, or raw legacy evidence mutation was performed.

## Why This Batch Follows PERF_0006 And Batch 001

All three cases are TPC-H-derived performance-sensitive analytical rewrite cases with root-level legacy SQL, engine DDL/load scripts, retained cross-dialect result evidence, retained plan evidence, hard-negative outputs, and Spark plan text files containing local temporary path traces. The batch reused the `PERF_0006` and batch 001 canonical pattern: canonical SQL/schema/checker/evidence/metadata layout, sanitized public Spark plan evidence, no raw `runs/` wholesale copy, and explicit no-speedup boundary.

## Per-Case Migration Result

- `PERF_0017`: pass; hard-negative reason static-inferred as `return_flag_predicate_changed`.
- `PERF_0019`: pass; hard-negative reason static-inferred as `excluded_comment_phrase_changed`.
- `PERF_0024`: pass; hard-negative reason static-inferred as `part_name_prefix_predicate_changed`.

All three selected cases were attempted and completed as canonical public-release packages. No cases were failed or deferred.

## Validation Result

- SHA256 copy validation: PASS for copied legacy files; generated, adapted, and sanitized derivatives are recorded separately in the file inventory.
- Public hygiene scan: PASS for all three migrated case directories.
- YAML validation: PASS for all migrated case YAML files.
- JSON validation: PASS for all migrated case evidence/metadata JSON files.
- Validator v0.3 full-case: PASS 3/3.
- Validator v0.3 canonical-case: PASS 3/3.
- Evidence-pilot regression: PASS 6/6.
- Full-case regression: PASS 8/8.
- Canonical-case regression: PASS 7/7.

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

- Hard-negative reasons are static-inferred for the three cases unless later maintainer review records stronger approval.
- Adapted validation scripts remain legacy assets and should not be treated as final public runners.
- Batch scale should remain bounded and reviewed before selecting the next wave.

## Next Safe Action

Human review this bounded PERF wave-2 batch 002. If accepted, choose the next small reviewed wave from the readiness audit; do not start blind full Common-core 40 migration.
