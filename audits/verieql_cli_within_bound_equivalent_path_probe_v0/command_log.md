# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D032|D033|D034|D035" project_control/DECISION_LOG.md
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Preflight result:

- release repo clean and on `feature/case-package-v2-external-schema`
- `HEAD` matched `origin/feature/case-package-v2-external-schema` after fetch
- D032, D033, D034, and D035 present
- required prior VeriEQL audits present
- staged VeriEQL source tree unchanged from prior tasks, with pre-existing `M constants.py`

## Source Inspection

```bash
sed -n '1,220p' README.md
nl -ba parallel/cli_within_bound.py | sed -n '1,240p'
nl -ba parallel/cli_within_timeout.py | sed -n '1,190p'
nl -ba constants.py | sed -n '70,100p'
nl -ba errors.py | sed -n '1,120p'
find benchmarks -maxdepth 2 -type f | sort | head -20
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound --help
```

## Probe Input Creation

Runtime files were created only under:

`/tmp/sqlrb_verieql_cli_within_bound_equivalent_path_probe_v0/`

Two JSONL files were created:

- `pairs.jsonlines`: initial lowercase schema keys, used to expose casing behavior.
- `pairs_upper_schema.jsonlines`: final VeriEQL-compatible uppercase schema keys.

## Probe Commands

Final matrix command shape:

```bash
cd /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python \
  -m parallel.cli_within_bound \
  -f /tmp/sqlrb_verieql_cli_within_bound_equivalent_path_probe_v0/pairs_upper_schema.jsonlines \
  -s <bound> \
  -t 30 \
  -c 1 \
  -o /tmp/sqlrb_verieql_cli_within_bound_equivalent_path_probe_v0/upper_schema_bound_<bound>_timeout_30/output.jsonl
```

Bounds tested:

- 1
- 2
- 3
- 5
- 10

No 120 second rerun was needed because the 30 second matrix produced clean bounded `EQU` and `NEQ`.

## Validation Commands

```bash
find audits/verieql_cli_within_bound_equivalent_path_probe_v0 -name '*.md' -type f -size 0 -print
git diff --check
git status -sb
git status --short --untracked-files=all
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
