# Manifest Diff Review

## Summary

The diff adds one additive `local_diagnostic` block to each of the 9 Common-core PORT manifests.

Same-engine cases receive:

- `diagnostic_mode: same_engine`
- `source_reference.engine: postgres`
- `source_reference.query: sql/source.sql`
- `target_candidate.engine: postgres`
- `target_candidate.role: adapter_output`
- checker comparison metadata
- local-only boundary flags

Cross-dialect cases receive:

- `diagnostic_mode: cross_dialect_reference`
- `source_reference.engine: mysql`
- `source_reference.query: sql/source.sql`
- `target_candidate.engine: postgres`
- `target_candidate.role: adapter_output`
- `target_reference.role: positive_reference`
- `target_reference.query: sql/pos_01.sql`
- `target_reference.use_for_checker_oracle: false`
- `target_reference.use_for_sanity_control: true`
- checker comparison metadata
- local-only boundary flags

## Confirmed Boundaries

- No SQL files changed.
- No source, runner, script, test, or docs files changed.
- No schema files changed.
- No checker files changed.
- No validation files changed.
- No `case_sets/` files changed.
- No reports/results files changed.
- No denominator scaffolds changed.

## Source Oracle Boundary

`pos_01.sql` is not made a source oracle.

For same-engine cases, `target_reference` is omitted. For cross-dialect cases, `pos_01.sql` is declared only as `positive_reference` with `use_for_checker_oracle: false` and `use_for_sanity_control: true`.

The source-reference oracle remains `source_reference.query`, executed on the declared `source_reference.engine`.
