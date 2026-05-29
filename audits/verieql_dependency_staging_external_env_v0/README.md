# VeriEQL Dependency Staging External Env V0

Verdict: `external_env_staged_help_probe_ready`.

This audit staged a local Python virtual environment outside the release repository for the already-discovered VeriEQL source tree:

- VeriEQL root: `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL`
- External venv: `/home/tianci_gao/.venvs/sqlrb-verieql`
- Python: `Python 3.12.3`

The venv was created outside `/home/tianci_gao/code/Rewritebench_v0`, dependencies were installed into that venv only, and no real SQL pair verification was run.

Non-experiment probes passed:

- Required import probe: passed for `ujson`, `z3`, `ordered_set`, `lark`, `prettytable`, and `mysql.connector`.
- VeriEQL batch CLI help probe: `python -m parallel.cli_within_timeout --help` passed from the VeriEQL root.

Future bounded canary environment contract:

```bash
export SQLRB_VERIEQL_ROOT=/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
export SQLRB_VERIEQL_PYTHON=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
export SQLRB_VERIEQL_CMD=/home/tianci_gao/.venvs/sqlrb-verieql/bin/python
```

`SQLRB_VERIEQL_PYTHON` is the intended explicit Python path for future documentation/contracts. The current wrapper command hook is `SQLRB_VERIEQL_CMD` or CLI `--tool-cmd`, which should use the same venv Python path for the staged-root batch invocation.

The staged VeriEQL Git tree remained unchanged relative to preflight: it still has the pre-existing `M constants.py` modification and no new tracked or untracked changes were introduced by this task.

Boundary: local dependency staging only; no `CONS_0007` canary, no Common-core run, no Semantic Equivalence Rate computation, no official metrics, no top-level `reports/` or `results/`, no retained evidence promotion, and no leaderboard.
