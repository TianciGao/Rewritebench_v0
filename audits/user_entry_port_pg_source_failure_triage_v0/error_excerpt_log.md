# Error Excerpt Log

Short excerpts from the targeted local PostgreSQL run. Repository-local paths are redacted to `<repo>`.

## PORT_0004

```text
psql:<repo>/runs/user/port_pg_source_failure_triage/workspaces/PORT_0004/postgres/execution/source_query.sql:8:
ERROR: syntax error near "="
LINE 1: SELECT CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) ...
```

## PORT_0013

```text
psql:<repo>/runs/user/port_pg_source_failure_triage/workspaces/PORT_0013/postgres/execution/source_query.sql:4:
ERROR: syntax error near "."
LINE 1: SELECT CAST( SUM( `t2`.`gender` = 'F' ) AS DOUBLE ) * 100 / ...
```

## PORT_0022

```text
psql:<repo>/runs/user/port_pg_source_failure_triage/workspaces/PORT_0022/postgres/execution/source_query.sql:4:
ERROR: syntax error near "."
LINE 1: SELECT CAST( COUNT( `t1`.`id` ) AS DOUBLE ) / 12 FROM `postl...
```

## PORT_0024

```text
psql:<repo>/runs/user/port_pg_source_failure_triage/workspaces/PORT_0024/postgres/execution/source_query.sql:4:
ERROR: syntax error near "="
LINE 1: SELECT CAST( SUM( CASE WHEN `istextless` = 0 AND `isstoryspo...
```

## PORT_0025

```text
psql:<repo>/runs/user/port_pg_source_failure_triage/workspaces/PORT_0025/postgres/execution/source_query.sql:4:
ERROR: syntax error near "."
LINE 1: SELECT `t1`.`account_id` FROM `loan` AS `t1` INNER JOIN `acc...
```
