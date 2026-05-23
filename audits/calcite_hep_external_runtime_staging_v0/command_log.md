# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 150fa810f113d18d75ec436800085cf491608a05 HEAD
python - <<'PY'  # GitHub Actions API check for user_entry_smoke.yml
...
PY
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
java -version
```

Inspection:

```bash
sed -n '1,260p' baselines/calcite_hep_fail_closed/adapter.py
sed -n '1,260p' tests/user_entry/test_calcite_hep_fail_closed_route.py
sed -n '1,220p' baselines/calcite_hep_fail_closed/README.md
sed -n '1,620p' /home/tianci_gao/code/sql-rewrite-bench/tools/calcite_hep/CalciteHepRewriteSmoke.java
find /home/tianci_gao/.gradle/caches/modules-2/files-2.1 -path '*org.apache.calcite*' -type f
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/calcite/calcite status -sb --untracked-files=no
```

External staging:

```bash
GRADLE_USER_HOME=/home/tianci_gao/.local/share/sqlrb/calcite_hep/gradle_home \
  ./gradlew --no-daemon :core:classes

javac -cp <external Calcite classes and Gradle-cache jars> \
  -d /home/tianci_gao/.local/share/sqlrb/calcite_hep/classes \
  /home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java
```

Manual runtime probe:

```bash
/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke \
  --case-id PERF_0006 \
  --source-sql /home/tianci_gao/code/Rewritebench_v0/cases/PERF/PERF_0006/sql/source.sql \
  --ddl /home/tianci_gao/code/Rewritebench_v0/schemas/tpch_common_core_v0/postgres/ddl.sql \
  --output-sql /tmp/sqlrb_calcite_hep_external_runtime_staging_v0/manual_probe/PERF_0006_candidate.sql \
  --mode real_route_canary
```

Tiny user-entry smoke:

```bash
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke \
SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep \
SQLRB_CALCITE_HEP_JAVA=/usr/bin/java \
SQLRB_CALCITE_HEP_TIMEOUT=30 \
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool all \
  --engines postgres \
  --case-list /tmp/sqlrb_calcite_hep_external_runtime_staging_v0/case_list.txt \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_external_runtime_staging_v0/smoke_output \
  --run-id calcite_hep_external_runtime_smoke \
  --adapter-timeout 40
```

Validation:

```bash
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
pytest tests/user_entry -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py
git diff --check
git status -sb
```
