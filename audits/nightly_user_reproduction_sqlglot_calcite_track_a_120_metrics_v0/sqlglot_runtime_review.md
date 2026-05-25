# SQLGlot Runtime Review

SQLGlot availability/version: `30.2.1`

SQLGlot no-op and SQLGlot optimize schema-aware were run through the existing `baselines/sqlglot/sqlglot_user_adapter.py` adapter paths. The no-op route was not silently optimized. The schema-aware optimize route used the explicit `--route optimize_schema_aware` adapter mode and was not downgraded to no-op.

Database/checker/timing execution was limited to these deterministic routes through the user-side pipeline.
