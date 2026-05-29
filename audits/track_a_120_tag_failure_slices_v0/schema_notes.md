# Schema Notes

`route_tag_slice_summary.csv` copies existing per-engine `tag_slices.csv` rows. The source schema is aggregate by `axis,tag` and does not contain `pool`, `case_id`, `candidate_execution_failed`, `source_execution_failed`, `unsupported_engine`, or `no_candidate_sql`. Those absent fields are recorded as `NA` rather than inferred.

`route_failure_by_tag.csv` and downstream frontier tables use existing source-run ledgers for per-row failure/status fields. Because `tag_slices.csv` is aggregate and cannot identify the case IDs behind a tag count, the per-case taxonomy join uses the case manifest paths recorded in each source run's `selected_cases.csv`. This is metadata-only reconstruction of the same retained manifest taxonomy consumed by `src/sql_rewrite_bench/tag_slices.py`; it does not inspect SQL text, positive rewrites, hard negatives, README text, checker files, or execution outputs to infer operation atoms.

No POCR, SER, official metric, primary local metric, or leaderboard field is computed here. Counts are diagnostic tag/failure aggregations only.
