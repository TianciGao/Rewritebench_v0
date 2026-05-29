# Identity Guard Pass vs Fail Comparison

This comparison uses only the existing bounded SQLSolver pass artifacts and referenced SQL/schema/manifest files. No verifier command was run for this triage packet.

## Pool Distribution

Identity guard passed pairs:
- `CONS`: 2
- `LONGTAIL`: 1

Identity guard unknown/failed pairs:
- `LONGTAIL`: 1
- `PERF`: 2
- `PORT`: 2

The pass set contains two Calcite CONS rows and one LONGTAIL row. The unknown set contains one LONGTAIL row, both selected PERF rows, and both selected PORT rows.

## Passed Identity Guard Rows

- `CONS_0005` (`CONS`): source_identity=`equivalent`, candidate_identity=`equivalent`; clues: sql_feature:correlated_subquery; rewrite_opportunity:subquery_decorrelation; portability:null_semantics_gap; consistency_focus:anti_join_semantics|null_semantics
- `CONS_0007` (`CONS`): source_identity=`equivalent`, candidate_identity=`equivalent`; clues: sql_feature:correlated_subquery|subquery_in_from; consistency_focus:correlated_exists_semantics|cross_row_department_constraint|predicate_boundary|subquery_semantics
- `LONGTAIL_0012` (`LONGTAIL`): source_identity=`equivalent`, candidate_identity=`equivalent`; clues: window_function; row_number; order_limit; aggregate; sql_feature:aggregation|complex_expression|outer_join|sort_limit|subquery_in_from|window_function; longtail_focus:aggregation|aggregation_input_boundary|complex_expression|optional_vote_enrichment_semantics|outer_join|outer_join_row_preservation|sort_limit|structural_robustness_only|subquery_in_from|window_function

## Unknown Identity Guard Rows

- `LONGTAIL_0011` (`LONGTAIL`): source_identity=`unknown`, candidate_identity=`unknown`; clues: cte; window_function; dense_rank; aggregate; sql_feature:aggregate|cte|join|sort|window_function; rewrite_opportunity:cte_strategy|expression_simplification; longtail_focus:rank_function_substitution|tie_sensitive_ranking
- `PERF_0006` (`PERF`): source_identity=`unknown`, candidate_identity=`equivalent`; clues: leading_line_comments; block_comments; date_literal; cast_date; aggregate; sql_feature:date_time_function|expression_complexity; rewrite_opportunity:materialization_strategy|predicate_pushdown
- `PERF_0007` (`PERF`): source_identity=`unknown`, candidate_identity=`unknown`; clues: leading_line_comments; block_comments; date_literal; interval_literal; cast_date; aggregate; sql_feature:date_time_function; rewrite_opportunity:materialization_strategy|predicate_pushdown
- `PORT_0003` (`PORT`): source_identity=`unknown`, candidate_identity=`unknown`; clues: leading_line_comments; block_comments; quoted_identifiers; nulls_first_last; double_precision; inline_ddl_comment; order_limit; rewrite_opportunity:dialect_adaptation|order_limit_simplification; portability:identifier_quoting|limit_fetch_gap|null_semantics_gap; portability_focus:identifier_quoting|limit_fetch_gap|null_semantics_gap
- `PORT_0005` (`PORT`): source_identity=`unknown`, candidate_identity=`unknown`; clues: leading_line_comments; block_comments; quoted_identifiers; nulls_first_last; timestamp_type; inline_ddl_comment; order_limit; rewrite_opportunity:dialect_adaptation|order_limit_simplification; portability:identifier_quoting|limit_fetch_gap|null_semantics_gap|order_direction_gap; portability_focus:identifier_quoting|limit_fetch_gap|null_semantics_gap|order_direction_gap

## SQL Structures

Passed rows include correlated subqueries (`CONS_0005`, `CONS_0007`) and a large aggregate/window query with `ROW_NUMBER` and `LIMIT` (`LONGTAIL_0012`). Unknown rows include `DENSE_RANK` inside a CTE (`LONGTAIL_0011`), TPC-H date/date-interval forms with leading source comments (`PERF_0006`, `PERF_0007`), and PORT rows with quoted identifiers plus `NULLS FIRST/LAST` ordering (`PORT_0003`, `PORT_0005`).

## Schema Characteristics

Passed CONS schemas are compact Calcite DDLs using integer/decimal/varchar fields. The passed LONGTAIL schema is simple StackOverflow-style integer/text DDL without CTE materialization requirements in the DDL. Unknown PERF schemas use DATE and NUMERIC types. Unknown PORT schemas are draft DDLs; `PORT_0003` includes `DOUBLE PRECISION` with an inline comment and produced SQLSolver parser diagnostics, and `PORT_0005` includes `DROP TABLE` plus `TIMESTAMP`.

## Candidate/Source Differences

The route is SQLGlot no-op, so source/candidate differences are formatting and dialect normalization rather than intended rewrites. `PERF_0006` is especially diagnostic: source identity was `unknown`, but candidate identity was `equivalent`, suggesting an input-format or source-normalization gap rather than semantic complexity. `PERF_0007` remains unknown after candidate normalization, pointing to interval/date arithmetic support. PORT rows preserve quoted identifiers and null ordering, which appear outside stable SQLSolver identity support.

## SQLSolver Output Patterns

All unknown rows returned `UNKNOWN` quickly rather than timing out. `PORT_0003` additionally emitted parser diagnostics around the DDL/input shape. Other unknown rows emitted only generic SQLSolver runtime messages and `UNKNOWN`, so their classification is feature/modeling based rather than a hard parser-error classification.

## Tag and Dialect Correlation

Unknown rows correlate with selected feature/dialect families: `window_function` plus rank semantics for `LONGTAIL_0011`, `date_time_function` for PERF rows, and PORT portability tags `identifier_quoting`, `null_semantics_gap`, and `limit_fetch_gap` for PORT rows. Passing rows show that correlated subqueries and some aggregate/window forms can work, but that does not generalize to DENSE_RANK, date interval arithmetic, or PORT dialect constructs.
