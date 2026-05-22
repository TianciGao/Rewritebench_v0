# Row-Order Analysis

## Source Query Order Properties

`cases/CONS/CONS_0011/sql/source.sql` selects `E1.ENAME` from `emp` with an `EXISTS` subquery over `dept LEFT JOIN bonus`. It has no `ORDER BY`.

The Spark workspace copy at `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/source_query.sql` is the same unordered query. Without an explicit `ORDER BY`, SQL result row order is not part of the query contract. Spark is therefore allowed to emit matching rows in either order for this query shape.

## Candidate Query Order Properties

`cases/CONS/CONS_0011/sql/pos_01.sql` also has no `ORDER BY`.

For this no-op diagnostic run, the adapter emitted source-like SQL. The workspace candidate at `runs/user/common_core_spark_noop_db_checker/workspaces/CONS_0011/spark/execution/candidate_query.sql` matches the source query and has no `ORDER BY`.

## Case Documentation and Manifest

The case README describes `CONS_0011` as a semantic consistency and checker-boundary case focused on correlated subquery, outer join, null preservation, and existence-test semantics. It does not state that row order matters.

The manifest lists the semantic risk as outer join semantics, null preservation, and existence-test semantics. It does not declare an order-sensitive result contract.

## Checker Config Order Policy

`checker/compare_config.yaml` declares:

- `oracle_policy: source_as_oracle`
- `result_comparison.mode: semantic_equivalence`

It does not declare exact row order, sorted rows, multiset comparison, or an order-insensitive comparison setting.

`checker/normalization.yaml` contains SQL-text normalization-style settings under `rules`, but it does not contain a top-level `sort_rows: true` setting. The local checker implementation reads only top-level `sort_rows`, `trim_whitespace`, and `normalize_numeric_format` from `normalization.yaml` for result-row normalization. Because `sort_rows` is absent, the checker compares normalized row lists in observed order.

## Artifact Comparison

Source result rows:

```json
{"ENAME": "ALICE"}
{"ENAME": "BOB"}
```

Candidate result rows:

```json
{"ENAME": "BOB"}
{"ENAME": "ALICE"}
```

Observed shape:

- Source row count: 2.
- Candidate row count: 2.
- Column labels equal: yes, `ENAME`.
- Values equal after sorting rows: yes.
- Difference before sorting: row order only.

## Semantic Interpretation

The intended semantic property for `CONS_0011` is order-insensitive result equivalence unless an explicit `ORDER BY` or case-local documentation says otherwise. This case has neither. The mismatch should not be treated as a true semantic mismatch.

The likely root cause is a case-level result-comparison policy gap, surfaced by Spark nondeterministic ordering for an unordered query. A narrow future case-local fix should make the order-insensitive comparison policy explicit and should not change SQL semantics or global official metrics.
