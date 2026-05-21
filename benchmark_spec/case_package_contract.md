# Case Package Contract

A case package is the benchmark unit. Public Common-core case packages use a manifest-governed surface rather than relying on directory scanning or README text alone.

Expected package files:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql` when declared for the case
- `schema/schema_profile.yaml`
- `checker/`
- `validation/`
- optional dialect variants under `sql/dialect_variants/` when retained for PORT semantics

The manifest governs source-family, provenance, taxonomy, SQL references, schema references, checker references, validation references, and denominator-eligibility metadata.

The case-local schema profile summarizes schema context. Executable DDL/load assets are resolved through manifest/schema-profile linkage to external schema packages where applicable.

This contract does not introduce new required files beyond the current public case package surface, and it does not authorize case membership changes, denominator changes, reports/results updates, metric computation, paper rendering, or leaderboard output.
