# Metadata and Runner Status

## Manifest Schema

All 9 Common-core PORT manifests use `local_diagnostic.schema_version: port_target_engine_diagnostic_v0`. Each manifest declares `local_diagnostic.engine_roles` for `postgres`, `mysql`, and fail-closed `spark`.

For supported local diagnostic routes, each selected target-engine role declares:

- `diagnostic_mode`
- `source_reference.role`
- `source_reference.engine`
- `source_reference.query`
- `target_candidate.role`
- `target_candidate.engine`
- optional `target_reference.role`
- optional `target_reference.engine`
- optional `target_reference.query`
- `target_reference.use_for_checker_oracle: false` when a target reference exists
- `checker.comparison`
- local-only boundary flags

## Validator Support

The target-engine-aware metadata is validated by the case-package validation path recorded in `audits/port_target_engine_role_mapping_v0/`. The closeout did not modify validators or manifests.

## Resolver and Runner Consumption

`case_package_resolver.py` resolves `local_diagnostic.engine_roles.<selected-engine>` when the target-engine-aware schema version is present. `user_run.py` records the resolved diagnostic role fields in the local ledger. `engine_execution.py` dispatches only the manifest-resolved source-reference engine and target-candidate engine roles.

If a target engine role is missing or unsupported, the resolver and runner fail closed with local diagnostic status instead of guessing. Spark remains explicitly unsupported/fail-closed.

## Role Inference Boundary

The runner must not infer source, target, or reference roles from filenames, SQL text, or pool name. `pos_01.sql` is not a source oracle. Controlled adapters copy manifest-declared target reference queries only as diagnostic target-candidate controls and do not execute SQL or compute metrics.

## Wrong-Engine Protection

The forward route avoids executing MySQL-like `source.sql` directly in PostgreSQL. The reverse route avoids executing PostgreSQL-like `source.sql` directly in MySQL. Both protections are implemented through manifest-declared target-engine roles.
