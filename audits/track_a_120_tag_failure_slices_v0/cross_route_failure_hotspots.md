# Cross-Route Failure Hotspots

This packet is diagnostic/support analysis only. It does not rank methods globally, create a leaderboard, compute primary local metrics, compute SER, compute POCR, infer operation atoms, or change paper results.

## Portability-Risk Hotspots

- `direct_llm_original`: literal_predicate_boundary=5, type_coercion=5, identifier_quoting=4, type_semantics_gap=4, date_time_semantics=4, null_semantics_gap=3, date_filter_semantics=3, datetime_semantics_gap=3, join_aggregate_input_boundary=2, aggregate_expression_semantics=2
- `sqlglot_noop`: identifier_quoting=12, literal_predicate_boundary=9, type_semantics_gap=8, type_coercion=8, date_time_semantics=7, date_filter_semantics=6, datetime_semantics_gap=5, limit_fetch_gap=4, null_semantics_gap=4, result_set_semantics=3
- `sqlglot_optimize_schema_aware`: identifier_quoting=13, literal_predicate_boundary=9, type_semantics_gap=9, type_coercion=8, date_time_semantics=7, date_filter_semantics=6, datetime_semantics_gap=6, null_semantics_gap=6, limit_fetch_gap=4, result_set_semantics=3
- `calcite_hep_fail_closed`: identifier_quoting=15, type_semantics_gap=11, date_time_semantics=9, literal_predicate_boundary=8, type_coercion=8, limit_fetch_gap=6, null_semantics_gap=6, date_filter_semantics=6, datetime_semantics_gap=6, result_set_semantics=3

## SQL-Feature Hotspots

- `direct_llm_original`: correlated_subquery=5, expression_complexity=4, outer_join=3, date_time_function=3, aggregate=1, disjunction=1, join=1, range_predicate=1, set_operation=1, aggregation=1
- `sqlglot_noop`: expression_complexity=7, date_time_function=4, aggregate=1, disjunction=1, join=1, range_predicate=1
- `sqlglot_optimize_schema_aware`: correlated_subquery=14, outer_join=13, date_time_function=8, expression_complexity=8, join=6, subquery_in_from=6, cte=5, sort=5, aggregation=5, aggregate=4
- `calcite_hep_fail_closed`: expression_complexity=11, window_function=7, cte=6, date_time_function=6, outer_join=6, join=5, aggregation=5, aggregate=4, sort=4, complex_expression=4

## Rewrite-Opportunity Hotspots

- `direct_llm_original`: dialect_adaptation=10, subquery_decorrelation=3, expression_simplification=3, function_normalization=3, aggregation_rewrite=1
- `sqlglot_noop`: dialect_adaptation=22, expression_simplification=5, order_limit_simplification=4, function_normalization=4
- `sqlglot_optimize_schema_aware`: dialect_adaptation=23, expression_simplification=7, subquery_decorrelation=5, function_normalization=5, predicate_pushdown=5, aggregation_rewrite=4, order_limit_simplification=4, materialization_strategy=2, join_reorder=2, cte_strategy=1
- `calcite_hep_fail_closed`: dialect_adaptation=26, expression_simplification=7, order_limit_simplification=6, function_normalization=6, aggregation_rewrite=4, cte_strategy=3, predicate_pushdown=1

## Plan-Operator Hotspots

- No frontier rows carry this axis in existing tag evidence.

## Workload-Realism Hotspots

- No frontier rows carry this axis in existing tag evidence.

## Engine-Specific Hotspots

- MySQL mismatch frontier tag profile: rewrite_opportunity:dialect_adaptation=21, portability_risk:identifier_quoting=14, portability_risk:type_semantics_gap=11, portability_risk:literal_predicate_boundary=10, sql_feature:expression_complexity=8, rewrite_opportunity:expression_simplification=7, portability_risk:type_coercion=7, portability_risk:date_filter_semantics=6, portability_risk:datetime_semantics_gap=6, portability_risk:null_semantics_gap=5, sql_feature:outer_join=5, sql_feature:aggregate=4
- Spark unsupported/execution frontier tag profile: rewrite_opportunity:dialect_adaptation=28, portability_risk:date_time_semantics=12, portability_risk:type_coercion=12, portability_risk:identifier_quoting=12, sql_feature:expression_complexity=11, portability_risk:literal_predicate_boundary=9, rewrite_opportunity:function_normalization=8, sql_feature:date_time_function=8, portability_risk:type_semantics_gap=8, rewrite_opportunity:expression_simplification=7, portability_risk:datetime_semantics_gap=5, portability_risk:date_filter_semantics=5
- These profiles differ in the existing evidence: MySQL frontier is dominated by mismatch rows, while Spark concentrates unsupported/execution/no-candidate boundary rows.

## Pool-Specific Hotspots

- `PERF`: sql_feature:aggregate=8, sql_feature:disjunction=8, sql_feature:join=8, sql_feature:range_predicate=8, rewrite_opportunity:predicate_pushdown=4, sql_feature:date_time_function=3, rewrite_opportunity:materialization_strategy=2, sql_feature:subquery_in_from=2, rewrite_opportunity:join_reorder=2, portability_risk:type_semantics_gap=2, rewrite_opportunity:aggregation_rewrite=2, rewrite_opportunity:cte_strategy=2
- `CONS`: sql_feature:correlated_subquery=19, sql_feature:outer_join=11, rewrite_opportunity:subquery_decorrelation=8, rewrite_opportunity:aggregation_rewrite=7, portability_risk:null_semantics_gap=5, sql_feature:set_operation=4, sql_feature:subquery_in_from=3, rewrite_opportunity:predicate_pushdown=2
- `PORT`: rewrite_opportunity:dialect_adaptation=81, portability_risk:identifier_quoting=44, portability_risk:literal_predicate_boundary=31, portability_risk:type_semantics_gap=30, portability_risk:type_coercion=29, sql_feature:expression_complexity=28, portability_risk:date_time_semantics=27, portability_risk:date_filter_semantics=21, portability_risk:datetime_semantics_gap=20, rewrite_opportunity:expression_simplification=20, rewrite_opportunity:function_normalization=18, sql_feature:date_time_function=18
- `LONGTAIL`: sql_feature:aggregation=11, sql_feature:outer_join=10, sql_feature:window_function=9, sql_feature:cte=9, sql_feature:sort=9, sql_feature:complex_expression=7, sql_feature:join=5, sql_feature:sort_limit=4, sql_feature:subquery_in_from=4, rewrite_opportunity:cte_strategy=2, rewrite_opportunity:expression_simplification=2, sql_feature:aggregate=2

## Direct LLM Mismatch Tags

- `portability_risk`: null_semantics_gap=3, identifier_quoting=3, literal_predicate_boundary=3, type_semantics_gap=3, date_filter_semantics=2, datetime_semantics_gap=2, type_coercion=2, result_set_semantics=1
- `sql_feature`: correlated_subquery=3, expression_complexity=2, aggregate=1, disjunction=1, join=1, range_predicate=1, outer_join=1, date_time_function=1
- `rewrite_opportunity`: dialect_adaptation=5, subquery_decorrelation=3, expression_simplification=2, aggregation_rewrite=1, function_normalization=1
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## SQLGlot Optimize Execution/Unsupported Frontier Tags

- `portability_risk`: date_time_semantics=4, type_coercion=4, identifier_quoting=3, identifier_case_or_quoting=2, type_semantics_gap=2, literal_predicate_boundary=2, limit_fetch_gap=1, null_semantics_gap=1
- `sql_feature`: correlated_subquery=6, expression_complexity=4, subquery_in_from=3, outer_join=3, date_time_function=3
- `rewrite_opportunity`: dialect_adaptation=8, subquery_decorrelation=3, function_normalization=3, expression_simplification=2, order_limit_simplification=1
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## Calcite HEP Fail-Closed Frontier Tags

- `portability_risk`: identifier_quoting=14, date_time_semantics=9, type_semantics_gap=8, literal_predicate_boundary=7, type_coercion=7, limit_fetch_gap=6, null_semantics_gap=6, date_filter_semantics=6
- `sql_feature`: expression_complexity=8, date_time_function=6, aggregate=1, disjunction=1, join=1, range_predicate=1
- `rewrite_opportunity`: dialect_adaptation=24, order_limit_simplification=6, function_normalization=6, expression_simplification=5
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## SQLGlot No-Op Exact Source-Like Rows

- Exact source-like/source-preserving rows carry: rewrite_opportunity:aggregation_rewrite=6, rewrite_opportunity:predicate_pushdown=3, sql_feature:outer_join=3
