# verieql_support_layout_config_contract_v0

Verdict: completed with one narrow config-contract code/test hardening change.

VeriEQL support remains located in the approved verifier-support layer:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- shared verifier-support helpers under `src/sql_rewrite_bench/verifier_support/`
- focused tests under `tests/user_entry/test_verieql_support.py`

No top-level `VeriEQL_support/`, `verieql_support/`, `tools/verieql/`, `configs/verieql/`, repository-local VeriEQL source tree, venv, native dependency tree, or build output was found or created.

Configuration discovery is environment-variable based. Staged-root batch mode supports `SQLRB_VERIEQL_ROOT` and `VERIEQL_ROOT`; external Python selection now supports `SQLRB_VERIEQL_PYTHON`; explicit command selection remains available through `SQLRB_VERIEQL_CMD`.

Runtime outputs remain local-only. Audits use `/tmp/...`; user-facing verifier output remains under `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.

Paper-facing VeriEQL SER promotion remains blocked due the existing coverage/identity limitations.
