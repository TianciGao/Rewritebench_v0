# CONS_0005 Execution Review

Acceptance check:
- Prior invalid PostgreSQL qualification `"table1"."table2"."i"`: absent.
- Prior invalid MySQL/Spark qualification `` `table1`.`table2`.`i` ``: absent.

PostgreSQL:
- candidate generated: yes
- preflight passed: yes
- source executable: yes
- candidate executable: yes
- checker attempted: yes
- exact/result-consistent: yes

MySQL:
- candidate generated: yes
- preflight passed: yes
- source executable: yes
- candidate executable: no
- checker attempted: no
- failure bucket: `candidate_execution_failed`
- adapter warning: `ARRAY_ANY is unsupported`
- execution error summary: MySQL rejected the generated candidate near the lambda expression in `ARRAY_ANY(..., _x -> table1.j = _x)`.

Spark:
- candidate generated: yes
- preflight passed: yes
- source executable: yes
- candidate executable: yes
- checker attempted: yes
- exact/result-consistent: no
- failure bucket: `mismatch`
- mismatch summary: source returned 0 rows, candidate returned 1 row `{i: 1, j: 3}`.

Conclusion:
- The original invalid-qualification blocker is fixed under execution.
- MySQL now exposes a separate dialect-emission blocker around `ARRAY_ANY`.
- Spark exposes a semantic mismatch on this optimized rewrite and must be triaged before broader use.
