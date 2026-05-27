# Manual Stage B Sample Review

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

This sample review inspected row metrics and available safe annotation/evidence refs for representative rows. No score changes were made. candidate/source/positive span presence alone is not operation support; source-to-candidate transformation evidence remains required.

## Repair-1 Spark supported row

    - Row: `PERF_0008` / `PERF` / `spark` / `direct_llm_repair_1` / `direct_llm_repair_1_tri_engine_pocr_pilot_v0`.
    - Candidate SHA256: `b8d1397ce8d9e1914497a213501cbf04115e4d969ecac7862c6afc7a45b75ecc`.
    - Row metrics: expected operation atoms `3`, supported `1`, presence-only `0`, insufficient evidence `2`, fail-closed status `none`, annotation status `schema_valid`.
    - Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=direct_llm_repair_1_tri_engine_pocr_pilot_v0; implemented_operation_atoms=['A3']; evidence_refs_head=candidate_sql_span:FROM orders o
JOIN customer c
  ON c.c_custkey = o.o_custkey
JOIN lineitem l
  ON l.l_orderkey = o.o_orderkey, source_sql_span:from
	customer,
	orders,
	lineitem, source_candidate_diff:changed.
    - Review disposition: `stage_b_support_plausible_from_row_metrics`. No score change was made.

## Repair-1 Spark insufficient row

- Row: `PERF_0033` / `PERF` / `spark` / `direct_llm_repair_1` / `direct_llm_repair_1_tri_engine_pocr_pilot_v0`.
- Candidate SHA256: `74ea710ebaf45481ab9f67eadc8faeee3b4066b7ab332815c7c27dedbbea8ef4`.
- Row metrics: expected operation atoms `3`, supported `0`, presence-only `0`, insufficient evidence `3`, fail-closed status `none`, annotation status `schema_valid`.
- Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=direct_llm_repair_1_tri_engine_pocr_pilot_v0; implemented_operation_atoms=[]; evidence_refs_head=none.
- Review disposition: `insufficient_evidence_boundary_plausible`. No score change was made.

## SQLGlot optimize MySQL supported row

- Row: `PERF_0024` / `PERF` / `mysql` / `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_pg40_pocr_diagnostic`.
- Candidate SHA256: `7a4d9114af3623f3b173eff3422e70a667769029b11658a2a3823e382bc5a2c7`.
- Row metrics: expected operation atoms `3`, supported `3`, presence-only `0`, insufficient evidence `0`, fail-closed status `none`, annotation status `schema_valid`.
- Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=sqlglot_optimize_schema_aware_pg40_pocr_diagnostic; implemented_operation_atoms=['A1', 'A2', 'A3']; evidence_refs_head=source_sql_span:from
supplier,
nation, candidate_sql_span:FROM `supplier` AS `supplier` JOIN `nation` AS `nation` ON `nation`.`n_name` = 'BRAZIL' AND `nation`.`n_nationkey` = `supplier`.`s_nationkey`, positive_sql_span:supplier
join nation.
- Review disposition: `stage_b_support_plausible_from_row_metrics`. No score change was made.

## SQLGlot optimize Spark supported row

    - Row: `PERF_0008` / `PERF` / `spark` / `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_pg40_pocr_diagnostic`.
    - Candidate SHA256: `a9a953c85ebdc66f5ebe9ddd5ed8f79a82113bb002134a0d2b4ee4a1334c130a`.
    - Row metrics: expected operation atoms `3`, supported `1`, presence-only `0`, insufficient evidence `2`, fail-closed status `none`, annotation status `schema_valid`.
    - Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=sqlglot_optimize_schema_aware_pg40_pocr_diagnostic; implemented_operation_atoms=['A3']; evidence_refs_head=candidate_sql_span:FROM `customer` AS `customer` JOIN `orders` AS `orders` ON `customer`.`c_custkey` = `orders`.`o_custkey` AND `orders`.`o_orderdate` < CAST('1995-03-27' AS DATE) JOIN `lineitem` AS `lineitem` ON `lineitem`.`l_orderkey` = `orders`.`o_orderkey` AND `lineitem`.`l_shipdate` > CAST('1995-03-27' AS DATE), source_sql_span:from
	customer,
	orders,
	lineitem, positive_sql_span:join (
    select
        o_orderkey,
        o_custkey,
        o_orderdate,
        o_shippriority
    from orders
    where o_orderdate < date '1995-03-27'
) orders_filtered
  on customer_filtered.c_custkey = orders_filtered.o_custkey
join lineitem
  on orders_filtered.o_orderkey = lineitem.l_orderkey.
    - Review disposition: `stage_b_support_plausible_from_row_metrics`. No score change was made.

## SQLGlot optimize no-candidate row

- Row: `CONS_0009` / `CONS` / `postgres` / `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_pg40_pocr_diagnostic`.
- Candidate SHA256: `none`.
- Row metrics: expected operation atoms `3`, supported `0`, presence-only `0`, insufficient evidence `0`, fail-closed status `skipped_no_candidate`, annotation status `candidate_missing`.
- Annotation/evidence inspection: annotation row not found in selected JSONL.
- Review disposition: `no_candidate_boundary`. No score change was made.

## SQLGlot no-op zero-control row

- Row: `PERF_0019` / `PERF` / `mysql` / `sqlglot_noop` / `sqlglot_noop_tri_engine_pocr_sanity_control_v0`.
- Candidate SHA256: `099a3ecc8fd1d77bd86c9aa25b43a2c4e7c5c4832edb756491db80ccff6cf422`.
- Row metrics: expected operation atoms `3`, supported `0`, presence-only `3`, insufficient evidence `0`, fail-closed status `none`, annotation status `schema_valid`.
- Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=sqlglot_noop_tri_engine_pocr_sanity_control_v0; implemented_operation_atoms=['A1', 'A2', 'A3']; evidence_refs_head=source_candidate_diff:changed, positive_sql_span:count(orders.o_orderkey) as c_count, candidate_sql_span:count(o_orderkey).
- Review disposition: `no_op_control_plausible`. No score change was made.

## SQLGlot no-op fail-closed row

- Row: `PERF_0006` / `PERF` / `postgres` / `sqlglot_noop` / `sqlglot_noop_pg40_pocr_sanity_control`.
- Candidate SHA256: `250256397b1969ed1f7080c201b9440b0c917720508edf89497dab51e841562b`.
- Row metrics: expected operation atoms `3`, supported `0`, presence-only `0`, insufficient evidence `0`, fail-closed status `schema_invalid`, annotation status `schema_invalid`.
- Annotation/evidence inspection: annotation_status=malformed_json; nested_route_id=sqlglot_noop_pg40_pocr_sanity_control; implemented_operation_atoms=[]; evidence_refs_head=none.
- Review disposition: `schema_invalid_fail_closed_boundary`. No score change was made.

## Direct original Spark supported row

    - Row: `PERF_0008` / `PERF` / `spark` / `direct_llm_original` / `direct_llm_original_pg40_pocr_diagnostic`.
    - Candidate SHA256: `b8d1397ce8d9e1914497a213501cbf04115e4d969ecac7862c6afc7a45b75ecc`.
    - Row metrics: expected operation atoms `3`, supported `1`, presence-only `0`, insufficient evidence `2`, fail-closed status `none`, annotation status `schema_valid`.
    - Annotation/evidence inspection: annotation_status=schema_valid; nested_route_id=direct_llm_original_pg40_pocr_diagnostic; implemented_operation_atoms=['A3']; evidence_refs_head=candidate_sql_span:FROM orders o
JOIN customer c
  ON c.c_custkey = o.o_custkey
JOIN lineitem l
  ON l.l_orderkey = o.o_orderkey, source_sql_span:from
	customer,
	orders,
	lineitem, positive_sql_span:join (
    select
        o_orderkey,
        o_custkey,
        o_orderdate,
        o_shippriority
    from orders.
    - Review disposition: `stage_b_support_plausible_from_row_metrics`. No score change was made.

## Direct original MySQL fail-closed row

- Row: `PERF_0006` / `PERF` / `mysql` / `direct_llm_original` / `direct_llm_original_pg40_pocr_diagnostic`.
- Candidate SHA256: `4da582fe46ca527d0e901d772dd2c97133950b2750c62ded95dfb33a2c71073b`.
- Row metrics: expected operation atoms `3`, supported `0`, presence-only `0`, insufficient evidence `0`, fail-closed status `schema_invalid`, annotation status `schema_invalid`.
- Annotation/evidence inspection: annotation_status=malformed_json; nested_route_id=direct_llm_original_pg40_pocr_diagnostic; implemented_operation_atoms=[]; evidence_refs_head=none.
- Review disposition: `schema_invalid_fail_closed_boundary`. No score change was made.

## Route mismatch row

  - Row: `CONS_0011` / `CONS` / `mysql` / `direct_llm_repair_1` / `direct_llm_repair_1_tri_engine_pocr_pilot_v0`.
  - Candidate SHA256: `562463408416e4f1188b8b571cb7e1b28150f5796a339531c05a0f3991e55146`.
  - Row metrics: expected operation atoms `2`, supported `0`, presence-only `0`, insufficient evidence `0`, fail-closed status `route_mismatch`, annotation status `schema_invalid`.
  - Annotation/evidence inspection: annotation_status=schema_invalid; nested_route_id=direct_llm_repair_1_tri_pocr_pilot_v0; implemented_operation_atoms=['A1']; evidence_refs_head=candidate_sql_span:WHERE NOT EXISTS (
  SELECT 1
  FROM bonus B
  WHERE D.DNAME = B.ENAME
    AND B.JOB = E1.JOB
), positive_sql_span:SELECT COUNT(*), source_candidate_diff:changed.
  - Review disposition: `identity_boundary_fail_closed`. No score change was made.
