# Future P2 Manifest Patch Prompt

Task title:
P2 add explicit PORT local-diagnostic manifest role metadata

Purpose:
Patch all 9 Common-core PORT manifests with additive `local_diagnostic` metadata according to `audits/port_cross_dialect_manifest_role_design_v0/`.

Scope:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Allowed modifications:

- The 9 listed `cases/PORT/*/manifest.yaml` files only.
- Optional audit packet under `audits/port_cross_dialect_manifest_patch_v0/`.
- `project_control/MIGRATION_STATUS.md`.
- `project_control/MIGRATION_RUN_LOG.md`.

Do not modify:

- SQL files.
- README files.
- schema/checker/validation files.
- source code under `src/`.
- scripts.
- tests, unless a separately approved static metadata validator already exists and only test fixtures are needed.
- `case_sets/`.
- reports/results.
- benchmark_spec.
- retained evidence.
- release tags or branches.

Required behavior:

- Add explicit `local_diagnostic` metadata for all 9 PORT cases.
- Use `diagnostic_mode: same_engine` for PostgreSQL-compatible source-reference cases.
- Use `diagnostic_mode: cross_dialect_reference` for MySQL-like source-reference cases.
- Explicitly declare `source_reference.engine`, `source_reference.query`, `target_candidate.engine`, and `target_candidate.role`.
- Declare `target_reference` only when the role is safe and explicit.
- Do not use `pos_01.sql` as a source oracle.
- Preserve local-only boundary flags.
- Preserve PERF / CONS / LONGTAIL same-engine behavior.
- Do not change Common-core membership or denominators.

Validation:

- `git diff --check`.
- YAML parse checks for all 9 modified manifests.
- Static role-metadata validation according to `field_definition_matrix.csv`.
- Confirm no SQL files changed.
- Confirm no non-PORT cases changed.
- Confirm `case_sets/` unchanged.
- Confirm reports/results unchanged.
- Confirm no official metrics, timing/speedup, paper rendering, retained-evidence promotion, or leaderboard.

Boundaries:

- No runner changes.
- No MySQL/Spark implementation.
- No DB/checker execution required.
- No official metrics.
- No timing/speedup.
- No reports/results updates.
- No global leaderboard.
