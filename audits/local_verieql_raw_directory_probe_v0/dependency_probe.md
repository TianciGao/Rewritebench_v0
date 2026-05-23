# Dependency Probe

## requirements.txt

The staged VeriEQL `requirements.txt` contains:

```text
z3-solver
mo-sql-parsing==8.205.22260
ujson
ordered_set
lark
tqdm
pandas
pyyaml
prettytable
mysql-connector-python
matplotlib
sphinx
sphinx-rtd-theme
```

## Active Python Environment

Command:

```bash
which python
```

Result:

```text
/home/tianci_gao/code/sql-rewrite-bench/.venv/bin/python
```

## Import Probe

Read-only import checks found:

```text
ujson: missing
z3: missing
ordered_set: missing
lark: missing
tqdm: ok
pandas: ok
yaml: ok
prettytable: missing
mysql.connector: missing
```

## Interpretation

This source tree requires a Python environment that is not currently satisfied by the active local `.venv`. Installing dependencies was outside this task and was not performed.
