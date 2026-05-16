# CONS_0009

`CONS_0009` is a canonical public-release case package for a CONS semantic-guard case. It is designed to test checker strictness and hard-negative rejection. It is not a performance claim.

## Case Design

`sql/source.sql` is the source semantic-guard query. `sql/positives/pos_01.sql` is the trusted positive rewrite or adaptation. `sql/negatives/neg_01.sql` is an intentional hard negative.

The source query compares t0 rows against a correlated scalar SUM over a UNION ALL input. The positive rewrite preaggregates the two correlated inputs with the same keys. The hard negative changes the second correlation key and therefore changes which rows contribute to the SUM.

Maintainer-approved expected rejection reason: rewrite_neg_01 changes the correlation key for the second UNION ALL aggregate input from `t2b = t0b` to `t2a = t0a`. This changes the correlated scalar SUM predicate. Therefore neg_01 is an intentional hard negative and should be rejected by the checker.

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
