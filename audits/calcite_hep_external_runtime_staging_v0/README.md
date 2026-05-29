# Calcite HEP External Runtime Staging

Task: `calcite_hep_external_runtime_staging_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: external Calcite HEP invocation path staged outside the release repo and wired into the D035 baseline adapter.

The route-specific adapter remains at `baselines/calcite_hep_fail_closed/adapter.py`. It now discovers an external Calcite HEP runtime through environment variables, resolves per-engine DDL from the case/external schema profiles, invokes the external runtime with a bounded command shape, captures candidate SQL only from the declared candidate file, and fails closed for missing runtime, missing schema DDL, command failure, timeout, or empty output.

External runtime staged:

- External Calcite source root: `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/calcite/calcite`
- External staging root: `/home/tianci_gao/.local/share/sqlrb/calcite_hep`
- Command: `/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke`
- Java: OpenJDK 17.0.18
- Gradle wrapper build: `GRADLE_USER_HOME=/home/tianci_gao/.local/share/sqlrb/calcite_hep/gradle_home ./gradlew --no-daemon :core:classes`

Tiny smoke:

- Rows: `CONS_0036`, `CONS_0037`, `PERF_0006`
- Engine: PostgreSQL
- Runtime output root: `/tmp/sqlrb_calcite_hep_external_runtime_staging_v0/`
- Selected rows: 3
- Adapter-invoked rows: 3
- Candidate-generated rows: 3
- Failure buckets: `none`

Boundary:

- Local diagnostic route staging only.
- No full Common-core run.
- No all-120 Track-A run.
- No MySQL/Spark run.
- No verifier pass.
- No official metrics or Semantic Equivalence Rate.
- No top-level `reports/` or `results/` update.
- No retained-evidence promotion.
- No Calcite source/JAR/build output committed.
