# Validation Notes

## Runtime Probe Checks

- Java availability checked with `java -version`: passed.
- Java version: `openjdk version "17.0.18" 2026-01-20`.
- `SQLRB_LEARNEDREWRITE_CMD` presence checked without printing value: not set.
- `SQLRB_LEARNEDREWRITE_URL` presence checked without printing value: not set.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`: not set.
- Runtime reachable check: not attempted because no command or URL is configured.
- Synthetic preflight request: not attempted.

## Test Validation

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed, `12 passed, 8 subtests passed`.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.

## CSV And JSON Checks

- `learnedrewrite_runtime_readiness_matrix.csv` parse check: passed with 9 rows and all required checks represented.
- No `synthetic_preflight_result.json` exists because no synthetic request was attempted.

## Markdown Checks

- Markdown/text non-empty checks: passed for all generated Markdown/text files.

## Boundary Checks

- No Common-core case SQL sent to real runtime: passed by command log review.
- No real benchmark run: passed by command log review.
- No DB/checker/timing/local_metrics/verifier command: passed by command log review.
- No upstream source/JAR/dependency artifact copied: passed by changed-file artifact extension review.
- No runtime outputs staged: passed before explicit staging; no `runs/user`, `output`, top-level `reports`, or top-level `results` path is in the changed-file set.
- `git diff --check`: passed.
- Changed-file secret scan: passed for secret-shaped values in audit and project-control changed files.
- Protected-path review: passed; expected changed paths are this audit packet and project-control writeback only. Two unrelated pre-existing untracked Direct LLM audit directories were left untouched.
