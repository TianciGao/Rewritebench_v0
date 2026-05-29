# Command Log

Commands used for inspection and validation, with no secrets printed:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,240p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,280p' project_control/MIGRATION_STATUS.md
sed -n '1,320p' project_control/DECISION_LOG.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' docs/README.md
sed -n '1,280p' docs/pocr_diagnostic.md
sed -n '1,280p' docs/candidate_sql_outputs.md
rg -n "annotation_jsonl|annotation JSONL|annotation artifact|safe_annotation_outputs|annotation_manifest" docs src/sql_rewrite_bench/pocr audits/pocr_* -g '*.md' -g '*.py' -g '*.csv'
python - <<'PY'
import csv
from pathlib import Path
for path in [Path('audits/pocr_annotation_jsonl_artifact_contract_v0/annotation_jsonl_schema_contract.csv'), Path('audits/pocr_annotation_jsonl_artifact_contract_v0/annotation_manifest_schema_contract.csv')]:
    with path.open(newline='', encoding='utf-8') as fh:
        rows=list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f'{path} has no rows')
PY
rg -F "output/results/<run_id>/pocr/annotations/" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "annotation JSONL is diagnostic evidence" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "route mismatch must fail closed" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "candidate_sha256 mismatch must fail closed" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "No official POCR is computed" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "No paper-facing metric is promoted" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "No route-level POCR score is emitted" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
rg -F "No global leaderboard is produced" docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0
find docs/pocr_annotation_artifacts.md audits/pocr_annotation_jsonl_artifact_contract_v0 -type f \( -name '*.md' -o -name '*.csv' \) -print0 | xargs -0 -I{} sh -c 'test -s "$1" || exit 1' sh {}
git diff --name-status -- cases '**/skills.md' output reports results runs/user
git diff --check
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
```

Closeout validation commands are recorded in the project-control run log.
