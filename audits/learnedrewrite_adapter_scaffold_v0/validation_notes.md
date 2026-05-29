# Validation Notes

Validation is completed for the fixture-only scaffold.

## Tests

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed, `12 passed, 8 subtests passed`.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.

## Closeout Checks

- CSV parse checks passed for `fixture_test_matrix.csv` with 12 rows.
- Markdown/text non-empty checks passed for all audit Markdown/text files.
- Upstream artifact-copy check passed: no `.java`, `.jar`, `.class`, `.zip`, `.tar`, `.gz`, `.bin`, `.pt`, `.pth`, or `.ckpt` file was added under the allowed LearnedRewrite paths.
- No Java runtime command occurred. Command log review found only the explicit boundary statement that no Java/JAR command was run.
- No DB/checker/timing/local_metrics/verifier command occurred. Command log review found only validation commands and explicit no-run boundary statements.
- Runtime output staging check passed before explicit staging; no `runs/user`, `/tmp`, `output`, top-level `reports`, or top-level `results` path is in the changed-file set.
- `git diff --check`: passed.
- Changed-file secret scan: passed; no API key values or bearer-token-shaped values were found in changed files.
- Protected-path review: passed after explicit staging.
- Staged-file secret scan: passed after explicit staging.

## Local Cache Note

Validation created ignored local `__pycache__` directories under `baselines/learnedrewrite/` and `tests/user_entry/`. They are not staged and are not runtime artifacts.

## Boundary

The task did not run the real LearnedRewrite runtime, Java server/JAR, R-Bot, LLM-R2, live LLM calls, DB execution, checker execution, timing, local metrics, SQLSolver, VeriEQL, official metrics, paper rendering, retained-evidence promotion, leaderboard generation, or Track A 120.
