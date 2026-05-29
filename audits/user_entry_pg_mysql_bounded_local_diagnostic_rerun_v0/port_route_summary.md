# PORT Route Summary

The bidirectional PORT controlled diagnostics are already closed separately:

- Forward route: MySQL source-reference to PostgreSQL target-candidate for `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`, controlled exact 5/5.
- Reverse route: PostgreSQL source-reference to MySQL target-candidate for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`, controlled exact 4/4.

This rerun used `examples/user/noop_adapter.py`. The no-op adapter emits source-like SQL and is not the same thing as a controlled target-reference adapter. Therefore, no-op cross-dialect target-candidate failures should not be interpreted as official method failure, paper evidence, or cross-dialect benchmark accuracy.

In this snapshot:

- PostgreSQL selected 5 forward cross-dialect PORT rows. Their MySQL source-reference execution succeeded, then PostgreSQL target-candidate execution failed because the no-op candidate remained MySQL-like source SQL.
- MySQL selected 4 reverse cross-dialect PORT rows. Their PostgreSQL source-reference execution succeeded, then MySQL target-candidate execution failed because the no-op candidate remained PostgreSQL-like source SQL.

The controlled target-reference diagnostics remain the relevant evidence for PORT route correctness and checker handoff.
