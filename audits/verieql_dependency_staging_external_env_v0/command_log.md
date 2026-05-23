# Command Log

## Audit Plan Recorded Before Environment Actions

Plan:

1. Use external venv path `/home/tianci_gao/.venvs/sqlrb-verieql`.
2. Do not create or modify any venv under `/home/tianci_gao/code/Rewritebench_v0`.
3. Do not modify the staged VeriEQL source tree.
4. Install dependencies only into the external venv.
5. Run only non-experiment probes:
   - Python version
   - import probe
   - `python -m parallel.cli_within_timeout --help` from the VeriEQL root
6. Do not run CONS_0007 or any SQL pair verification.
7. Record package versions and source-tree cleanliness after the probes.

## Preflight

```bash
git status -sb
rg -n "## D034|## D035" project_control/DECISION_LOG.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -d audits/verieql_adapter_jsonl_compatibility_v0
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status --porcelain
sed -n '1,200p' /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt
```

Result:

- Release repo was clean.
- D034/D035 present.
- Wrapper and compatibility audit present.
- VeriEQL root present.
- VeriEQL root pre-existing Git status: `main...origin/main` with `M constants.py`.
- Requirements file contains `z3-solver`, `mo-sql-parsing==8.205.22260`, `ujson`, `ordered_set`, `lark`, `tqdm`, `pandas`, `pyyaml`, `prettytable`, `mysql-connector-python`, `matplotlib`, `sphinx`, and `sphinx-rtd-theme`.

Further command results are appended after environment staging.

## Environment Staging

```bash
python3 -m venv /home/tianci_gao/.venvs/sqlrb-verieql
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python --version
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m pip install --upgrade pip
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m pip install -r /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt
```

Result:

- External venv path: `/home/tianci_gao/.venvs/sqlrb-verieql`.
- Python version: `Python 3.12.3`.
- Pip upgraded from `24.0` to `26.1.1`.
- VeriEQL requirements installed successfully into the external venv.

## Non-Experiment Probes

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python --version
```

Result:

```text
Python 3.12.3
```

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -c "import ujson, z3, ordered_set, lark, prettytable, mysql.connector; print('imports ok')"
```

Result:

```text
imports ok
```

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
```

Working directory:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Result:

```text
usage: cli_within_timeout.py [-h] [-f FILE] [-s BOUND_SIZE] [-t TIMEOUT]
                             [-m {train,eval}]
                             [-c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}]
                             [-i {0,1}] [-o OUT_FILE]

VeriEQL cli
```

The full help output is recorded in `help_probe_result.md`.

## Dependency Versions

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m pip freeze
```

Result:

- Recorded in `dependency_versions.txt`.

## Source Tree Cleanliness

```bash
git status -sb
git status --porcelain
```

Working directory:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Result:

```text
## main...origin/main
 M constants.py
```

```text
 M constants.py
```

Interpretation:

- The source tree remained unchanged relative to preflight.
- The `constants.py` modification was pre-existing.
- No real SQL pair verification was run.

## Validation

```bash
tail -30 project_control/MIGRATION_STATUS.md
tail -90 project_control/MIGRATION_RUN_LOG.md
```

Result:

- Project-control readability check passed.
- The new status and run-log entries are readable and appended in chronological context.

```bash
find audits/verieql_dependency_staging_external_env_v0 -maxdepth 1 -type f -print | sort
find audits/verieql_dependency_staging_external_env_v0 -name '*.md' -type f -empty -print
```

Result:

- Audit packet files are present.
- No empty Markdown files were found.

```bash
git diff --check
```

Result:

- Passed with no whitespace errors.

```bash
git status --short -- src tests scripts cases case_sets schemas inventory baselines reports results output benchmarks runs/user
```

Result:

- No protected release-repo surfaces were modified.
- No `runs/user/` or `output/` runtime artifacts were staged.

```bash
git status -sb
```

Result before commit:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
 M project_control/MIGRATION_RUN_LOG.md
 M project_control/MIGRATION_STATUS.md
?? audits/verieql_dependency_staging_external_env_v0/
```

This is the expected audit/project-control-only change set before commit.
