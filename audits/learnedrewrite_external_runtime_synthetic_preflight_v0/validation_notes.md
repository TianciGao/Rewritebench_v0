# Validation Notes

Validation performed:

- CSV parse checks: passed for `learnedrewrite_runtime_readiness_matrix.csv`.
- JSON parse checks: passed for `synthetic_request.json` and `synthetic_preflight_result.json`.
- Markdown/text non-empty checks: passed for all generated Markdown/text audit files.
- LearnedRewrite adapter fixture tests: `pytest tests/user_entry/test_learnedrewrite_adapter.py -q` passed, `12 passed, 8 subtests passed`.
- Adapter py_compile: `python -m py_compile baselines/learnedrewrite/adapter.py` passed.
- JAR copy check: passed; no JAR/source/dependency artifact appears under this audit packet.
- Runtime shutdown check: passed; no `rewriter_java.jar` process or listener on port `6336` remained after the preflight.
- Old repo read-only boundary: no legacy repo modifications were made.
- No Common-core SQL sent: passed by request payload and command log review.
- No DB/checker/timing/local_metrics/verifier command: passed by command log review.
- No R-Bot/LLM-R2/live LLM call: passed by command log review.
- No old result copied as canonical metric: audit contains summaries only.
- No top-level reports/results update: passed by protected-path review.
- Runtime outputs staged: only audit-safe summaries are intended for staging; `/tmp` runtime logs are not staged.
- Secret scan: planned/passed over changed files before commit.
- `git diff --check`: passed.

Expected unchanged boundaries:

- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
