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

Expected fields:

- `schema_id`
- `source_family`
- `public_release_status`
- `engines`
- engine-specific `ddl` and `load` paths
- `used_by_cases` or equivalent case-family notes
- `adoption_mode`
- compatibility and cleanup notes

The profile should describe the reusable execution context, not paper results or official metrics.

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
- keep case-local `schema/` as compatibility artifact
- validate static paths
- defer deletion until validator and runner compatibility pass

## Case-local Schema Compatibility Policy

Case-local `schema/` directories may remain during branch adoption. They should be marked as compatibility artifacts where practical.

Deletion is not allowed until a separate cleanup task proves:

- no runner path still depends on case-local schema
- no validator path still depends on case-local schema
- manifest `schema_ref` resolves for all intended engines
- retained-evidence and audit mappings remain traceable

## Runner and Validator Compatibility Requirements

Before broad v2 conversion:

- validators must parse `schema_ref`
- validators must verify external DDL/load path existence
- runners must resolve schema assets from `schema_ref`
- runners must fail closed on missing or unsupported engine schema refs
- compatibility mode must still support v1 case-local schema until cleanup is authorized
- no execution output may be written to `schemas/`

## Boundaries

External schema packages are reusable inputs. They are not user-run output, retained paper results, timing artifacts, reports, or leaderboard data.
