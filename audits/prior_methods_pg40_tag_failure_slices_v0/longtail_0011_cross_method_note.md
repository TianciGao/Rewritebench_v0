# LONGTAIL_0011 Cross-Method Note

`LONGTAIL_0011` appears as a repeated PG40 candidate-execution boundary across the three prior-method diagnostics.

## Method Status

- `learnedrewrite`: `candidate_execution_failed`; generated=true; executable=false; exact=false.
- `rbot_gpt54_adapted`: `candidate_execution_failed`; generated=true; executable=false; exact=false.
- `llm_r2_gpt54_adapted`: `candidate_execution_failed`; generated=true; executable=false; exact=false.

## Tag Profile

sql_feature=aggregate; sql_feature=cte; sql_feature=join; sql_feature=sort; sql_feature=window_function; rewrite_opportunity=cte_strategy; rewrite_opportunity=expression_simplification

## Likely Diagnostic Boundary

The retained taxonomy tags indicate CTE, window function, join, aggregate, sort, expression simplification, and CTE strategy complexity. The repeated candidate-execution failure suggests a generated-SQL execution/runtime boundary on this long-tail shape. This is a diagnostic clue only; no verifier or official semantic-equivalence evidence was produced.

## Boundary

This note is not a method ranking conclusion. It does not mean one method is globally better than another, and it does not authorize Track A 120 expansion.
