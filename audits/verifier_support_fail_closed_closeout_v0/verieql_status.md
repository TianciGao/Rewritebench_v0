# VeriEQL Status

Implementation status:

- Wrapper module: `src/sql_rewrite_bench/verifier_support/verieql.py`
- Detection helper: `detect_verieql`
- Output normalization helper: `normalize_verieql_output`
- Bounded writer: `write_verieql_canary`

Local tool status from `verieql_bounded_canary_v2`:

- `tool_available=false`
- `tool_version=null`
- `detection_reason=verieql_command_not_found`
- Real VeriEQL run performed: no

Fail-closed behavior:

- Unavailable tool writes `not_attempted` verdict rows.
- Raw stdout/stderr artifact paths are still contract-shaped.
- Summary records `semantic_equivalence_rate=null`.
- Summary records `na_reason=verieql_unavailable`.

Future readiness gate:

- Provide an explicit command path or environment variable.
- Confirm tool version can be detected.
- Run one-pair bounded canary, preferably `CONS_0005` source/positive or a synthetic support pair.
- Retain raw stdout/stderr under `output/results/<run_id>/verifier/tools/verieql/`.
- Confirm normalized verdict mapping before any broader use.
