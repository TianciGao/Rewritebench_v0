# Command Log

Task: `common_core_sqlglot_noop_failure_triage_v0`

Branch: `feature/case-package-v2-external-schema`

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -8
```

Starting state was clean and on `feature/case-package-v2-external-schema`.

## Context Read

Read the required context:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `project_control/DECISION_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `baselines/sqlglot/README.md`
- `audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/`

## Artifact Inspection

Inspected existing local run artifacts only:

- `runs/user/common_core_sqlglot_noop_postgres_snapshot/ledger.csv`
- `runs/user/common_core_sqlglot_noop_postgres_snapshot/failures.csv`
- PostgreSQL failed-row adapter stderr files.
- `runs/user/common_core_sqlglot_noop_mysql_snapshot/ledger.csv`
- `runs/user/common_core_sqlglot_noop_mysql_snapshot/failures.csv`
- MySQL failed-row candidate SQL, candidate error, source/candidate JSONL, and mismatch summaries.
- `runs/user/common_core_sqlglot_noop_spark_snapshot/ledger.csv`
- `runs/user/common_core_sqlglot_noop_spark_snapshot/failures.csv`
- Spark failed-row candidate SQL, candidate error, source/candidate JSONL, and mismatch summaries.

No `user_run` rerun was performed. SQLGlot optimize was not run.

## Evidence Highlights

- PostgreSQL PORT rows failed before candidate generation with SQLGlot parse errors.
- MySQL `PORT_0008` failed candidate execution with invalid single-quoted identifier paths.
- MySQL `PERF_0062`, `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024` had matching positional values but mismatched generated expression labels.
- MySQL `PORT_0003`, `PORT_0005`, and `PORT_0012` had value mismatches caused by literalized identifiers or target SQL semantics.
- Spark `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0082` failed candidate execution after preflight with `Spark diagnostic query must contain exactly one statement`.
- Spark `PORT_0003` and `PORT_0013` failed target candidate execution due target SQL incompatibility.
- Spark `PORT_0004` and `PORT_0005` executed but mismatched values.
- Spark `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025` failed closed as explicit unsupported rows.

## Validation

Validation commands:

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
for path in [
    Path("project_control/MIGRATION_STATUS.md"),
    Path("project_control/MIGRATION_RUN_LOG.md"),
]:
    text = path.read_text(encoding="utf-8")
    assert "common_core_sqlglot_noop_failure_triage_v0" in text
PY

PYTHONPATH=src python - <<'PY'
import csv
from pathlib import Path
base = Path("audits/common_core_sqlglot_noop_failure_triage_v0")
for name in [
    "failure_triage_matrix.csv",
    "per_engine_failure_summary.csv",
    "port_vs_nonport_summary.csv",
]:
    with (base / name).open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        assert rows, name
for name in [
    "README.md",
    "candidate_examples.md",
    "recommendation.md",
    "protected_surface_check.md",
    "command_log.md",
    "boundary_checklist.md",
]:
    text = (base / name).read_text(encoding="utf-8")
    assert text.startswith("#"), name
PY

git diff --check
```

Validation result: passed.
