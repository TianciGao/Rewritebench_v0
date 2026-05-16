# CONS_0037

`CONS_0037` is a canonical public-release case package for a CONS semantic-guard case. It is designed to test checker strictness and hard-negative rejection. It is not a performance claim.

## Case Design

`sql/source.sql` is the source semantic-guard query. `sql/positives/pos_01.sql` is the trusted positive rewrite or adaptation. `sql/negatives/neg_01.sql` is an intentional hard negative.

The source and positive queries count distinct joined department names under a LEFT JOIN. The hard negative removes DISTINCT, so duplicate joined department-name rows can change the aggregate count.

Maintainer-approved expected rejection reason: rewrite_neg_01 removes DISTINCT from COUNT(DISTINCT dept.name). Under LEFT JOIN, duplicate department-name rows can change the aggregate count. Therefore neg_01 is an intentional hard negative and should be rejected by the checker.

Therefore `neg_01` should be rejected by the checker. The approved expected-rejection record is in `checker/expected_rejections.yaml`.

## Package Scope

- Source SQL is in `sql/source.sql`.
- Positive rewrite SQL is in `sql/positives/pos_01.sql`.
- Hard-negative SQL is in `sql/negatives/neg_01.sql`.
- Engine DDL and witness load files are in `schema/`.
- Checker configuration is in `checker/`.
- Retained public evidence is under `evidence/`.
- Stable metadata is under `metadata/`.
- Human notes are under `notes/`.

## Evidence Boundary

Raw legacy run artifacts remain mapped through `evidence/runs_retention.yaml`. Raw legacy runs are mapped and retained, not deleted. Spark plan text files with local temporary path traces are not published raw; sanitized public copies are under `evidence/retained_plans/spark/`.

## Validation Asset Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not yet final public user runners, and future public runner output must not write to case-local `runs/` by default.

## Claim Boundary

This migration did not run DB engines, did not regenerate evidence, denominator unchanged, paper results unchanged, Common-core membership unchanged, case admission status unchanged, and no global leaderboard is introduced.
