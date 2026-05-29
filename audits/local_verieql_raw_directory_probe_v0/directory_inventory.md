# Directory Inventory

## Raw Root

Path:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql
```

Top-level entries:

```text
incoming/
notes/
staged/
```

The raw root does not contain:

- `README.md`
- `requirements.txt`
- `__main__.py`
- `parallel/`
- `benchmarks/`

## Staged Source Root

Path:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Observed source markers:

- `README.md`
- `requirements.txt`
- `__main__.py`
- `parallel/cli_within_timeout.py`
- `parallel/cli_within_bound.py`
- `benchmarks/calcite/`
- `benchmarks/leetcode/`
- `benchmarks/literature/`
- `verifiers/`
- `parsers/`
- `z3py_libs/`
- `Dockerfile`
- `license.md`

Nested Git status:

```text
branch: main...origin/main
commit: 493cbb81000205e33b0623cfd1c39106fa035fae
remote: https://github.com/VeriEQL/VeriEQL.git
pre-existing local modification: constants.py
```

The `constants.py` modification was pre-existing and was not touched by this task.
