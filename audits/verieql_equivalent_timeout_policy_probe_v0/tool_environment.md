# Tool Environment

VeriEQL root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

VeriEQL Python:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Environment variables:

```text
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout -f <pairs.jsonl> -t <timeout> -o <output.jsonl>
```

Help probe:

```text
passed; the command printed argparse help for -f/--file, -t/--timeout, and -o/--out_file.
```

No dependencies were installed in this task.
