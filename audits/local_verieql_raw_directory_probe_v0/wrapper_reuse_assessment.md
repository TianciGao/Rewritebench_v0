# Wrapper Reuse Assessment

## Existing Release Wrapper

The current release wrapper in `src/sql_rewrite_bench/verifier_support/verieql.py` detects commands from:

- explicit command argument,
- `SQLRB_VERIEQL_COMMAND`,
- `VERIEQL_COMMAND`,
- `VERIEQL_BIN`,
- PATH names `verieql`, `VeriEQL`, `verieql-cli`, and `veri-eql`.

It does not currently recognize `SQLRB_VERIEQL_CMD` by name.

When a command is available, the wrapper invokes it as:

```text
<command> <source_sql_path> <comparison_sql_path> [--schema <schema_context_path>]
```

## VeriEQL Source CLI Contract

The staged VeriEQL batch CLI expects:

```text
python -m parallel.cli_within_timeout -f <jsonlines> -t <timeout> -o <out_file>
```

from the VeriEQL source root.

It consumes JSONL records containing schema, constraints, and SQL pair fields. It does not consume the wrapper's direct `source.sql comparison.sql --schema` command shape.

## Recommended Future Adapter Shape

Future code should be separately authorized and should:

- add `SQLRB_VERIEQL_ROOT` support,
- optionally add `SQLRB_VERIEQL_CMD` as an alias if that is the team-approved env var,
- generate a temporary VeriEQL JSONL pair file from a verifier pair record,
- run the batch module with `cwd=$SQLRB_VERIEQL_ROOT`,
- pass `-f`, `-t`, `-o`, and likely `-c 1` for bounded canaries,
- parse the output JSONL states into the shared verifier verdict vocabulary,
- retain raw stdout/stderr and output JSONL under D035 local output paths,
- keep local-only boundary flags and fail-closed behavior.

## Current Recommendation

Do not set a current `SQLRB_VERIEQL_CMD` expecting the existing wrapper to work directly. The correct future root is:

```text
SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

The command path remains pending adapter/dependency work.
