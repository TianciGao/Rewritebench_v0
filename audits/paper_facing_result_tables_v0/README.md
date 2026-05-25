# Paper-Facing Result Tables v0

This packet drafts paper-facing result tables from existing local diagnostic audit evidence only. It does not run experiments, recompute metrics, render paper files, promote retained evidence, or create a leaderboard.

The tables use the exact metric names from `repository_spec/metrics_contract_v1.md`:

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate
- Semantic Equivalence Rate
- GM Speedup Ratio
- Speedup Ratio Percentiles
- Positive Operation Coverage Rate
- Cross-Engine Execution Coverage Rate
- Cross-Engine Result Consistency Rate
- Cross-Engine GM Speedup Ratio

Included Track A 120 canonical local diagnostic routes:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_noop`
- `sqlglot_optimize_schema_aware`
- `calcite_hep_fail_closed`

Included PostgreSQL-only PG40 bounded prior-method evidence:

- `learnedrewrite`
- `rbot_gpt54_adapted`
- `llm_r2_gpt54_adapted`

Tables produced:

- `table1_paper_metric_route_evidence_ledger.csv` and `.md`
- `table2_failure_frontier_summary.csv` and `.md`
- `table3_failure_bucket_taxonomy_diagnostic_summary.csv` and `.md`
- `table4_metric_availability_and_boundary.csv` and `.md`
- `table5_evidence_location_index.csv` and `.md`

Boundaries:

- Track A 120 and PostgreSQL-only PG40 evidence remain separate.
- R-Bot and LLM-R2 PG40 rows are adapted GPT-5.4 local diagnostics, not original-paper reproductions.
- LearnedRewrite PG40 is PostgreSQL-only external-runtime bounded evidence.
- SQLSolver and VeriEQL are verifier support only, not rewrite-generation baselines.
- Semantic Equivalence Rate is `N.A.` or `coverage_limited`; local checker exactness is not formal verifier evidence.
- Positive Operation Coverage Rate is deferred / `N.A.`.
- No global leaderboard is created.

Next safe action: use this packet to draft or update paper Section 8 result tables and appendix artifact index. Do not run additional experiments unless a specific evidence gap is identified.
