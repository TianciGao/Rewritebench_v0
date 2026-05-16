# CONS_0005 Canonical Full Case Migration Pilot

Date: 2026-05-16

## Scope

This report records the one-case copy-first canonical-layout full case migration pilot for `CONS_0005`. It is not Common-core 40 migration, not batch migration, not DB validation, and not evidence regeneration.

## Why CONS_0005 After PORT Pilots

`PORT_0004` tested copy-first full migration in a legacy-compatible layout. `PORT_0008` tested canonical layout and sanitized retained Spark plan integration. `CONS_0005` tests canonical layout for a checker-heavy CONS semantic-guard case with hard-negative packaging.

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

## What CONS Tests That PORT Did Not

`CONS_0005` tests hard-negative semantics, checker configuration, expected-rejection metadata, and witness packaging for correlated `NOT IN` with NULL-sensitive behavior.

## Copied And Generated File Groups

- SQL copied into `sql/`.
- DDL and witness load SQL copied into `schema/<engine>/`.
- Checker YAML generated under `checker/`.
- Validation assets generated as retained legacy validation assets with output-policy caveat.
- Public-safe retained JSON/TSV evidence promoted into `evidence/`.
- Spark plan text evidence sanitized into `evidence/retained_plans/spark/`.
- Metadata generated under `metadata/`.
- Notes copied or generated under `notes/`.

## Hard-Negative Expected Rejection Approval

The expected rejection for `neg_01` is maintainer-approved for migration. `rewrite_neg_01.sql` does not preserve NULL-sensitive correlated `NOT IN` semantics. On retained witness evidence, source and positive outputs are empty, while the negative output is `1\t3`.

## Checker And Witness Semantics

The checker model is engine-local witness guarding: source equals positive, and source differs from negative, for PostgreSQL, MySQL, and Spark retained outputs. The witness discriminator is a NULL value in `table2.i`.

## Spark Plan Sanitization Handling

Raw legacy Spark plan text files contain local temporary path traces. Raw Spark plans were not copied into public retained evidence. Sanitized public copies were created under `evidence/retained_plans/spark/`, preserving plan operators, table names, column names, expressions, and structure.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not final public user runners, and future public runner output must not write to case-local `runs/` by default.

## Validator v0.3 Results

- Full-case validator result: PASS 1/1 for `CONS_0005`.
- Canonical-case validator result: PASS 1/1 for `CONS_0005`.
- Evidence-pilot regression result: PASS 6/6 for the six blocked-PORT evidence-pilot slices.
- Full-case regression result: PASS 2/2 for `PORT_0004` and `PORT_0008`.

## Public Hygiene Scan Results

Public hygiene scan passed for `cases/CONS/CONS_0005`. Raw Spark plan local temporary path traces were removed from public sanitized copies.

## Claim Boundary

Denominator, paper results, Common-core membership, case admission status, and raw legacy evidence were not changed. No global leaderboard was introduced.

## Remaining Risks

- Validation scripts are retained assets, not final public runner entrypoints.
- Spark plan sanitized copies should be reviewed for evidence-preserving redaction.
- CONS checker semantics are approved for this migration, but future cross-pool rollout still needs review case by case.
