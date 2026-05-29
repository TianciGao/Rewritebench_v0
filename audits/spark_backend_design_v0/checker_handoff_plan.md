# Checker Handoff Plan

## Same-Engine Spark

For `--engine spark` same-engine rows, the Spark backend should execute `sql/source.sql` and the adapter-generated candidate SQL against the same isolated Spark schema. If both executions and JSONL exports succeed, `user_run.py` can call `local_result_checker.py` exactly as it does for PostgreSQL and MySQL:

- `source_result_path`: Spark `source_result.jsonl`
- `candidate_result_path`: Spark `candidate_result.jsonl`
- `checker_dir`: per-row checker workspace
- checker configs: case-local `checker/` files

No checker API change is required if Spark emits the same JSONL object shape.

## Future Cross-Dialect Spark

If a later manifest declares Spark as source-reference or target-candidate, `engine_execution.py` should sequence roles from manifest metadata only. Spark artifacts should carry role-specific paths, for example:

- Spark source-reference -> PostgreSQL/MySQL target-candidate
- PostgreSQL/MySQL source-reference -> Spark target-candidate

The checker should compare the declared source-reference result artifact to the declared target-candidate result artifact. Target reference SQL must not become a checker oracle unless a future policy explicitly changes that; current PORT policy says target references are sanity controls only.

## Normalization Boundary

No Spark-specific checker normalization is authorized by this design. Existing same-engine behavior remains strict except for case-local normalization configs already in use. Existing opt-in cross-dialect normalization remains scoped to manifest-declared cross-dialect local diagnostics and should not be broadened for Spark without a dedicated audit and regression tests.

## Failure Handoff

If Spark source execution, candidate execution, schema setup, or result export fails, do not run the checker. Ledger should record `checker_not_enabled` and `not_exact_due_to_execution_failure` as current PostgreSQL/MySQL paths do.
