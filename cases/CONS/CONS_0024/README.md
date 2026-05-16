# CONS_0024

`CONS_0024` is a canonical public-release case package for a CONS semantic-guard case. It is designed to test checker strictness and hard-negative rejection. It is not a performance claim.

## Case Design

`sql/source.sql` is the source semantic-guard query. `sql/positives/pos_01.sql` is the trusted positive rewrite or adaptation. `sql/negatives/neg_01.sql` is an intentional hard negative.

The source query preserves left-side employee rows through a LEFT JOIN with an aggregate EXISTS/HAVING condition in the join predicate. The positive rewrite returns the preserved employee rows. The hard negative changes that row-preserving join into an INNER JOIN constrained by the aggregate condition, filtering rows that should remain.

Maintainer-approved expected rejection reason: rewrite_neg_01 changes a LEFT JOIN that preserves left-side employee rows into an INNER JOIN constrained by aggregate EXISTS/HAVING logic. This filters out employee rows that should have been preserved. Therefore neg_01 is an intentional hard negative and should be rejected by the checker.

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
