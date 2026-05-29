# Validation Notes

Validation date: 2026-05-25.

Implementation validation:
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/pocr/diagnostic_output_schema.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/__init__.py`: passed.
- `PYTHONPATH=src pytest tests/pocr -q`: passed, 87 tests.
- Facade temp output-root tests: passed; diagnostic files were written only under pytest temporary directories.

Common-core skills validation:
- Common-core root-level `skills.md` parse count: 40.
- Valid contracts: 40.
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Parsed operation atoms: 107.
- Parsed semantic guard atoms: 80.
- Validation issues: 0.

Audit file validation:
- `sample_diagnostic_rows.csv`: parsed successfully with 4 rows.
- `sample_diagnostic_summary_by_pool.csv`: parsed successfully with 4 rows.
- Markdown non-empty checks passed for all audit Markdown files.

Boundary validation:
- Live API calls: no.
- API keys read: no.
- DB/checker/timing runs: no.
- Baseline rerun: no.
- Official POCR computed: no.
- Route-level POCR aggregated: no.
- Paper metric promoted: no.
- Default user-run integration: no.
- Top-level `output/`, `reports/`, and `results/` writes: no.
- Case-local `runs/` writes: no.

Protected-path review:
- No `cases/` files were modified.
- No root-level `skills.md` files were modified.
- No `skill/` folders were created.
- No `output/`, top-level `reports/`, top-level `results/`, `runs/`, or `retained_evidence/` paths were modified.
- Existing `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql/` was read-only input for sample rows and was not staged.

Secret and diff checks:
- Changed-file secret scan: passed.
- `git diff --check`: passed.
- Staged protected-path scan: passed; no protected path was staged.
- Staged secret scan: passed.
- Runtime output staged check: passed; no `output/`, top-level `reports/`, top-level `results/`, or `runs/` path was staged.

No denominator, paper result, case membership, or raw legacy evidence changed.
