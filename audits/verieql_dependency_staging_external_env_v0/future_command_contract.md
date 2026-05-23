# Future Command Contract

Recommended future environment:

```bash
export SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
export SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
export SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

Current wrapper compatibility:

- `SQLRB_VERIEQL_ROOT` selects staged-root JSONL batch mode.
- The current wrapper recognizes `SQLRB_VERIEQL_CMD` and CLI `--tool-cmd`.
- The current wrapper does not yet have a dedicated `SQLRB_VERIEQL_PYTHON` setting; record it as the intended explicit Python path, and use the same value through `SQLRB_VERIEQL_CMD` or `--tool-cmd` for now.

Expected future batch command shape:

```bash
cd /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_timeout \
  -f <pairs.jsonl> \
  -t <timeout_seconds> \
  -o <output.jsonl>
```

The release wrapper should continue to write verifier outputs only under the D035 local output contract:

```text
output/results/<run_id>/verifier/
output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

Future bounded canary recommendation:

- First target: `CONS_0007`.
- Scope: one-pair canary only.
- Required next task: separately authorized bounded canary execution.
- Boundary: local diagnostic only, not official Semantic Equivalence Rate, not paper results, not retained evidence.
