# verieql_ddl_parameterized_type_parser_hardening_v0

Task mode: narrow code hardening.

This packet records the VeriEQL wrapper DDL parser hardening for parameterized SQL types.

Goal:
- Preserve parameterized type strings in generated VeriEQL schema metadata.
- Keep table and column identifiers canonicalized to uppercase.
- Avoid rewriting repository SQL or DDL files.
- Avoid changing finite-bound verdict normalization.

Types covered:
- `VARCHAR(32)`
- `NUMERIC(15,2)`
- `DECIMAL(9,2)`

Result:
- The wrapper now finds CREATE TABLE bodies with balanced-parentheses parsing instead of stopping at the first `)`.
- Column-list splitting still respects nested parentheses.
- Column type extraction preserves complete type strings before column constraints.
- Focused tests pass.
- A `CONS_0037` JSONL schema extraction smoke, with no VeriEQL invocation, preserved `NAME=VARCHAR(32)`.

Boundary:
- No Common-core run.
- No exact-candidate verifier pass.
- No official Semantic Equivalence Rate.
- No official metrics.
- No reports/results update.
- No retained evidence promotion.
- No leaderboard output.

