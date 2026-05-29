# Tool Environment

VeriEQL root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

External Python:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Python version:

```text
Python 3.12.3
```

Environment variables used:

```bash
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Help probe:

```bash
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
```

Result:

- Exit code `0`.
- Help text displayed the JSONL batch flags `-f/--file`, `-t/--timeout`, and `-o/--out_file`.

Wrapper detection:

- `tool_available=true`
- `detection_reason=verieql_root_available`
- `invocation_mode=jsonl_batch`
- `tool_version` is the first help line reported by the staged CLI.

No dependencies were installed or changed in this task.
