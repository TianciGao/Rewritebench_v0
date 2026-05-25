# Paper Table Usage Notes

## Main Text Candidates

`table1_paper_metric_route_evidence_ledger.md` can support a compact main-text local diagnostic summary if the paper labels these values as local diagnostic evidence and keeps Track A 120 separate from PostgreSQL-only PG40 prior-method evidence.

`table4_metric_availability_and_boundary.md` is suitable for main text or a short methodology note because it states which paper metrics are currently available, `N.A.`, coverage-limited, or deferred.

## Appendix Candidates

`table2_failure_frontier_summary.md`, `table3_failure_bucket_taxonomy_diagnostic_summary.md`, and `table5_evidence_location_index.md` are better appendix tables. They are detailed support tables for error analysis, taxonomy slicing, and artifact traceability.

## How To Cite Track A 120 Versus PG40

Track A 120 rows use the same-engine planned denominator of 120 case-engine rows. PostgreSQL-only PG40 prior-method rows use 40 PostgreSQL Common-core rows. These scopes are different and should not be merged or directly ranked.

R-Bot and LLM-R2 PG40 rows are adapted GPT-5.4 local diagnostics. They are not original-paper reproductions and did not use the official R-Bot or LLM-R2 stacks. LearnedRewrite PG40 is PostgreSQL-only external-runtime bounded evidence.

## Why No Global Leaderboard

The metric contract and migration decisions prohibit a global leaderboard. The evidence combines different roles and scopes: Track A 120 rewrite routes, PostgreSQL-only PG40 prior-method bounded diagnostics, and verifier/support packets. These are not a single comparable competition table.

## Why Verifier Support Is Separate

SQLSolver and VeriEQL are verifier support tools, not rewrite-generation baselines. They inform Semantic Equivalence Rate readiness and status boundaries, but they do not produce candidate rewrites and should not appear as rewrite methods.

Semantic Equivalence Rate is computed only from formal verifier evidence. Local checker exactness is not Semantic Equivalence Rate evidence.

## Why Positive Operation Coverage Rate Remains Deferred

Positive Operation Coverage Rate requires external operation-atom evidence and a separate approved script/policy. Failure bucket x taxonomy tag slices are diagnostic/support only and must not be treated as Positive Operation Coverage Rate.
