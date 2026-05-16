# CONS_0005

`CONS_0005` is a canonical public-release case package for one CONS semantic-guard case. It tests correlated `NOT IN` with NULL-sensitive semantics and anti-join behavior. The package is designed to check checker strictness and retained witness behavior, not to claim performance.

## Case Design

`sql/source.sql` and `sql/positives/pos_01.sql` are expected to match on the retained witness. `sql/negatives/neg_01.sql` is an intentional hard negative.

The approved hard-negative reason is that `neg_01` does not preserve NULL-sensitive correlated `NOT IN` semantics. On the retained witness:

- source and positive output: empty
- negative output: `1	3`

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

Raw legacy run artifacts remain mapped through `evidence/runs_retention.yaml`. Raw legacy evidence is retained and mapped, not deleted. Spark plan text files with local temporary path traces are not published raw; sanitized public copies are under `evidence/retained_plans/spark/`.

## Validation Asset Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not yet canonical public user runners, and future public runner output must not write to case-local `runs/` by default.

## Claim Boundary

This migration did not run DB engines, did not regenerate evidence, denominator unchanged, paper results unchanged, Common-core membership unchanged, case admission status unchanged, and no global leaderboard is introduced.
