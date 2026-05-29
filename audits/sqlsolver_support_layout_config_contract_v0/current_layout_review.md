# Current Layout Review

Reviewed SQLSolver-related implementation files:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `src/sql_rewrite_bench/verifier_support/__init__.py`
- `src/cli/main.py`
- `tests/user_entry/test_sqlsolver_support.py`
- current SQLSolver audit packets

Layout conclusion:

- Core SQLSolver wrapper code is under `src/sql_rewrite_bench/verifier_support/sqlsolver.py`.
- Shared verifier support imports remain under `src/sql_rewrite_bench/verifier_support/`.
- The CLI only calls the existing verifier-support wrapper; no new CLI surface was added.
- Focused tests remain under `tests/user_entry/`.
- Audit packets remain under `audits/`.

No misplaced SQLSolver support/config directory was found.
