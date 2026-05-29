# Boundary Checklist

- [x] Documentation/layout hygiene only.
- [x] No benchmark data moved.
- [x] No `cases/`, `case_sets/`, `schemas/`, or `inventory/` migration.
- [x] No `scripts/dev` migration.
- [x] No source code changes.
- [x] No test changes.
- [x] No experiment run.
- [x] No baseline run.
- [x] No verifier run.
- [x] No metrics computation.
- [x] No official Semantic Equivalence Rate computation.
- [x] No paper report/result update.
- [x] No retained-evidence promotion.
- [x] No leaderboard output.
- [x] No denominator change.
- [x] No case membership change.
- [x] No paper result change.
- [x] No runtime artifacts committed.
- [x] D035 exported output roots documented.
- [x] `runs/user/<run_id>/` documented as internal transitional staging.
- [x] Physical migration to `benchmarks/` deferred.

Final validation:

- [x] Audit Markdown files are non-empty.
- [x] D035 output roots appear in reviewed docs.
- [x] `runs/user` mentions are internal transitional staging or runner-managed staging.
- [x] No reviewed user-facing doc describes `runs/user/<run_id>/` as the primary user output root.
- [x] `git diff --check` passed.
- [x] Protected runtime/source/test/data surfaces are unchanged.
