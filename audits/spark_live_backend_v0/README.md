# Spark Live Backend v0

Verdict: `implemented_live_backend_environment_blocked`

This task upgraded Spark from an explicit fail-closed skeleton to a PySpark-backed local diagnostic backend. The backend now resolves manifest-declared external Spark schema assets, starts a local PySpark session when PySpark is available, creates an isolated diagnostic database, runs source and candidate SQL, writes JSONL source/candidate result artifacts, and returns artifacts to the existing local checker path.

Live Spark validation was not run because the local Spark environment is not configured: `spark-sql` is not on `PATH`, `SPARK_LOCAL_IP` and `SPARK_HOME` are unset, and `pyspark` is not importable. PostgreSQL and MySQL probes were ok.

The backend remains local diagnostic only. It does not compute official metrics, timing, speedup, paper tables, reports/results updates, retained-evidence promotion, denominator changes, paper result changes, case membership changes, raw legacy evidence changes, or leaderboard output.

Recommended next safe action: configure a local PySpark environment and rerun the two-case Spark live smoke (`PERF_0006`, `CONS_0005`) before considering a bounded Common-core Spark local diagnostic trial.
