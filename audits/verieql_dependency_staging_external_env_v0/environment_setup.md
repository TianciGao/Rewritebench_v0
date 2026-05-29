# Environment Setup

External venv path:

```text
/home/tianci_gao/.venvs/sqlrb-verieql
```

VeriEQL source root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Commands used:

```bash
python3 -m venv /home/tianci_gao/.venvs/sqlrb-verieql
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python --version
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m pip install --upgrade pip
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m pip install -r /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt
```

Result:

- Venv created or reused outside the release repo.
- Python version: `Python 3.12.3`.
- Pip upgraded from `24.0` to `26.1.1`.
- VeriEQL requirements installed into the external venv.
- No packages were installed into system Python.
- No venv was created inside `/home/tianci_gao/code/Rewritebench_v0`.

Installed requirement families included:

- `z3-solver`
- `mo-sql-parsing==8.205.22260`
- `ujson`
- `ordered-set`
- `lark`
- `tqdm`
- `pandas`
- `pyyaml`
- `prettytable`
- `mysql-connector-python`
- `matplotlib`
- `sphinx`
- `sphinx-rtd-theme`

No real SQL pair verification was run.
