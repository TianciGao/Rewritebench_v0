# Canonicalization Rules

## SQL line/comment shaping

SQLSolver query input is prepared as exactly one SQL statement per physical line. Leading line comments are stripped before whitespace is collapsed so a `--` comment cannot accidentally comment out the SQL statement after one-line shaping. Block comments are stripped outside literals.

## One-statement-per-line policy

Query input must contain exactly one statement after comment handling. Multi-statement input fails closed with `wrapper_input_format_gap` and is not sent to SQLSolver.

## Semicolon policy

A single terminal semicolon is normalized away for query input. Internal or multiple statement separators are rejected rather than guessed.

## Whitespace policy

Whitespace is collapsed outside single-quoted literals and double-quoted identifiers. String literal contents are preserved.

## Schema comment stripping

Line comments and block comments are stripped from schema DDL outside literals/quoted identifiers. Inline DDL comments do not reach SQLSolver schema input.

## DROP TABLE preamble handling

`DROP TABLE ...` preambles are removed from SQLSolver schema input. They are verifier-input scaffolding, not schema facts needed for equivalence checking.

## Type normalization

The schema layer maps common PostgreSQL type spellings to Calcite-friendlier forms when safe:

- `DOUBLE PRECISION` -> `DOUBLE`
- `TIMESTAMP WITHOUT TIME ZONE` -> `TIMESTAMP`
- `TEXT` -> `VARCHAR`
- `NUMERIC(...)` / `NUMERIC` -> `DECIMAL(...)` / `DECIMAL`

Table names, column names, primary keys, and foreign keys are preserved when present.

## Feature guards

The wrapper reports explicit guard categories for support risks:

- `unsupported_sql_feature`
- `unsupported_postgres_dialect`
- `schema_canonicalization_gap`
- `wrapper_input_format_gap`
- `type_or_function_modeling_gap`
- `query_normalization_gap`
- `unknown_tool_behavior`

Guard categories are metadata and support boundaries. They are not method failures and not SER evidence.

## Unsafe/fail-closed behavior

Unsafe canonicalization, ambiguous statement boundaries, empty SQL after comment handling, unsupported schema statements, and unterminated comments/quotes fail closed before SQLSolver invocation.
