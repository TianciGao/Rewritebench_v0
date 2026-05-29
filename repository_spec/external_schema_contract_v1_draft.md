# External Schema Contract v1 Draft

Status: draft policy for reusable schema assets on `feature/case-package-v2-external-schema`

This contract defines how case manifests should reference external reusable schema assets. It does not authorize DB execution expansion, case conversion, denominator updates, retained-evidence updates, reports/results updates, metric computation, or leaderboard output.

## Layout

External schemas live under:

```text
schemas/<SCHEMA_ID>/
  schema_profile.yaml
  postgres/
    ddl.sql
    load.sql
  mysql/
    ddl.sql
    load.sql
  spark/
    ddl.sql
    load.sql
```

An engine directory is required only when that engine is supported by the schema package.

## schema_profile.yaml

External `schemas/<SCHEMA_ID>/schema_profile.yaml` expected fields:

- `schema_id`
- `source_family`
- `public_release_status`
- `engines`
- engine-specific `ddl` and `load` paths
- `used_by_cases` or equivalent case-family notes
- `adoption_mode`
- compatibility and cleanup notes

The profile should describe the reusable execution context, not paper results or official metrics.

## Case-local schema/schema_profile.yaml

Clean v2 case packages retain case-local `schema/` only for:

```text
cases/<POOL>/<CASE_ID>/schema/schema_profile.yaml
```

The case-local profile is a case-facing summary and linkage file. It is not executable DDL/load and must not duplicate full per-engine schema scripts.

Required case-local profile fields:

- `schema_id`
- `external_schema_profile`
- `source_family`
- `relevant_tables`
- `columns`
- `column_types`
- `primary_keys`
- `foreign_keys`
- `dialect_differences`
- `engine_support`
- `fixture_notes` when fixture/data caveats are relevant

The case-local profile should link to the external schema profile and, where useful, summarize the external DDL/load paths. The external schema package remains the source for executable database setup files.

## Engine-specific DDL/Load Paths

The canonical path pattern is:

```text
schemas/<SCHEMA_ID>/<engine>/ddl.sql
schemas/<SCHEMA_ID>/<engine>/load.sql
```

Supported engine ids are currently `postgres`, `mysql`, and `spark` for Common-core planning. Adding engines requires separate policy and validator updates.

## schema_ref Manifest Shape

Recommended manifest shape:

```yaml
schema_ref:
  schema_id: tpch_common_core_v0
  profile: schemas/tpch_common_core_v0/schema_profile.yaml
  case_profile: schema/schema_profile.yaml
  engines:
    postgres:
      ddl: schemas/tpch_common_core_v0/postgres/ddl.sql
      load: schemas/tpch_common_core_v0/postgres/load.sql
    mysql:
      ddl: schemas/tpch_common_core_v0/mysql/ddl.sql
      load: schemas/tpch_common_core_v0/mysql/load.sql
    spark:
      ddl: schemas/tpch_common_core_v0/spark/ddl.sql
      load: schemas/tpch_common_core_v0/spark/load.sql
```

`schema_ref` becomes the source of truth for DB/checker schema resolution after runner and validator compatibility is implemented.

## Copy-first Adoption Policy

Initial external schema adoption is copy-first:

- copy schema assets into `schemas/<SCHEMA_ID>/`
- add manifest `schema_ref`
- create or update case-local `schema/schema_profile.yaml`
- keep case-local executable schema files only as compatibility artifacts
- validate static paths
- defer deletion until validator and runner compatibility pass

## Case-local Schema Compatibility Policy

Case-local `schema/` remains in clean v2 only for `schema/schema_profile.yaml`.

Case-local executable files such as `schema/postgres/ddl.sql` or `schema/postgres/load.sql` may remain during branch adoption as compatibility artifacts. They should be marked as compatibility artifacts where practical.

Deletion is not allowed until a separate cleanup task proves:

- no runner path still depends on case-local executable DDL/load
- no validator path still depends on case-local executable DDL/load
- manifest `schema_ref` resolves for all intended engines
- case-local `schema/schema_profile.yaml` resolves to the external schema profile
- retained-evidence and audit mappings remain traceable

## Runner and Validator Compatibility Requirements

Before broad v2 conversion:

- validators must parse `schema_ref`
- validators must parse case-local `schema/schema_profile.yaml`
- validators must verify external DDL/load path existence
- runners must resolve executable schema assets from `schema_ref` and external `schemas/`
- runners must fail closed on missing or unsupported engine schema refs
- compatibility mode must still support v1 case-local executable schema files until cleanup is authorized
- no execution output may be written to `schemas/`

## Boundaries

External schema packages are reusable inputs. They are not user-run output, retained paper results, timing artifacts, reports, or leaderboard data.
