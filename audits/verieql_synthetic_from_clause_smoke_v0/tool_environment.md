# Tool Environment

VeriEQL root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

VeriEQL Python:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Command used by the wrapper:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout -f <pairs.jsonl> -t 30 -o <output.jsonl>
```

Environment variables used:

```text
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Help probe:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout --help
```

Result:

```text
passed; the command printed argparse help for -f/--file, -t/--timeout, and -o/--out_file.
```

No dependencies were installed during this task.
