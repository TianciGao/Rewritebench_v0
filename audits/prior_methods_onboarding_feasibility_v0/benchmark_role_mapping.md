# Benchmark Role Mapping

This packet reviews R-Bot, LLM-R2, and LearnedRewrite before any adapter implementation or experiment. The role assignments below are feasibility recommendations only; they do not authorize runs, metrics, or paper-facing promotion.

## Shared Repository Boundary

SQL-RewriteBench Common-core v0 Track A is a 120 planned-row same-engine denominator: 40 cases across PostgreSQL, MySQL, and Spark. A prior method can enter Track A canonical local diagnostics only after it has a D035 user-facade adapter that emits row-level candidate SQL, metadata, failure buckets, DB/checker/timing artifacts where applicable, and local-only flags. Old legacy evidence can inform fixtures and expectations, but it cannot be imported as new canonical local metrics.

## R-Bot / LLM4Rewrite

Recommended initial placement: bounded prior-method appendix evidence.

R-Bot is an LLM/RAG-guided rule-selection and rewrite pipeline. The official repository expects PostgreSQL datasets, a built rewrite-evidence retrieval index, a configured provider, and a Calcite/Java rewrite substrate. Legacy evidence contains meaningful R-Bot artifacts, including formal 120-labeled generation planning, PG40 generation expansion, PG15 execution/timing, and older PG-only slices. That evidence is valuable, but it is not a D035 local diagnostic route and is not tri-engine Track A output.

Safe onboarding role:

- Start with a no-live substrate inventory and fake provider wrapper tests.
- Then use a bounded PostgreSQL-only fixture subset after the retrieval corpus/index and contamination policy are frozen.
- Keep MySQL/Spark as denominator-visible unsupported rows if a 120-shaped route is ever planned.

Not safe to claim now:

- Full Track A 120 readiness.
- Direct comparability with tri-engine local metrics.
- Any leaderboard placement.

## LLM-R2

Recommended initial placement: recovered-output audit only, then bounded prior-method appendix evidence if a one-row wrapper becomes stable.

LLM-R2 uses an LLM to choose rewrite rules, with a trained demonstration selector and a Java rule applier. The official source has a TPCH selector checkpoint and native schema/query/pool layouts, but it is not row-scoped for SQL-RewriteBench. Legacy evidence shows PG9 original-route bounded evidence and a separate PG6 recovered-extraction route. The recovered route is useful for extraction tests, but it must remain distinct from original LLM-R2 route semantics.

Safe onboarding role:

- First build a no-live D035 wrapper fixture for one PostgreSQL row.
- Use legacy recovered outputs only as extraction fixtures and route-boundary examples.
- Do not merge recovered-route rows into original-route metrics.

Not safe to claim now:

- Track A 120 readiness.
- MySQL/Spark support.
- OpenAI-compatible provider compatibility without wrapper changes.

## LearnedRewrite

Recommended initial placement: bounded prior-method appendix evidence, with LearnedRewrite as the next implementation candidate if legal/source hygiene is acceptable.

LearnedRewrite is a Java/Calcite rewrite system with an HTTP server and workload entrypoints that can emit complete rewritten SQL. It does not need live LLM calls for the core rewrite path. This makes it the most plausible first adapter candidate technically. The blockers are repository license absence, local-path assumptions, Calcite dialect/schema conversion, source-like/no-op output handling, and a secret-safety concern in an upstream helper source file.

Safe onboarding role:

- Start with a no-live external Java wrapper design and synthetic fixture tests.
- Build a schema JSON converter from case-package schema metadata.
- Use a very small PostgreSQL-only bounded smoke after legal/source hygiene is resolved.

Not safe to claim now:

- Full Track A 120 readiness.
- MySQL/Spark support.
- Meaningful rewrite improvement without source-like/no-op diagnostics.

## Overall Verdict

The safest next adapter candidate is LearnedRewrite, narrowly scoped to no-live wrapper/fixture work first. R-Bot and LLM-R2 need larger substrate and provider-control tasks before method execution. All three must stay role-aware, denominator-aware, and local-diagnostic-only until a separate promotion task exists.
