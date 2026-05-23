# Current Adapter Inventory

Findings:

- No prior Calcite HEP user-entry adapter was present in `src/`.
- Existing Calcite mentions were retained-evidence/status scaffolding references in `docs/dev/`, `repository_spec/`, `scripts/dev/`, and project-control history.
- No top-level `Calcite_support/`, `calcite_support/`, `tools/calcite/`, or `configs/calcite/` folder was found.
- No Calcite binary, JAR, source checkout, Gradle build output, or vendored third-party tree is tracked in the release repo.

Implemented minimal route files:

- `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py`
- `src/sql_rewrite_bench/local_timing.py` route identity recognition for the Calcite adapter command.
- `tests/user_entry/test_calcite_hep_fail_closed_route.py`

This keeps Calcite support inside the existing user-entry adapter boundary rather than creating a new repository-local tool tree.
