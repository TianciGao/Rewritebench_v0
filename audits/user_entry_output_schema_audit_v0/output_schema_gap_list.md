# Output Schema Gap List

## U2 module split prerequisites

- Extract adapter invocation and candidate capture from `user_run.py` into a dedicated adapter runner design.
- Extract row consolidation and CSV writing responsibilities into a ledger writer design.
- Add a case package resolver design that resolves manifest, source SQL, schema profile, checker paths, and taxonomy/tag metadata.
- Define stable typed row models before implementation.

## U3 candidate preflight prerequisites

- Add proposed fields for preflight attempted, preflight passed, preflight status, and preflight failure class.
- Decide static checks for empty SQL, missing SQL, multi-statement SQL, unsupported statement type, unsafe SQL, parse status, and source-like/no-op classification.
- Keep preflight separate from semantic equivalence and DB execution.

## U4 local quality report prerequisites

- Define `quality_summary.json` and `quality_report.md` separately from official metrics.
- Add denominator-aware counts for selected, generated, preflight-passed, executed, checker-attempted, exact, mismatch, and failure buckets.
- Define how quality summaries treat dry-run rows and non-DB rows.

## U5 tag-aware slice prerequisites

- Add manifest/taxonomy tag resolution through a case package resolver.
- Define `tag_slices.csv` fields and denominator-aware grouping.
- Do not infer tags from SQL text at runtime.
- Do not create tag scores, rankings, or leaderboard rows.

## U6 user readability prerequisites

- Design `--list-cases`, `--explain-selection`, and `--show-output-schema`.
- Make output schema discoverable without running DB/checker execution.
- Keep docs aligned with actual schema fields.

## U7 engine router prerequisites

- Define common engine execution result interface.
- Route `postgres` to current `postgres_execution.py`.
- Add fail-closed stubs or designs for MySQL and Spark before implementation.
- Add explicit fields for DB execution attempted, source executable, candidate executable, schema setup status, and engine version.

## U8 timing diagnostic prerequisites

- Timing remains deferred.
- Define raw timing artifact schema only after timing protocol approval.
- Do not compute speedup or official timing metrics in user-entry.
- Keep `GM_Speedup` and `Speedup Ratio Percentiles` governed by `repository_spec/metrics_contract_v1.md`.

## Deferred official metrics / paper reproduction gaps

- Official metrics computation remains out of scope.
- Paper table rendering remains out of scope.
- Retained-evidence adapter integration remains out of scope.
- Reports/results migration remains out of scope.
- Full reproduction CLI remains out of scope.
- Global leaderboard remains forbidden.
