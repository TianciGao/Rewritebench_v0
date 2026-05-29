# Verifier Pair Shape Review

Verifier output shape:
- Runtime output root: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/`.
- Pairs CSV: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/verifier_pairs.csv`.
- Verdict JSONL: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/verifier_verdicts.jsonl`.
- Summary JSON: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/semantic_equivalence_summary.json`.
- Batch JSONL input/output: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/results/verieql_exact_candidate_tiny_local_pass_v0/verifier/tools/verieql/batch/`.

Common pair fields:
- `tool=verieql`
- `pair_type=source_vs_candidate`
- `route_id=sqlglot_noop`
- `method_id=sqlglot_noop`
- `engine=postgres`
- `verifier_mode=finite_bound`
- `bound_size=10`
- `timeout_seconds=30`
- `result_checker_exactness_used=false`
- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Schema context paths:
- `CONS_0036`: `schemas/verieql_cons0036_v0/postgres/ddl.sql`
- `PERF_0077`: `schemas/job_imdb_perf0077_v0/postgres/ddl.sql`
- `PERF_0082`: `schemas/job_imdb_perf0082_v0/postgres/ddl.sql`

Observed shape notes:
- The wrapper preserved source SQL and candidate SQL paths without mutating source run artifacts.
- VeriEQL JSONL schema identifiers were canonicalized to uppercase.
- `CONS_0036` exposed a minor DDL parser rough edge for parameterized types: `VARCHAR(32)` appeared as `VARCHAR(32` in VeriEQL output metadata. This did not block the equivalent verdict, but it should be hardened before broader passes.

