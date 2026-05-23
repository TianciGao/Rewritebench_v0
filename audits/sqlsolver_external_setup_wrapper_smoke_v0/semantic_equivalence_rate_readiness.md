# Semantic Equivalence Rate Readiness

SQLSolver is now ready for a tiny local exact-candidate verifier pass from an infrastructure perspective:

- External SQLSolver source was cloned and built.
- JAR-mode wrapper discovery works.
- The wrapper can invoke the official JAR with SQL, schema, and output files.
- Synthetic `EQ` and `NEQ` paths both produced clean decidable outputs.
- Focused tests and full user-entry tests passed.

Remaining gates before any paper-facing metric:

- Run a tiny exact-candidate local pass with identity sanity checks.
- Report attempted, decidable, unknown, timeout, and tool-error coverage.
- Keep SQLSolver evidence support-only until a separate promotion task authorizes paper-facing use.
- Investigate any `NEQ` on identity pairs or local result-consistent no-op candidates before promotion.

Official Semantic Equivalence Rate remains uncomputed in this task.
