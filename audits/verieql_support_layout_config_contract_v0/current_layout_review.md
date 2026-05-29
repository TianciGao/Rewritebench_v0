# Current Layout Review

Reviewed VeriEQL-related implementation files:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `src/sql_rewrite_bench/verifier_support/__init__.py`
- `src/cli/main.py`
- `tests/user_entry/test_verieql_support.py`
- current VeriEQL audit packets

Layout conclusion:

- Core VeriEQL wrapper code is under `src/sql_rewrite_bench/verifier_support/verieql.py`.
- Shared verifier support imports remain under `src/sql_rewrite_bench/verifier_support/`.
- The CLI only calls the existing verifier-support wrapper; no new CLI surface was added.
- Focused tests remain under `tests/user_entry/`.
- Audit packets remain under `audits/`.

No misplaced VeriEQL support/config directory was found.

Schema directories named `schemas/verieql_cons0036_v0/` and `schemas/verieql_cons0037_v0/` are case schema assets from prior bounded diagnostics, not VeriEQL support/config code or vendored tool trees.
