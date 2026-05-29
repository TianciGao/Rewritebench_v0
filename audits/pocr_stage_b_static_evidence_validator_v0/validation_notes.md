# Validation Notes

## Summary

- `python -m py_compile $(rg --files src/sql_rewrite_bench/pocr -g '*.py')`: passed.
- `pytest tests/pocr -q`: passed, 48 tests.
- Common-core skills parser inventory: parsed and validated 40/40 root-level `skills.md` files.
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Candidate resolver dry-run: resolved 40/40 rows from `runs/user/common_core_pg_noop_db_checker/candidate_sql/`.
- Annotation resolver output: 40 rows, with `present=3`, `schema_invalid=1`, and `missing=36`.
- Static Stage B diagnostic output: 40 rows.
- `official_pocr_computed=true` rows: 0.
- Route-level POCR aggregation output: none produced.
- Static validated operation atoms in the dry-run: 0.
- Static rejected operation atoms in the dry-run: 3, from unsupported prior-smoke evidence-ref syntax.

## File Checks

- CSV parse checks passed for:
  - `annotation_artifact_inventory.csv` (40 rows)
  - `static_evidence_validation_examples.csv` (5 rows)
  - `diagnostic_row_drafts_with_static_stage_b.csv` (40 rows)
- JSONL parse check passed for the read-only input `audits/pocr_live_api_annotation_smoke_v0/safe_annotation_outputs.jsonl` (4 rows).
- Markdown non-empty checks passed for all audit Markdown files.

## Boundary Checks

- No live LLM/API call was run.
- No API key was read.
- No DB/checker/timing command was run.
- No baseline was run or rerun.
- No `compute-local-metrics` command was run.
- No verifier command was run.
- No official Positive Operation Coverage Rate was computed.
- No route-level POCR aggregation was produced.
- No user-output integration was added.
- No paper-facing metric/report/result was promoted.
- No `cases/`, root-level `skills.md`, `skill/` folders, `output/`, top-level `reports/`, top-level `results/`, or `runs/` files were modified.
- Existing files under `runs/user/common_core_pg_noop_db_checker/candidate_sql/` were read-only inputs and were not staged.

## Hygiene Checks

- Changed-file secret scan: passed.
- `git diff --check`: passed.
- Protected-path review: passed.
- Unrelated untracked directories and zip/Zone.Identifier files remain untracked and were not staged.
