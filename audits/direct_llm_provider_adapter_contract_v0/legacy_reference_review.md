# Legacy Reference Review

Reference-only repository:
- https://github.com/TianciGao/sql-rewrite-bench

Local reference checkout:
- `/tmp/sql-rewrite-bench_legacy_ref`

Reviewed surfaces:
- `docs/_scratch/EXPANDED_PERF_DIRECT_LLM_PREFLIGHT_SUMMARY_v0.md`
- `docs/_scratch/EXPANDED_PERF_DIRECT_LLM_RUN_SCAFFOLD_SUMMARY_v0.md`
- `scripts/cli.py`

Findings used for design only:
- Legacy Direct LLM work separated prompt rendering from live API availability.
- Legacy diagnostics treated missing API environment as a route readiness blocker, not as a current-result metric.
- Legacy extraction was conservative: SQL-only responses, single candidate, and fail-closed behavior for prose or ambiguous outputs.
- Legacy model-call metadata included provider/model and extraction status concepts that are still useful for traceability.

Boundaries:
- No old results were copied.
- No old retained evidence was used as current evidence.
- No secrets were copied.
- No paper-facing output was updated.
- The new adapter implementation is in the current D035 baseline layout under `baselines/direct_llm_original/`.
