# CONS Hard-Negative Review Dossiers

## CONS_0007

Source SQL: `cases/CONS/CONS_0007/source.sql`  
Positive SQL: `cases/CONS/CONS_0007/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0007/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark outputs return Theodore rows from departments 10 and 30 for source and positive.

Hard-negative semantic difference: Negative drops the required different-department predicate (`deptno <> e1.deptno`) from the correlated EXISTS condition, so any same-commission row can qualify.

Retained witness/result evidence: Retained negative outputs add Bill and Eric because the different-department guard was removed. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `correlated_exists_predicate_boundary_changed`. Semantic risk types: `correlated_subquery_semantics_changed;predicate_boundary_changed;exists_semantics`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0007 as an intentional hard negative: rewrite_neg_01 removes the correlated different-department predicate, changing EXISTS semantics from same commission in another department to any same-commission row; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0009

Source SQL: `cases/CONS/CONS_0009/source.sql`  
Positive SQL: `cases/CONS/CONS_0009/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0009/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain row `1 1`.

Hard-negative semantic difference: Negative preaggregates the second UNION ALL input by `t2a` and joins it to `t0a`, while source/positive use `t2b = t0b`; this changes the correlated input to SUM.

Retained witness/result evidence: Retained negative outputs contain rows `1 1` and `2 0`, adding a row because the second correlated key is wrong. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `correlated_union_all_join_key_changed`. Semantic risk types: `correlated_subquery_semantics_changed;set_operation_semantics_changed;aggregation_input_boundary_changed;predicate_boundary_changed`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0009 as an intentional hard negative: rewrite_neg_01 changes the correlation key for the second UNION ALL aggregate input from `t2b = t0b` to `t2a = t0a`, changing the scalar SUM predicate; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0010

Source SQL: `cases/CONS/CONS_0010/source.sql`  
Positive SQL: `cases/CONS/CONS_0010/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0010/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain CAROL and DAVE.

Hard-negative semantic difference: Negative removes `e2.empno <> e1.empno`, so the current employee row can satisfy the duplicate-salary EXISTS guard.

Retained witness/result evidence: Retained negative output keeps only DAVE, dropping CAROL because self-matching changes the NOT EXISTS guard. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `self_row_exclusion_removed`. Semantic risk types: `correlated_subquery_semantics_changed;duplicate_multiplicity_changed;predicate_boundary_changed;anti_join_semantics`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0010 as an intentional hard negative: rewrite_neg_01 removes the self-row exclusion from the duplicate-salary correlated EXISTS condition, changing the NOT EXISTS/anti-join semantics; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0011

Source SQL: `cases/CONS/CONS_0011/source.sql`  
Positive SQL: `cases/CONS/CONS_0011/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0011/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain ALICE and BOB.

Hard-negative semantic difference: Negative changes the LEFT JOIN plus `b.ename IS NULL` existence condition into an INNER JOIN count of matching bonus rows.

Retained witness/result evidence: Retained negative output contains only ALICE, losing the row that depends on null-preserving outer join behavior. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `outer_join_null_preservation_changed`. Semantic risk types: `outer_join_null_preservation_changed;null_semantics_not_preserved;correlated_subquery_semantics_changed`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0011 as an intentional hard negative: rewrite_neg_01 replaces the null-preserving LEFT JOIN/IS NULL existence test with an INNER JOIN match test, changing outer-join NULL semantics; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0012

Source SQL: `cases/CONS/CONS_0012/source.sql`  
Positive SQL: `cases/CONS/CONS_0012/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0012/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain departments 10 and 30.

Hard-negative semantic difference: Source EXISTS with `LIMIT 1 OFFSET 2` requires at least three matching employee rows; negative lowers the grouped threshold from `COUNT(*) >= 3` to `COUNT(*) >= 2`.

Retained witness/result evidence: Retained negative output additionally includes department 20 because the threshold is lowered. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `limit_offset_threshold_changed`. Semantic risk types: `order_limit_boundary_changed;aggregation_grouping_changed;predicate_boundary_changed;correlated_subquery_semantics_changed`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0012 as an intentional hard negative: rewrite_neg_01 lowers the LIMIT/OFFSET-derived existence threshold from at least three matching rows to at least two, changing the order/limit boundary; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0024

Source SQL: `cases/CONS/CONS_0024/source.sql`  
Positive SQL: `cases/CONS/CONS_0024/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0024/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain employee `1`.

Hard-negative semantic difference: Source projects only the preserved left-side employee key from a LEFT JOIN; positive collapses to all employees, while negative changes the join to INNER JOIN with the HAVING filter and can filter employees out.

Retained witness/result evidence: Retained negative outputs are empty because the INNER JOIN/HAVING filter removes the preserved employee row. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `outer_join_row_preservation_changed`. Semantic risk types: `outer_join_null_preservation_changed;aggregation_input_boundary_changed;predicate_boundary_changed`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0024 as an intentional hard negative: rewrite_neg_01 changes a row-preserving LEFT JOIN into an INNER JOIN guarded by the aggregate EXISTS/HAVING condition, so preserved employee rows can be filtered out; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0036

Source SQL: `cases/CONS/CONS_0036/source.sql`  
Positive SQL: `cases/CONS/CONS_0036/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0036/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain `Charlie 2`.

Hard-negative semantic difference: Negative changes the pushed aggregate filter literal from `Charlie` to `Alice`.

Retained witness/result evidence: Retained negative output contains `Alice 1`, proving the grouped predicate target changed. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `group_filter_literal_changed`. Semantic risk types: `predicate_boundary_changed;aggregation_grouping_changed;aggregation_input_boundary_changed`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0036 as an intentional hard negative: rewrite_neg_01 changes the aggregate filter predicate literal from `Charlie` to `Alice`, changing the grouped result; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.

## CONS_0037

Source SQL: `cases/CONS/CONS_0037/source.sql`  
Positive SQL: `cases/CONS/CONS_0037/rewrite_pos_01.sql`  
Negative SQL: `cases/CONS/CONS_0037/rewrite_neg_01.sql`

Source / positive summary: Retained pg/mysql/spark source and positive outputs contain `10 1` and `20 1`.

Hard-negative semantic difference: Negative removes DISTINCT from `COUNT(DISTINCT dept.name)`, so duplicate joined department-name rows change the aggregate.

Retained witness/result evidence: Retained negative output changes department 10 to count 2 while department 20 remains 1. Retained `runs/result_check.json` reports pg/mysql/spark source-positive equality and source-negative difference.

Why checker should reject: `aggregation_distinct_semantics_changed`. Semantic risk types: `duplicate_multiplicity_changed;aggregation_grouping_changed;outer_join_semantics`.

Confidence: high.

Suggested approval wording: Approve neg_01 for CONS_0037 as an intentional hard negative: rewrite_neg_01 removes DISTINCT from the joined-name aggregate, changing duplicate multiplicity under the LEFT JOIN; the checker should reject it.

Manual check before migration: maintainer should confirm the wording above, then future migration can encode it in `checker/expected_rejections.yaml` with `approval_status: maintainer_approved_for_migration`. Also confirm Spark plans are sanitized or archive-mapped and validation scripts are copied only as retained legacy assets.

Migration can proceed after approval: yes_after_approval.
