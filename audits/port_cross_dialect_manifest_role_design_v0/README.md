# P1 PORT Cross-Dialect Manifest Role Design

## Verdict

`ready_for_manifest_metadata_patch`

P1 reviewed all 9 Common-core PORT cases and designed an additive manifest metadata shape for local diagnostic execution roles. No manifests, SQL files, runner code, engine backends, reports, results, denominators, case membership, or raw legacy evidence were changed.

## PORT Classification Summary

- `same_engine_compatible`: 4 cases (`PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`)
- `cross_dialect_reference_required`: 5 cases (`PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`)
- `engine_specific_source_variant_required`: 0 cases
- `manual_review_required`: 0 primary classifications
- `unsupported_for_pg_local_diagnostic`: 0 cases

`PORT_0003` needs careful metadata review during P2 because its manifest does not currently declare `source_dialect`, even though `sql/source.sql` is observed to be PostgreSQL-compatible in the local diagnostic path. Several same-engine-compatible PORT cases also have `pos_01.sql` files that are not safe PostgreSQL source-oracle substitutes; the schema therefore makes target references explicit and optional.

## Design Summary

The proposed manifest block is `local_diagnostic`, scoped to local diagnostics only. It separates:

- `diagnostic_mode`
- `source_reference`
- `target_candidate`
- optional `target_reference`
- `checker.comparison`
- local-only boundary flags

The runner must not infer source, target, or reference roles from file names, SQL text, or pool name alone. `pos_01.sql` must not become a PostgreSQL source oracle unless explicit metadata and policy authorize that role.

## Recommended Next Safe Action

Run P2 as a metadata-only manifest patch task covering all 9 Common-core PORT cases. P2 should add explicit `local_diagnostic` metadata only, prohibit SQL edits and runner changes, and run static validation plus non-PORT regression-protection checks.

MySQL source-side execution remains a later implementation requirement for MySQL-like source-reference cases. Spark remains deferred.

## Boundaries

- Local diagnostic design only.
- No implementation performed.
- No case, manifest, or SQL edits.
- No MySQL/Spark implementation.
- No official metrics.
- No timing/speedup.
- No paper tables.
- No reports/results updates.
- No denominator, paper result, case membership, or raw legacy evidence changes.
- No global leaderboard.
