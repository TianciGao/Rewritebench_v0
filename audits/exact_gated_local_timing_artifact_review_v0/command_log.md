# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -8
git merge-base --is-ancestor 858511a9723f8648af4acea493f458e353bf0a92 HEAD
rg -n "exact_gated_local_timing_diagnostic_v0|858511a|Commit hash:|Push result:" project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md
```

Context reads included:

```bash
project_control/MIGRATION_MASTER_PLAN.md
project_control/MIGRATION_STATUS.md
project_control/MIGRATION_RUN_LOG.md
project_control/DECISION_LOG.md
project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
repository_spec/timing_artifact_schema_v0_draft.md
docs/user_entry_checker_policy.md
audits/timing_artifact_schema_design_v0/
audits/timing_schema_open_questions_resolution_v0/
audits/exact_gated_local_timing_diagnostic_v0/
```

Artifact inspection:

```bash
python - <<'PY'
import json
from pathlib import Path
runs = {
    "postgres": Path("runs/user/timing_sqlglot_noop_postgres_smoke"),
    "mysql": Path("runs/user/timing_sqlglot_noop_mysql_smoke"),
    "spark": Path("runs/user/timing_sqlglot_noop_spark_smoke"),
}
required = [
    "route_id", "method_id", "case_id", "pool", "engine", "denominator_id",
    "candidate_id", "local_run_id", "timing_policy_id", "exact_status",
    "failure_bucket", "timing_eligible", "timing_status", "timing_na_reason",
    "source_runtime_samples_ms", "candidate_runtime_samples_ms",
    "source_median_ms", "candidate_median_ms", "speedup_ratio",
    "source_sql_hash", "candidate_sql_hash", "local_diagnostic_only",
    "official_metric_input", "paper_result_input", "retained_evidence_promoted",
    "leaderboard_input",
]
for engine, root in runs.items():
    timing = root / "timing"
    for rel in ["timing_policy.json", "environment_metadata.json", "timing_summary.json"]:
        assert (timing / rel).exists()
    for path in sorted((timing / "rows").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert not [key for key in required if key not in data]
        assert data["local_diagnostic_only"] is True
        assert data["official_metric_input"] is False
        assert data["paper_result_input"] is False
        assert data["retained_evidence_promoted"] is False
        assert data["leaderboard_input"] is False
PY
```

Validation:

```bash
python -m json.tool audits/exact_gated_local_timing_diagnostic_v0/timing_status_counts.json
python - <<'PY'
import csv
from pathlib import Path
root = Path("audits/exact_gated_local_timing_artifact_review_v0")
for path in root.glob("*.csv"):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert reader.fieldnames
        assert rows
for path in root.glob("*.md"):
    assert path.read_text(encoding="utf-8").strip()
PY
git diff --check
git diff --name-only
git ls-files --others --exclude-standard
```

No timing rerun was performed.

Validation results:

- Project-control readability: passed.
- Audit Markdown/CSV sanity checks: passed.
- Timing artifact schema review: passed for all three bounded smoke timing directories and all six row artifacts.
- `git diff --check`: passed.
- Protected-surface check: passed.
- `runs/user/` committed output check: passed; no `runs/user/` outputs are tracked, staged, or unignored.
