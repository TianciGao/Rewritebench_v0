# Validation Notes

Validation planned and completed before commit:

- CSV parse checks for `learnedrewrite_runtime_readiness_matrix.csv`.
- JSON parse checks for `synthetic_request.json` and
  `synthetic_preflight_result.json`.
- Markdown/text non-empty checks for generated audit files.
- Runtime asset paths are outside the release repo.
- No JAR/source/rules asset copied into the release repo.
- No Common-core SQL sent to the real runtime.
- No DB/checker/timing/local_metrics/verifier command occurred.
- No R-Bot/LLM-R2/live LLM call occurred.
- No old result copied as canonical metrics.
- No top-level reports/results update.
- No runtime outputs staged except audit-safe summaries.
- Runtime shutdown check passed: no listener on port `6336` and no
  `rewriter_java.jar` process remained after the test.
- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q` passed.
- `python -m py_compile baselines/learnedrewrite/adapter.py` passed.
- `git diff --check` passed.
- Changed-file secret scan passed.
- Protected-path review passed.

Boundary result:

- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
