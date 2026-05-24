# LearnedRewrite Adapter Scaffold v0

## Summary

This task adds a fixture-only LearnedRewrite external-wrapper adapter scaffold at:

- `baselines/learnedrewrite/adapter.py`

The scaffold implements fake runtime mode only. It is designed to validate D035 user-facade adapter shape, single-SQL extraction, metadata hygiene, and fail-closed behavior without invoking LearnedRewrite, Java, HTTP, DB execution, checker execution, timing, local metrics, verifiers, official metrics, paper rendering, retained evidence promotion, or leaderboard generation.

## What Changed

- Added the fixture-only adapter scaffold.
- Updated the LearnedRewrite baseline README from design-only to fake-runtime scaffold status.
- Added focused fixture tests in `tests/user_entry/test_learnedrewrite_adapter.py`.
- Created this audit packet.

## Runtime Boundary

The adapter does not run the real LearnedRewrite Java runtime. Command and HTTP modes are fail-closed future hooks. Fake mode accepts a fixture JSON response or inline fake SQL, extracts exactly one SQL statement, and writes candidate SQL only when unambiguous.

## Source Hygiene

No upstream LearnedRewrite source, JAR, dependency JAR, checkpoint, dataset, generated output, request log, or old legacy output was copied into this repository.

## Validation

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.

## Next Safe Action

Authorize a no-runtime D035 user-facade smoke for LearnedRewrite fake runtime. Do not run the real Java runtime until fake user-facade integration and extraction guards are stable.
