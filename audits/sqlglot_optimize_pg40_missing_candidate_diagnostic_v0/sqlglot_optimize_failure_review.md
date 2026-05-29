# SQLGlot Optimize Failure Review

## CONS_0009

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_optimize_failed; sqlglot_optimize_failed: _u_0.c is not <class 'sqlglot.expressions.query.Selectable'>.
- Finding: SQLGlot optimize generation failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

## PORT_0004

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_parse_failed; SQLGlot parse failed: Expected END after CASE. Line 5, Col: 32. -- draft-only / not validated -- source dialect: mysql_like_candidate SELECT CAST( SUM( CASE WHEN `sex` =
- Finding: SQLGlot optimize parse failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

## PORT_0013

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_parse_failed; SQLGlot parse failed: Expecting ). Line 1, Col: 21. SELECT CAST( SUM( `t2`.`gender` = 'F' ) AS DOUBLE ) * 100 / COUNT( `t2`.`client_id` ) FROM `district` AS `t1` INNER JO
- Finding: SQLGlot optimize parse failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

## PORT_0022

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_parse_failed; SQLGlot parse failed: Expecting ). Line 1, Col: 23. SELECT CAST( COUNT( `t1`.`id` ) AS DOUBLE ) / 12 FROM `postlinks` AS `t1` INNER JOIN `posts` AS `t2` ON `t1`.`postid`
- Finding: SQLGlot optimize parse failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

## PORT_0024

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_parse_failed; SQLGlot parse failed: Expected END after CASE. Line 1, Col: 39. SELECT CAST( SUM( CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) AS DOUBLE ) *
- Finding: SQLGlot optimize parse failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

## PORT_0025

- Manifest status: `generation_failed` / `not_generated` / `adapter_failed`.
- Failure detail: adapter_failed; adapter_failed: see per-run log; sqlglot_parse_failed; SQLGlot parse failed: Invalid expression / Unexpected token. Line 1, Col: 11. SELECT `t1`.`account_id` FROM `loan` AS `t1` INNER JOIN `account` AS `t2` ON `t1`.`account_i
- Finding: SQLGlot optimize parse failure recorded during candidate capture; user reproduction also records adapter_failed before candidate SQL was available.
- Previously retained/captured SQLGlot optimize PostgreSQL candidate elsewhere: `no`.
- Safe for PG40 annotation now: `no`.

These failures are expected to remain visible unless a later task explicitly reruns or fixes SQLGlot optimize candidate capture. They are not preflight-blocked rows in the selected PostgreSQL manifest; they are generation/adapter failures.
