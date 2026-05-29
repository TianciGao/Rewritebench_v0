# Validation Notes

Validation performed during generation:

- Prior selected-pair CSV parsed: passed.
- Selected pair count equals 8: passed.
- Same-selection check against prior selected_pairs.csv: passed.
- Source/candidate path existence checks: passed.
- Source/candidate SHA256 checks against prior manifest: passed.
- Schema DDL path existence checks from prior notes: passed.
- SQLSolver JAR availability check: passed with detection reason `sqlsolver_jar_available`.
- Every selected pair has source identity and candidate identity verdict rows: passed.
- Actual source-candidate rows exist only for passed identity guards or explicit blockers: passed.
- No benchmark pair outside the same 8 was verified: passed by selected-pair set check.
- No VeriEQL run occurred: passed by command log.
- No local_metrics.py run occurred: passed by command log.
- No official metric was computed: passed by boundary review.
- No adapter/DB/checker/timing/LLM/Repair-1 command was run: passed by command log.

Post-generation validation:

- CSV parse checks for generated CSVs: passed.
- JSONL parse check for `sqlsolver_verdicts_after_guards.jsonl`: passed, 24 records.
- JSON parse check for `bounded_support_summary_after_guards.json`: passed.
- Markdown/text non-empty checks: passed.
- Selected pair count check: passed, exactly 8 rows.
- Same-selection check against prior `selected_pairs.csv`: passed.
- Hash check: passed for all selected source/candidate SQL paths.
- Identity guard count check: passed, 16 identity records and 8 source-candidate records.
- No benchmark pair outside the same 8 was verified: passed.
- No VeriEQL, local_metrics, official metric, adapter, DB/checker/timing, LLM, or Repair-1 command was run: passed by command log review.
- `git diff --check`: passed.
- Changed-file secret scan: passed; a value-oriented diff scan found no secret values.
- Protected-path review: passed.
