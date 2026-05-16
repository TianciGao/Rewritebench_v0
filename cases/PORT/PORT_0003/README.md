# PORT_0003

`PORT_0003` is a canonical public-release PORT case package for portability and cross-engine adaptation review. It is packaged for correctness, portability-boundary evidence, hard-negative checking, and plan/failure observability.

## Case Summary

PostgreSQL-oriented source selects the school offering at the largest absolute longitude with NULLS LAST. The positive MySQL adaptation preserves the descending absolute-longitude top-1 ordering with dialect quoting changes. The package records dialect and engine portability risk using retained static evidence; it does not create new cross-engine execution results.

## Case Design

- Source SQL: `sql/source.sql`.
- Positive rewrite/adaptation: `sql/positives/pos_01.sql`.
- Hard negative: `sql/negatives/neg_01.sql`.

The hard negative flips the absolute-longitude ORDER BY direction and can select the wrong top-1 school. The expected rejection reason is `order_limit_direction_changed` and is static-inferred from SQL plus retained result evidence. The approval status is recorded in `checker/expected_rejections.yaml`.

## Portability Boundary

No DB rerun was performed during migration. No new cross-engine execution result, transfer-speed claim, complete nine-case PORT closure claim, ranking claim, or leaderboard claim was created. Any cross-engine interpretation must come only from retained evidence and the paper protocol.

## Public Release Boundary

No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is established. Raw legacy evidence was not modified.

## Evidence Map

Retained evidence is indexed in `evidence/runs_retention.yaml`. Hard-negative expectation metadata is in `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained as do-not-delete originals; they were not copied wholesale.

## Validation Script Caveat

The copied validation scripts are retained legacy validation assets. They are not final public user runners. Future public runners should write outputs outside case-local `runs/` by default.
