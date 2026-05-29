# Prior Methods PG40 Tag Failure Slices

This packet builds a unified PostgreSQL-only PG40 diagnostic join between prior-method failure buckets and retained case taxonomy tags.

Methods included:

- `learnedrewrite`, from `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/` and `audits/learnedrewrite_pg40_route_boundary_policy_v0/`
- `rbot_gpt54_adapted`, from `audits/rbot_gpt54_pg40_bounded_local_diagnostic_rerun_with_metrics_v0/` and `audits/rbot_gpt54_pg40_route_boundary_policy_v0/`
- `llm_r2_gpt54_adapted`, from `audits/llm_r2_gpt54_pg40_bounded_local_diagnostic_v0/` and `audits/llm_r2_gpt54_pg40_route_boundary_policy_v0/`

Top diagnostic findings:

- LearnedRewrite has the broadest PG40 frontier, with mismatch, candidate-execution-failed, and fail-closed/no-candidate rows.
- R-Bot adapted GPT-5.4 has three PG40 non-exact rows: `PORT_0013`, `PERF_0008`, and `LONGTAIL_0011`.
- LLM-R2 adapted GPT-5.4 has one PG40 non-exact row: `LONGTAIL_0011`.
- `LONGTAIL_0011` is the repeated cross-method candidate-execution boundary.
- Source-like/no-op diagnostics appear for LearnedRewrite on `CONS_0036` and `CONS_0037`, and for LLM-R2 on `CONS_0037`; R-Bot has none in the source audit.

Missing artifacts: none for this diagnostic join. The source PG40 audit CSV/JSON/Markdown packets and case manifests are sufficient. No raw runtime outputs are required or used.

Next safe action: write a unified local diagnostic evidence index / result-location summary covering Track A 120 canonical routes, verifier/support packets, and PostgreSQL-only prior-method bounded evidence. Do not expand prior methods beyond PG40 without separate engine-support or Track A support-assessment authorization.
