# PERF_0006 Canonical Full Case Migration Pilot

Date: 2026-05-16

## Scope

This report records the one-case copy-first canonical-layout full case migration pilot for `PERF_0006`. It is not Common-core 40 migration, not batch migration, not DB validation, and not evidence regeneration.

## Why PERF_0006 After PORT And CONS Pilots

`PORT_0004` tested copy-first full migration in a legacy-compatible layout. `PORT_0008` tested canonical layout and sanitized retained evidence integration. `CONS_0005` tested checker-heavy hard-negative packaging. `PERF_0006` tests canonical layout for a performance-sensitive analytical rewrite case while preserving the no-new-speedup boundary.

## Legacy State Snapshot

- legacy pwd: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- branch: `artifact/case-package-contract-alignment-clean`
- HEAD: `7e438b5d767922007a1ca456fed0bf2e237a8952`
- status:

```text
## artifact/case-package-contract-alignment-clean...origin/artifact/case-package-contract-alignment-clean [behind 7]
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt
 M reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
```

- diff name-status:

```text
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
```

- recent commits:

```text
7e438b5d docs: rewrite README for common-core reproducibility
6eefb7c2 docs: rewrite README for common-core reproducibility
c1cc0ff1 artifacts: add common-core reproduction input bundle
```

The dirty report files are pre-existing. This task did not alter the legacy repo.

## What PERF Tests That PORT And CONS Did Not

`PERF_0006` is a TPC-H Q1-derived analytical aggregation case. The positive rewrite isolates the cutoff filter in a derived relation before aggregation. The hard negative changes the cutoff predicate from less-than-or-equal to strict less-than. The pilot tests whether canonical packaging can represent performance-sensitive rewrite pressure without creating timing, ranking, leaderboard, or paper-result claims.

## Copied And Generated File Groups

- SQL copied into `sql/`.
- DDL and witness load SQL copied into `schema/<engine>/`.
- Checker YAML generated under `checker/`.
- Validation assets adapted as retained legacy validation assets with output-policy caveat.
- Public-safe retained JSON/TSV evidence promoted into `evidence/`.
- Spark plan text evidence sanitized into `evidence/retained_plans/spark/`.
- Metadata generated under `metadata/`.
- Notes generated under `notes/`.

## Rewrite Pressure And Performance Boundary

The rewrite pressure is predicate placement before aggregation. PERF_0006 remains performance-sensitive by design, but this migration did not run timing workloads, did not compute speedup, did not create a leaderboard, and did not change any paper result.

## Hard-Negative Expected Rejection

`neg_01` changes the cutoff predicate from less-than-or-equal to strict less-than. On the retained witness, this excludes the cutoff-date row and changes the aggregated `A/F` group. The checker should accept source/positive equivalence and reject the hard negative.

## Spark Plan Sanitization Handling

Raw legacy Spark plan text files contain local temporary Spark path traces. Raw Spark plans were not copied into public retained evidence. Sanitized public copies were created under `evidence/retained_plans/spark/`, preserving plan operators, table names, column names, expressions, and structure.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not final public user runners, and future public runner output must not write to case-local `runs/` by default.

## Validator v0.3 Results

- Full-case validator result: PASS 1/1 for `PERF_0006`.
- Canonical-case validator result: PASS 1/1 for `PERF_0006`.
- Evidence-pilot regression result: PASS 6/6 for the six blocked-PORT evidence-pilot slices.
- Full-case regression result: PASS 3/3 for `PORT_0004`, `PORT_0008`, and `CONS_0005`.

## Public Hygiene Scan Results

Public hygiene scan passed for `cases/PERF/PERF_0006`. Raw Spark plan local temporary path traces were removed from published sanitized copies. Raw Spark plan text was not copied into public retained evidence.

## Claim Boundary

Denominator, paper results, Common-core membership, case admission status, raw legacy evidence, timing evidence, and speedup claims were not changed. No global leaderboard was introduced.

## Remaining Risks

- Validation scripts are retained assets, not final public runner entrypoints.
- Spark plan sanitized copies should be reviewed for evidence-preserving redaction.
- Performance-sensitive retained evidence can be misread as a new speedup claim unless the claim boundary remains visible.
