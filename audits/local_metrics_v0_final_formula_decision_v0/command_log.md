# Command Log

Preflight and context:

```bash
git status -sb
git branch --show-current
git log --oneline -8
rg -n "^## D[0-9]+" project_control/DECISION_LOG.md | tail -12
```

Context read:

```bash
project_control/MIGRATION_MASTER_PLAN.md
project_control/MIGRATION_STATUS.md
project_control/MIGRATION_RUN_LOG.md
project_control/DECISION_LOG.md
project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
repository_spec/timing_artifact_schema_v0_draft.md
audits/latest_paper_metrics_timing_protocol_alignment_v0/
audits/timing_schema_open_questions_resolution_v0/
audits/exact_gated_local_timing_artifact_review_v0/
```

Local paper PDF check:

```bash
find /home/tianci_gao /mnt/data /tmp -maxdepth 4 -iname 'Beyond_Faster_SQL*5*.pdf' -o -iname 'Beyond_Faster_SQL*.pdf'
```

Result: no local PDF was found; this matches the caveat in the latest-paper alignment audit.

Validation:

```bash
python - <<'PY'
from pathlib import Path
for path in [
    Path("project_control/MIGRATION_MASTER_PLAN.md"),
    Path("project_control/MIGRATION_STATUS.md"),
    Path("project_control/MIGRATION_RUN_LOG.md"),
    Path("project_control/DECISION_LOG.md"),
]:
    assert path.read_text(encoding="utf-8").strip(), path
assert "## D033: Local metrics v0 formula and boundary decision" in Path("project_control/DECISION_LOG.md").read_text(encoding="utf-8")
PY
python - <<'PY'
from pathlib import Path
root = Path("audits/local_metrics_v0_final_formula_decision_v0")
for path in root.glob("*.md"):
    assert path.read_text(encoding="utf-8").strip(), path
PY
git diff --check
git diff --name-only
git ls-files --others --exclude-standard
```

Results:

- Project-control readability: passed.
- D033 presence check: passed.
- Audit Markdown sanity: passed.
- `git diff --check`: passed.
- Protected-surface check: passed.
- `runs/user/` committed output check: passed.
