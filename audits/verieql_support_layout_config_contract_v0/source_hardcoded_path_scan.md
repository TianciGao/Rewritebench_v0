# Source Hardcoded Path Scan

Scan scope:

- `src/`
- `tests/`
- `scripts/`
- `docs/`
- `repository_spec/`
- `.github/`

VeriEQL-specific machine-local path scan:

- No committed source/test/script/doc/workflow path contains `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql`.
- No committed source/test/script/doc/workflow path contains `/home/tianci_gao/.venvs/sqlrb-verieql`.
- No committed source/test/script/doc/workflow path hard-codes `SQLRB_VERIEQL_ROOT`, `SQLRB_VERIEQL_PYTHON`, `SQLRB_VERIEQL_CMD`, or `VERIEQL_ROOT` to a machine-local path.

Repository-wide external artifact scan excluding audits, runtime output, and `runs/user` found no VeriEQL support folder, VeriEQL source tree, venv, native dependency tree, or build output in the release repo.

Project-control and audit files intentionally record machine-local VeriEQL paths as historical local diagnostic provenance.
