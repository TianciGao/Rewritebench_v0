# LONGTAIL_0011 Canonical Full Case Migration Pilot

Date: 2026-05-16

## Scope

This audit records the one-case copy-first canonical-layout full case migration pilot for `LONGTAIL_0011`. This is not Common-core 40 migration, not batch migration, not DB validation, and not evidence regeneration.

## Why LONGTAIL_0011 Was Selected

`LONGTAIL_0011` follows PORT, CONS, and PERF pilots to test the canonical layout for the LONGTAIL pool. It stresses realistic / structurally complex SQL packaging: CTE pipeline, window ranking, joins, aggregate/order logic, and tie-sensitive ranking behavior.

## Legacy State Snapshot

- pwd: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
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
- diff --name-status:
```text
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
```
- log --oneline -3:
```text
7e438b5d docs: rewrite README for common-core reproducibility
6eefb7c2 docs: rewrite README for common-core reproducibility
c1cc0ff1 artifacts: add common-core reproduction input bundle
```

The legacy repo was read-only. The pre-existing dirty report files were not altered by this task.

## Copied And Generated File Groups

- Byte-for-byte copied legacy files: 33.
- Intentionally adapted files: 7 (six validation scripts plus source SQL whitespace normalization).
- Sanitized Spark plan derivatives: 3.
- Generated metadata/summary files: 19.

Copied groups include SQL, engine DDL, witness load files, notes, public-safe retained controls, hard-negative outputs, PostgreSQL/MySQL JSON plans, and Spark `plan_check.json`. Raw legacy `runs/` was not copied wholesale.

## Long-Tail Structure Boundary

The package records structural long-tail characteristics only. It does not create workload-frequency, production-frequency, timing, speedup, ranking, leaderboard, denominator, or paper-result claims.

Structures present: CTE pipeline, window ranking, joins, aggregate/order logic, and tie-sensitive ranking behavior.

## Hard-Negative Expected Rejection

The maintainer-approved expected rejection reason is `tie_sensitive_ranking_semantics_not_preserved`. `rewrite_neg_01.sql` replaces `DENSE_RANK()` with `ROW_NUMBER()`. This breaks tie-sensitive ranking semantics because tied rows no longer share the same rank. `DENSE_RANK()` preserves tied rows at the same rank, while `ROW_NUMBER()` assigns a unique order and can collapse tied worst-score rows.

Evidence paths:

- `checker/expected_rejections.yaml`
- `evidence/hard_negative/hard_negative_summary.json`
- `evidence/retained_controls/*/result_check.json`
- `evidence/hard_negative/*/rewrite_neg_01.tsv`

## Spark Plan Sanitization

Raw legacy Spark plan text contained local temporary path traces. Raw Spark plan text was not copied into public retained evidence. Sanitized public copies were created under `cases/LONGTAIL/LONGTAIL_0011/evidence/retained_plans/spark/`, and original raw paths are mapped in `evidence/runs_retention.yaml` with do-not-delete status.

Sanitized public copies:

- `evidence/retained_plans/spark/source.sanitized.txt`
- `evidence/retained_plans/spark/rewrite_pos_01.sanitized.txt`
- `evidence/retained_plans/spark/rewrite_neg_01.sanitized.txt`

## Validation Script Caveat

Scripts under `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runners must not write to case-local runs/ by default.

## Validator v0.3 Results

- full-case: PASS 1/1
- canonical-case: PASS 1/1
- evidence-pilot regression: PASS 6/6
- full-case regression: PASS 4/4

## Public Hygiene Scan Results

Public hygiene scan under `cases/LONGTAIL/LONGTAIL_0011` passed. No forbidden local path, WSL-local wording, API/prompt/token trace, or raw Spark local path trace remains in the public case package.

## Boundary Statements

- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
- workload-frequency claim created: no
- production-frequency claim created: no
- Common-core 40 migration started: no

## Remaining Risks

- The migrated validation scripts are retained legacy assets, not final public user runners.
- Long-tail structure must continue to be described as structural robustness only, not workload-frequency evidence.
- Raw Spark plan originals remain private/archive-mapped and must not be published without hygiene review.
