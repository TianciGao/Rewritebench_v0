# Tool Environment

VeriEQL root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Python:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Environment variables used:

```bash
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Help probe:

```text
python -m parallel.cli_within_timeout --help
```

Result:

```text
exit code 0
```

Wrapper detection:

```json
{
  "tool_available": true,
  "detection_reason": "verieql_root_available",
  "invocation_mode": "jsonl_batch",
  "tool_version": "usage: cli_within_timeout.py [-h] [-f FILE] [-s BOUND_SIZE] [-t TIMEOUT]"
}
```

No dependencies were installed in this task. No VeriEQL source files were edited.
