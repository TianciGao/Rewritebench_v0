# Value vs Label Examples

The examples below are copied from existing local result artifacts under `runs/user/common_core_sqlglot_noop_mysql_snapshot`. They are local diagnostic artifacts only and are not retained evidence or official metrics.

## PERF_0062

Role class: same-engine non-PORT MySQL row.

Source columns:

```text
avg(ss_ext_sales_price)
avg(ss_ext_wholesale_cost)
avg(ss_quantity)
sum(ss_ext_wholesale_cost)
```

Candidate columns:

```text
AVG(ss_ext_sales_price)
AVG(ss_ext_wholesale_cost)
AVG(ss_quantity)
SUM(ss_ext_wholesale_cost)
```

Source values and candidate values both serialize as:

```text
120.000000 | 80.000000 | 4.0000 | 80.00
```

Classification: label-only mismatch candidate. The observed difference is aggregate function label case, not row values.

## PORT_0004

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source column:

```text
CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` )
```

Candidate column:

```text
CAST(SUM(CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)
```

Source value and candidate value both serialize as:

```text
50
```

Classification: label-only mismatch candidate. The observed difference is expression label whitespace/formatting.

## PORT_0013

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source column:

```text
CAST( SUM( `t2`.`gender` = 'F' ) AS DOUBLE ) * 100 / COUNT( `t2`.`client_id` )
```

Candidate column:

```text
CAST(SUM(`t2`.`gender` = 'F') AS DOUBLE) * 100 / COUNT(`t2`.`client_id`)
```

Source value and candidate value both serialize as:

```text
66.66666666666667
```

Classification: label-only mismatch candidate. The observed difference is expression label whitespace/formatting.

## PORT_0022

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source column:

```text
CAST( COUNT( `t1`.`id` ) AS DOUBLE ) / 12
```

Candidate column:

```text
CAST(COUNT(`t1`.`id`) AS DOUBLE) / 12
```

Source value and candidate value both serialize as:

```text
0.25
```

Classification: label-only mismatch candidate. The observed difference is expression label whitespace/formatting.

## PORT_0024

Role class: same-engine PORT MySQL row in the SQLGlot noop real-adapter surface.

Source column:

```text
CAST( SUM( CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` )
```

Candidate column:

```text
CAST(SUM(CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)
```

Source value and candidate value both serialize as:

```text
50
```

Classification: label-only mismatch candidate. The observed difference is expression label whitespace/formatting.

## Checker Observation

For all five rows, `mismatch_summary.json` reports one source row and one candidate row. The cross-dialect normalization block is inactive:

```text
cross_dialect_normalization_active: false
positional_column_comparison_used: false
mixed_numeric_equivalence_enabled: false
```

The same-engine checker path therefore compares full JSON row objects, including labels. The value arrays match positionally, but the object keys differ.
