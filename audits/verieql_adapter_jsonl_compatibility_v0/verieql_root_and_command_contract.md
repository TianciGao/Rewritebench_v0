# VeriEQL Root And Command Contract

## Root Variables

Supported root variables:

- `SQLRB_VERIEQL_ROOT`
- `VERIEQL_ROOT`

Expected root shape:

```text
<root>/
  parallel/
    cli_within_timeout.py
```

The known local staged root is:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

## Command Resolution

When a root is configured, the wrapper uses JSONL batch mode.

Default command base:

```text
<current python> -m parallel.cli_within_timeout
```

If `--tool-cmd` or `SQLRB_VERIEQL_CMD`/`SQLRB_VERIEQL_COMMAND` is supplied while a root is present, the command is treated as the batch command base. If the command does not already include `-m` or `parallel.cli_within_timeout`, the wrapper appends:

```text
-m parallel.cli_within_timeout
```

Final batch command:

```text
<base> -f <verieql_pairs.jsonl> -t <timeout> -o <verieql_output.jsonl>
```

The command runs with `cwd=<SQLRB_VERIEQL_ROOT>`.

## Fail-Closed States

- Missing root: `tool_available=false`, `detection_reason=verieql_root_not_found`.
- Missing batch command executable: `tool_available=false`, `detection_reason=verieql_batch_command_not_found`.
- Missing Python dependency at invocation: per-pair `tool_error`, summary `na_reason=verieql_dependency_missing`.
- Dry run: per-pair `not_attempted`, summary `na_reason=verieql_dry_run_not_executed`.
