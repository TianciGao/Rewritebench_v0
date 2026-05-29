# Proposed Manifest Schema

## Purpose

The `local_diagnostic` block declares execution roles for local user-entry diagnostics. It is additive metadata only and does not change Common-core membership, denominators, official metrics, paper results, reports/results, or retained evidence.

The key design rule is that execution roles are explicit. The runner must not infer source, target, or reference roles from file names, SQL text, or pool names.

## Canonical YAML Shape

```yaml
local_diagnostic:
  schema_version: port_cross_dialect_diagnostic_v0
  diagnostic_mode: cross_dialect_reference

  source_reference:
    role: source_reference
    engine: mysql
    query: sql/source.sql

  target_candidate:
    role: adapter_output
    engine: postgres

  target_reference:
    role: positive_reference
    engine: postgres
    query: sql/pos_01.sql
    use_for_checker_oracle: false
    use_for_sanity_control: true

  checker:
    comparison: source_reference_result_to_target_candidate_result

  boundary:
    local_diagnostic_only: true
    official_metric_input: false
    paper_result_input: false
    reports_results_update: false
    leaderboard_input: false
```

## Field Semantics

`diagnostic_mode` chooses the local diagnostic execution model:

- `same_engine`: source reference and target candidate execute on the selected engine.
- `cross_dialect_reference`: source reference executes on its declared source engine and target candidate executes on the selected target engine.
- `manual_review_required`: metadata is intentionally not executable until maintainer review resolves roles.
- `unsupported_for_pg_local_diagnostic`: local PostgreSQL diagnostic must fail closed for this case.

`source_reference` defines the query and engine used to produce the source-side reference result artifact.

`target_candidate` defines the adapter-output role and target engine used to execute the candidate SQL.

`target_reference` is optional. When present, it is a trusted target-side positive query or sanity-control artifact. It must not be confused with the source oracle unless a future explicit policy adds such a role.

`checker.comparison` defines which result artifacts are compared by `local_result_checker.py`.

`boundary` records that this metadata is local diagnostic only.

## Same-Engine Compatible PORT Example

```yaml
local_diagnostic:
  schema_version: port_cross_dialect_diagnostic_v0
  diagnostic_mode: same_engine
  source_reference:
    role: source_reference
    engine: postgres
    query: sql/source.sql
  target_candidate:
    role: adapter_output
    engine: postgres
  checker:
    comparison: source_reference_result_to_target_candidate_result
  boundary:
    local_diagnostic_only: true
    official_metric_input: false
    paper_result_input: false
    reports_results_update: false
    leaderboard_input: false
```

If a same-engine case has no PostgreSQL-compatible `pos_01.sql`, the `target_reference` block should be omitted. Omission is safer than silently assigning the wrong role.

## Cross-Dialect MySQL Source to PostgreSQL Target Example

```yaml
local_diagnostic:
  schema_version: port_cross_dialect_diagnostic_v0
  diagnostic_mode: cross_dialect_reference
  source_reference:
    role: source_reference
    engine: mysql
    query: sql/source.sql
  target_candidate:
    role: adapter_output
    engine: postgres
  target_reference:
    role: positive_reference
    engine: postgres
    query: sql/pos_01.sql
    use_for_checker_oracle: false
    use_for_sanity_control: true
  checker:
    comparison: source_reference_result_to_target_candidate_result
  boundary:
    local_diagnostic_only: true
    official_metric_input: false
    paper_result_input: false
    reports_results_update: false
    leaderboard_input: false
```

This mode requires a future MySQL backend to produce source-reference result artifacts. Until that backend exists and is configured, the runner must fail closed.

## Manual Review / Unsupported Example

```yaml
local_diagnostic:
  schema_version: port_cross_dialect_diagnostic_v0
  diagnostic_mode: manual_review_required
  review_reason: source_and_target_roles_not_yet_approved
  boundary:
    local_diagnostic_only: true
    official_metric_input: false
    paper_result_input: false
    reports_results_update: false
    leaderboard_input: false
```

The runner should not execute DB/checker diagnostics for a `manual_review_required` case. It should record an explicit local diagnostic status.

## Explicit Non-Goals

- No official metrics.
- No timing/speedup.
- No paper table rendering.
- No reports/results updates.
- No retained-evidence promotion.
- No case membership or denominator changes.
- No tag score, ranking, or leaderboard.
