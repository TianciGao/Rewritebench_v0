# Case Package Contract v2 Draft

Status: draft policy for `feature/case-package-v2-external-schema`

This contract defines the target v2 case-local package shape. It is a branch-adoption contract, not authorization for bulk conversion, denominator changes, report/result updates, metric computation, retained-evidence deletion, or leaderboard output.

## Required Case-local Files

Each v2 case package should contain:

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/source.sql
  schema/schema_profile.yaml
  checker/
  validation/
```

When positive rewrites or hard negatives exist, use direct SQL files:

```text
sql/pos_01.sql
sql/neg_01.sql
```

Additional numbered files may use the same direct naming pattern, for example `pos_02.sql` or `neg_02.sql`.

## Optional Case-local Files

Optional case-local assets include:

- lightweight `witness/` policy metadata
- compatibility case-local `schema/<engine>/ddl.sql` and `schema/<engine>/load.sql` copies during branch adoption
- `notes/` for stable package caveats
- case-local `runs/` as optional compatibility only after content classification

## Default-excluded Files

The v2 case package does not require:

- case-local executable `schema/<engine>/ddl.sql`
- case-local executable `schema/<engine>/load.sql`
- case-local `data/data_profile.yaml`
- case-local `witness/correct_result.csv`
- heavy case-local `evidence/` payloads
- top-level static `evidence/cases/<POOL>/<CASE_ID>/` packages as a required final public surface
- local user-run outputs
- generated DB results, checker logs, timing output, or scratch workspaces

These assets should be regenerated through validation/checker/baseline/report scripts or kept only as explicitly authorized compatibility/retained artifacts.

## Manifest Roles

`manifest.yaml` is the source of truth for:

- case identity and pool
- direct SQL path references
- case-local `schema/schema_profile.yaml` references
- checker config path references
- validation entrypoint references
- `schema_ref`
- `evidence_policy`
- optional retained-artifact `evidence_ref` compatibility metadata
- witness mode
- compatibility notes

Manifest references do not change Common-core membership, denominators, paper results, reports/results, metric authorization, or leaderboard policy.

## SQL Path Convention

The target convention is:

```yaml
sql:
  source: sql/source.sql
  positives:
    - sql/pos_01.sql
  negatives:
    - sql/neg_01.sql
```

During branch adoption, manifests may include `legacy_compatibility_path` values for the v1 nested paths.

## Checker Path Convention

Checker configuration remains case-local by default:

```text
checker/checker.yaml
checker/normalization.yaml
checker/compare_config.yaml
checker/expected_rejections.yaml
```

The checker config may refer to direct v2 SQL paths. Any compatibility fallback must be explicit and temporary.

Clean v2 `checker/` contains configuration only. It must not contain duplicated Python checker implementations. Shared result comparison is provided by `src/sql_rewrite_bench/local_result_checker.py`; future shared SQL-shape and plan/evidence checks should live in `src/sql_rewrite_bench/sql_shape_validator.py` and `src/sql_rewrite_bench/plan_artifact_validator.py`.

## Schema Path Convention

Clean v2 keeps case-local `schema/` only for:

```text
schema/schema_profile.yaml
```

The profile is a case-facing schema summary, not executable DDL/load. It should record:

- `schema_id`
- `external_schema_profile`
- `source_family`
- relevant tables
- columns and types
- primary keys
- foreign keys
- dialect differences
- fixture/data notes when needed
- engine support summary

Executable DDL/load remains external under:

```text
schemas/<SCHEMA_ID>/<engine>/ddl.sql
schemas/<SCHEMA_ID>/<engine>/load.sql
```

Case-local per-engine schema files may remain only as branch-adoption compatibility artifacts until cleanup is explicitly authorized.

## Evidence Policy Convention

Clean v2 does not require case-local `evidence/` or top-level `evidence/cases/<POOL>/<CASE_ID>/` static packages. Benchmark evidence should be regenerated through validation, checker configuration, baselines, scripts, reports, and results only when those reporting surfaces are separately authorized.

The clean v2 manifest convention is:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

If static artifacts are deliberately retained during migration or for separately authorized paper/reporting review, use:

```yaml
evidence_policy:
  static_case_evidence: optional_retained
  retained_static_artifacts:
    - path: evidence/cases/<POOL>/<CASE_ID>/...
      role: retained_reference
```

`evidence_ref` is optional compatibility metadata. Its absence must not fail clean v2 static validation when `evidence_policy` records that static case evidence is not required.

## Validation Path Convention

The target validation entrypoints are:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
validation/run_engine_queries.py
```

Case-local validation scripts should be thin entrypoints. The shell wrappers call the local `run_engine_queries.py` shim, and the shim delegates to shared modules under `src/sql_rewrite_bench/validation/`.

Clean v2 `validation/` contains thin case-local entrypoints only. It must not duplicate shared engine-query, result-checking, SQL-shape, or plan-artifact implementation logic in every case. The local `run_engine_queries.py` must not contain hardcoded case IDs, credentials, DB execution code, case-local `runs/` writes, reports/results writes, metric computation, or leaderboard creation.

## Folder-ordered Conversion Sequence

Future writable conversion should proceed by folder/asset layer:

`manifest -> sql -> schema -> checker -> validation -> witness -> evidence -> metadata -> notes -> runs -> README/validator`

This sequence prevents spreading mixed v1/v2 structures across additional cases. Each layer should pass its static validation gate before the next layer is converted.

## Witness Policy

Runtime user-run checking defaults to source-as-oracle comparison: execute source SQL and candidate SQL in the same local context, then compare their results.

`data_profile.yaml` and `correct_result.csv` are optional. They may be generated, externalized, or retained under evidence when useful, but they are not required for local runtime checking when source-as-oracle execution is available.

## Case-local Runs Policy

Case-local `runs/` is not automatically retained evidence in v2. It must be classified by observed contents:

- absent `runs/`: no cleanup needed
- empty `runs/`: not retained evidence
- placeholder-only `runs/`: not retained evidence unless the placeholder explicitly documents retained artifacts stored in that directory
- retained-evidence-present `runs/`: retention mapping required before deletion
- sensitive/private/local-path/raw-trace `runs/`: private/archive mapping required; do not public-copy
- manual-review `runs/`: deletion forbidden until reviewed

Case-local `runs/` must not be used for new user-run outputs. New user-run outputs stay under top-level `runs/user/<run_id>/`.

D005 protection remains in force for non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace `runs/` directories. Those directories must not be deleted, rewritten, or moved without retention/archive mapping and explicit approval.

## No-global-leaderboard Boundary

Case packages do not define leaderboard ranking. Reports must remain denominator-aware and role-aware. v2 conversion does not authorize official metric computation, timing collection, report rendering, paper-result changes, or global leaderboard output.

## v1 Compatibility During Branch Adoption

v1 assets may remain during branch adoption as compatibility artifacts. Compatibility assets should be documented in the manifest, audit outputs, or schema/evidence references. Cleanup is a separate task after validator and runner compatibility pass.
