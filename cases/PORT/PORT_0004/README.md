# PORT_0004

`PORT_0004` is a canonical public-release PORT case package for portability and cross-engine adaptation review. It is packaged for correctness, portability-boundary evidence, hard-negative checking, and plan/failure observability.

## Case Summary

MySQL-oriented source computes a female-patient percentage for diagnosis RA in birth year 1980; the PostgreSQL positive preserves the year predicate under dialect adaptation. The package records dialect and engine portability risk using retained static evidence; this migration does not create new cross-engine execution results.

## Case Design

- Source SQL: `sql/source.sql`.
- Positive rewrite/adaptation: `sql/positives/pos_01.sql`.
- Hard negative: `sql/negatives/neg_01.sql`.

The hard negative changes the year literal from 1980 to 1981, changing the filtered patient cohort. The expected rejection reason is `year_filter_literal_changed` and is static-inferred from SQL plus retained result evidence. The approval status is recorded in `checker/expected_rejections.yaml`.

## Portability Boundary

No DB rerun was performed during migration. No new cross-engine execution result, transfer-speed claim, complete nine-case PORT result claim, ranking claim, or leaderboard claim was created. Any cross-engine interpretation must come only from retained evidence and the paper protocol.

## Public Release Boundary

No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is established. Raw legacy evidence was not modified.

## Evidence Map

Retained evidence is indexed in `evidence/runs_retention.yaml`. Hard-negative expectation metadata is in `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained as do-not-delete originals; they were not copied wholesale.

## Validation Script Caveat

The copied validation scripts are retained legacy validation assets. They are not final public user runners. Future public runners should write outputs outside case-local `runs/` by default.
