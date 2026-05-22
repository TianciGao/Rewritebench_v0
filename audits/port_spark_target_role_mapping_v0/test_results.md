# Test Results

Environment check:
- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark PySpark import: available.
- `PYSPARK_PYTHON`: set.
- `SQLRB_SPARK_MASTER`: set.
- Backend status: live local diagnostic backend available through PySpark.

Focused static and unit checks:
- Python compile for modified Python files and new adapter: passed.
- YAML parse for 9 Common-core PORT manifests: passed 9/9.
- Focused adapter/metadata tests: passed, 14 tests and 12 subtests.
- `PYTHONPATH=src pytest tests/user_entry -q`: passed, 125 passed, 1 skipped, 12 subtests passed.
- Case-package v2 reference validator over 40 Common-core case paths: passed 40/40 after rerunning with case paths rather than case IDs.

Live local diagnostics:
- Controlled Spark target diagnostic: completed with failures, selected/source/candidate/checker/exact/mismatch rows `4/4/4/4/2/2`.
- Spark unsupported role check: passed fail-closed behavior, selected/source/candidate/checker rows `5/0/0/0`.
- PostgreSQL PORT route preservation: passed exact `5/5`.
- MySQL PORT route preservation: passed exact `4/4`.
- Non-PORT Spark two-case regression: passed exact `2/2`.

Boundary:
- No official metrics were computed.
- No timing or speedup was computed.
- No reports/results were updated.
- No global leaderboard was created.
