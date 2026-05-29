# Inspected Examples

These examples are summarized from `audits/mysql_label_policy_triage_v0/` and existing local artifacts under `runs/user/common_core_sqlglot_noop_mysql_snapshot`. They are local diagnostic evidence only.

## PERF_0062

Role class: same-engine non-PORT MySQL row.

Source labels:

```text
avg(ss_ext_sales_price)
avg(ss_ext_wholesale_cost)
avg(ss_quantity)
sum(ss_ext_wholesale_cost)
```

Candidate labels:

```text
AVG(ss_ext_sales_price)
AVG(ss_ext_wholesale_cost)
AVG(ss_quantity)
SUM(ss_ext_wholesale_cost)
```

Values on both sides:

```text
120.000000 | 80.000000 | 4.0000 | 80.00
```

Interpretation: same-engine label-only mismatch candidate. Aggregate expression label case differs; positional values match.

## PORT_0004

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source label:

```text
CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` )
```

Candidate label:

```text
CAST(SUM(CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)
```

Value on both sides:

```text
50
```

Interpretation: label-only mismatch candidate. Expression whitespace/formatting differs; value matches.

## PORT_0013

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source label:

```text
CAST( SUM( `t2`.`gender` = 'F' ) AS DOUBLE ) * 100 / COUNT( `t2`.`client_id` )
```

Candidate label:

```text
CAST(SUM(`t2`.`gender` = 'F') AS DOUBLE) * 100 / COUNT(`t2`.`client_id`)
```

Value on both sides:

```text
66.66666666666667
```

Interpretation: label-only mismatch candidate. Expression whitespace/formatting differs; value matches.

## PORT_0022

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source label:

```text
CAST( COUNT( `t1`.`id` ) AS DOUBLE ) / 12
```

Candidate label:

```text
CAST(COUNT(`t1`.`id`) AS DOUBLE) / 12
```

Value on both sides:

```text
0.25
```

Interpretation: label-only mismatch candidate. Expression whitespace/formatting differs; value matches.

## PORT_0024

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source label:

```text
CAST( SUM( CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` )
```

Candidate label:

```text
CAST(SUM(CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)
```

Value on both sides:

```text
50
```

Interpretation: label-only mismatch candidate. Expression whitespace/formatting differs; value matches.

## Shared Shape

All five rows have:

- one source row and one candidate row;
- equal row counts;
- equal column counts;
- matching positional values;
- no observed row-order issue;
- no duplicate/multiplicity issue;
- no observed numeric/string/null normalization issue;
- label differences only.
