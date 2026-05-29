# Validation Notes

## Summary

- Prompt builder alignment: implemented.
- Fixture cases retried: `PERF_0006`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`.
- Live calls attempted: 4.
- Provider label: `openai_compatible`.
- Model label: `gpt-5.4`.
- Schema-valid annotations: 4.
- Malformed/schema-invalid annotations: 0.
- Static validated operation atoms: 11.
- Static rejected operation atoms: 0.
- Insufficient-evidence atoms: 0.
- Official POCR computed: no.
- Route-level POCR aggregated: no.

## Test And Parse Checks

- `python -m py_compile $(rg --files src/sql_rewrite_bench/pocr -g '*.py')`: passed.
- `pytest tests/pocr -q`: passed, 49 tests.
- Common-core skills parser inventory: 40/40 parsed and valid.
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Candidate resolver: 40/40 PG no-op candidates resolved from `runs/user/common_core_pg_noop_db_checker/candidate_sql/`.
- Offline static evidence fixtures: passed for valid span, missing span, unsupported syntax, no-ref insufficient evidence, and semantic guard non-numerator behavior.
- Audit CSV parse checks: passed.
- Audit JSONL parse check for `safe_annotation_outputs.jsonl`: passed.
- Audit Markdown non-empty checks: passed.

## Boundary Checks

- Live calls were bounded to exactly four selected rows.
- No DB/checker/timing run occurred.
- No baseline was run or rerun.
- No `compute-local-metrics` command occurred.
- No verifier command occurred.
- No official Positive Operation Coverage Rate was computed.
- No route-level POCR aggregation was produced.
- No user-output integration was added.
- No paper-facing report/result was updated.
- No top-level `reports/` or `results/` update occurred.
- No `output/` files were created.
- No `cases/`, root-level `skills.md`, `skill/` folders, or `runs/` files were modified.

## Secret And Hygiene Checks

- API keys were sourced from environment only.
- API key values were not printed, written, staged, or committed.
- Raw prompts and raw provider responses were not stored.
- Changed-file secret scan: passed.
- `git diff --check`: passed.
- Protected-path review: passed.
