# Validation Expectations

## Future Validator Rules

- `local_diagnostic.schema_version` must be recognized.
- `local_diagnostic.diagnostic_mode` must be one of `same_engine`, `cross_dialect_reference`, `manual_review_required`, or `unsupported_for_pg_local_diagnostic`.
- For `same_engine`, `source_reference.engine` and `target_candidate.engine` must be explicit and compatible with the selected local diagnostic engine.
- For `same_engine`, `source_reference.query` must exist and be unambiguous.
- For `cross_dialect_reference`, `source_reference.engine`, `source_reference.query`, and `target_candidate.engine` must be explicit.
- For `cross_dialect_reference`, missing source or target backends must produce explicit fail-closed local diagnostic status, not fallback.
- If `target_reference` is declared, its role must be explicit and must not be confused with the source oracle.
- Query paths must exist, be relative paths, and remain inside the case package.
- Engine values must be `postgres`, `mysql`, or `spark`.
- Boundary flags must preserve local-only status and must not mark the metadata as official metric or paper result input.

## Fail-Closed Expectations

The runner or validator must fail closed when:

- required role metadata is missing for a cross-dialect case;
- a declared query path is missing;
- a declared engine is unsupported;
- a required backend is not implemented or not configured;
- `target_reference` is declared without a role;
- metadata attempts to use `pos_01.sql` as a source oracle without explicit policy.

Fail-closed statuses should be local diagnostic statuses in the ledger, not official metrics.

## Denominator and Paper Boundary

Adding `local_diagnostic` metadata must not:

- change Common-core membership;
- change the Common-core v0 40-case count;
- change the Track A same-engine denominator of 120 planned rows;
- update paper results;
- update reports/results;
- promote retained evidence;
- compute official metrics.

## Non-PORT Regression Expectations

Future validation must prove representative non-PORT behavior is unchanged:

- `PERF_0006` remains same-engine default behavior.
- `CONS_0005` remains same-engine default behavior.
- `LONGTAIL_0011` remains same-engine default behavior.
- Cases without explicit cross-dialect metadata continue the existing same-engine user-entry path.
- `case_sets/` membership is not inferred by scanning `cases/`.

## Local Diagnostic Boundary

The metadata supports local diagnostics only. It is not timing, speedup, official metrics, paper reproduction, reports/results migration, retained-evidence promotion, or leaderboard input.
