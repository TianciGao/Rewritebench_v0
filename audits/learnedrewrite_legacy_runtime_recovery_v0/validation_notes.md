# Validation Notes

Validation performed:

- CSV parse checks: passed for `legacy_learnedrewrite_artifact_inventory.csv` and `learnedrewrite_runtime_readiness_matrix.csv`.
- JSON parse checks: passed for `synthetic_preflight_request_safe.json`.
- Markdown/text non-empty checks: passed for all generated Markdown/text audit files.
- Adapter fixture tests: `pytest tests/user_entry/test_learnedrewrite_adapter.py -q` passed, `12 passed, 8 subtests passed`.
- Adapter py_compile: `python -m py_compile baselines/learnedrewrite/adapter.py` passed.
- Old repo inspection boundary: read-only commands only.
- Online/official reference boundary: official LearnedRewrite README/API and online legacy report path documented.
- No Common-core SQL sent: passed by command log; no runtime request was issued.
- No upstream or legacy JAR copied: passed; no binary, Java, class, archive, or dependency artifact appears under the audit packet.
- No old result copied as canonical metric: passed; audit files contain references and summaries only.
- No prohibited command: passed; command log contains no DB/checker/timing/local_metrics/verifier/R-Bot/LLM-R2/LLM/paper/Track A 120 command.
- Protected path review: passed; intended changes are restricted to `audits/learnedrewrite_legacy_runtime_recovery_v0/` and project-control files.
- Changed-line secret-value scan: passed; no API key value, bearer token, private key, or password assignment was found in the diff.
- `git diff --check`: passed.

Expected validation outcome:

- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
