# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` unless another working directory is shown.

## Preflight And Required Reads

```bash
git status -sb
rg -n '^## D034|^## D035' project_control/DECISION_LOG.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -f src/sql_rewrite_bench/verifier_support/sqlsolver.py
PYTHONPATH=src python -m cli.main user --help
sed -n '1,240p' project_control/MIGRATION_MASTER_PLAN.md
tail -200 project_control/MIGRATION_STATUS.md
tail -200 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1070p' project_control/DECISION_LOG.md
sed -n '1,220p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,220p' repository_spec/user_output_contract_v0_draft.md
sed -n '1,220p' audits/verifier_support_fail_closed_closeout_v0/README.md
sed -n '1,220p' audits/user_verify_facade_fail_closed_v0/README.md
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/sqlsolver.py
```

## Legacy Repo Inventory

Working directory: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`

```bash
pwd
git status -sb
git branch --show-current
git remote -v
git rev-parse HEAD
git rev-parse origin/artifact/case-package-contract-alignment-clean
git ls-files | rg -i 'verieql|sqlsolver|verifier|equiv|equivalence|solver'
find . -maxdepth 5 \( -iname '*verieql*' -o -iname '*sqlsolver*' -o -iname '*verifier*' -o -iname '*equiv*' \) -print | sort
find . -maxdepth 6 \( -iname '*.jar' -o -iname '*.sh' -o -iname '*.py' \) -print | rg -i 'solver|veri|eql|equiv'
rg -l -i 'VeriEQL|SQLSolver|semantic equivalence|equivalence verifier|sqlsolver\.jar' --glob '!.git/**' . | head -100
find . -iname '*.jar' -print | sort
find . -maxdepth 6 -type d -print | rg -i 'verieql|sqlsolver|solver|veri|eql|equiv' | sort
rg --files docs/_scratch | rg -i 'SQLSOLVER|VERIEQL|VERIFIER|SUPPORT|EQUIV' | sort
stat -c '%A,%s,%n' reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/verify_rbot_smoke_venv.sh
file reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/verify_rbot_smoke_venv.sh
sed -n '1,180p' reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/run_manual_r_bot_formal_runtime_verify.py
sed -n '1,180p' reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/verify_rbot_smoke_venv.sh
head -40 reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
head -40 reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/verifier_support_artifact_audit_v1.csv
rg -n -i 'sqlsolver|jar|java|z3|docker|github|clone|manual|available|unavailable|command|path|JAVA_HOME|LD_LIBRARY_PATH|conda|venv|prebuilt|artifact|external|install|run' docs/_scratch/SQLSOLVER_*.md docs/_scratch/PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1.md docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md
rg -n -i 'verieql|jar|java|z3|docker|github|clone|manual|available|unavailable|command|path|JAVA_HOME|LD_LIBRARY_PATH|conda|venv|prebuilt|artifact|external|install|run|constraint' docs/_scratch/VERIEQL_*.md docs/_scratch/PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1.md docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md
find . -type f \( -iname '*verieql*' -o -iname '*sqlsolver*' -o -iname '*solver*' -o -iname '*eql*' -o -iname '*equiv*' \) -printf '%M,%s,%p\n' | sort
find . -type f -perm /111 -printf '%M,%s,%p\n' | rg -i 'verieql|sqlsolver|solver|eql|equiv|verifier' | sort
test -d datasets/raw/verieql/staged/VeriEQL && find datasets/raw/verieql/staged/VeriEQL -maxdepth 2 -type f -printf '%M,%s,%p\n' | sort | head -80 || echo 'datasets/raw/verieql/staged/VeriEQL not present'
find /home/tianci_gao/code/sql-rewrite-bench-artifact-clean -path '*/.git' -prune -o -type d \( -iname '*VeriEQL*' -o -iname '*SQLSolver*' -o -iname '*sqlsolver*' -o -iname '*verieql*' \) -print | sort
rg --files | rg -i 'sqlsolver_verieql_support_readiness|verieql_support|sqlsolver_support|formal_expansion|verifier_support|semantic_equivalence|equivalence' | sort
sed -n '1,220p' docs/_scratch/SQLSOLVER_PREBUILT_ARTIFACT_DISCOVERY_v1.md
sed -n '1,260p' docs/_scratch/SQLSOLVER_EXTERNAL_SUBSTRATE_ACQUISITION_AUDIT_v1.md
sed -n '1,190p' docs/_scratch/VERIEQL_SUPPORT_BOOTSTRAP_PROBE_v0.md
head -80 cases/CONS/CONS_0003/provenance/verieql_calcite_397_159_raw.json
sed -n '1,120p' cases/CONS/CONS_0003/provenance/verieql_calcite_397_159_notes.txt
head -80 cases/CONS/CONS_0004/provenance/verieql_calcite_397_362_raw.json
sed -n '1,120p' cases/CONS/CONS_0004/provenance/verieql_calcite_397_362_notes.txt
find reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1 -maxdepth 2 -type f -printf '%M,%s,%p\n' | sort
for f in reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/*; do head -20 "$f"; done
find . -type f \( -iname '*.jar' -o -iname '*.zip' -o -iname '*.tar.gz' -o -iname '*.whl' -o -iname 'gradlew' -o -iname '*docker*' \) -printf '%M,%s,%p\n' | sort | rg -i 'verieql|sqlsolver|solver|z3|antlr|gradle|docker|eql' || true
```

## Local Path And GitHub Reference

```bash
command -v verieql || true
command -v VeriEQL || true
command -v sqlsolver || true
command -v SQLSolver || true
env | rg 'VERIEQL|SQLSOLVER|JAVA_HOME|LD_LIBRARY_PATH|Z3' || true
test -d /tmp/rewritebench_sqlsolver_audit/candidate && find /tmp/rewritebench_sqlsolver_audit/candidate -maxdepth 3 -type f \( -iname '*.jar' -o -iname 'gradlew' -o -iname 'README*' \) -printf '%M,%s,%p\n' | sort | head -80 || echo '/tmp/rewritebench_sqlsolver_audit/candidate not present'
test -d /tmp/verieql-probe-venv && find /tmp/verieql-probe-venv -maxdepth 3 -type f -name python -o -name pip | head -20 || echo '/tmp/verieql-probe-venv not present'
git ls-remote https://github.com/TianciGao/sql-rewrite-bench.git refs/heads/artifact/case-package-contract-alignment-clean
```

The GitHub branch page was also opened in the browser tool:

```text
https://github.com/TianciGao/sql-rewrite-bench/tree/artifact/case-package-contract-alignment-clean
```

## Writeback And Validation

```bash
python - <<'PY'
from pathlib import Path
for path in ['project_control/MIGRATION_STATUS.md','project_control/MIGRATION_RUN_LOG.md','project_control/DECISION_LOG.md','project_control/MIGRATION_MASTER_PLAN.md']:
    text = Path(path).read_text(encoding='utf-8')
    assert text.strip(), path
print('project-control readability ok')
PY

python - <<'PY'
from pathlib import Path
for path in Path('audits/legacy_verifier_tool_availability_audit_v0').glob('*.md'):
    text = path.read_text(encoding='utf-8')
    assert text.startswith('#'), path
    assert '\t' not in text, path
print('audit markdown sanity ok')
PY

python - <<'PY'
import csv
from pathlib import Path
for path in Path('audits/legacy_verifier_tool_availability_audit_v0').glob('*.csv'):
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert rows, path
print('audit csv sanity ok')
PY

git diff --check

python - <<'PY'
from pathlib import Path
allowed_prefixes = ('audits/legacy_verifier_tool_availability_audit_v0/',)
allowed_files = {'project_control/MIGRATION_STATUS.md','project_control/MIGRATION_RUN_LOG.md'}
paths = []
import subprocess
out = subprocess.check_output(['git','status','--porcelain'], text=True)
for line in out.splitlines():
    if not line:
        continue
    path = line[3:]
    paths.append(path)
violations = [p for p in paths if p not in allowed_files and not p.startswith(allowed_prefixes)]
if violations:
    raise SystemExit('protected surface violation: ' + ', '.join(violations))
print('protected surface ok:', ', '.join(paths))
PY

git -C /home/tianci_gao/code/sql-rewrite-bench-artifact-clean status -sb
git status --porcelain | rg '^(.. )?(runs/user|output)/' || true
```

Results:

- Project-control readability: passed.
- Audit Markdown sanity: passed.
- Audit CSV sanity: passed.
- `git diff --check`: passed.
- Protected-surface check: passed, only audit packet and project-control files changed.
- Legacy repo status: unchanged from pre-existing dirty state.
- `runs/user/` and `output/` runtime artifacts staged/committed: none.
