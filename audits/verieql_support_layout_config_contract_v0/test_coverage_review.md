# Test Coverage Review

Focused VeriEQL tests cover:

- unavailable command fails closed without fake verifier evidence;
- missing root fails closed;
- staged-root JSONL timeout-mode detection;
- staged-root finite-bound detection;
- `VERIEQL_ROOT` alias detection;
- `SQLRB_VERIEQL_PYTHON` external Python selection;
- missing dependency fail-closed behavior;
- timeout-mode and finite-bound command construction;
- JSONL pair generation;
- schema identifier canonicalization;
- DDL parameterized type parsing;
- JSONL output normalization for `EQU`, `NEQ`, `TMO`, `NSE`, `UNK`, `SYN`, `NIE`, `OOM`, and `OTE`;
- no local result-checker exactness substitution;
- D035-shaped temp output paths;
- no leaderboard/ranking/winner fields.

This task added two focused regression tests:

- `test_detect_verieql_root_uses_explicit_python_env`
- `test_detect_verieql_root_accepts_legacy_root_env_alias`

No real VeriEQL installation is required for the focused tests.
