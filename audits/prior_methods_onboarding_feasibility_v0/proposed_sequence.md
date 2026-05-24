# Proposed Sequence

## 1. LearnedRewrite No-Live Wrapper Design

Start with LearnedRewrite because it has the narrowest runtime shape: Java/Calcite, complete SQL output in JSON, and no required live LLM call. Do not vendor upstream source. Build only a release-repo adapter contract that can point to an external checkout or jar.

First task:

- confirm repository license/source-use boundary;
- write schema JSON conversion fixtures from case-package schema metadata;
- write parser tests for `/rewriter` JSON output and `test_workload` output;
- classify source-like/no-op outputs separately from nontrivial rewrites;
- do not run DB/checker/timing or compute metrics.

## 2. LearnedRewrite Bounded PostgreSQL Smoke

Only after no-live fixtures pass, authorize a tiny PostgreSQL-only smoke on 2-4 Common-core rows. This should go through `python -m cli.main user evaluate`, with DB/checker/timing only if separately authorized. It must remain local diagnostic and denominator-labeled.

## 3. LLM-R2 One-Row No-Live Wrapper

Next, build a no-live wrapper for LLM-R2 that can transform one case package into native query/schema/pool inputs and parse one generated SQL output. Use old PG9 and recovered PG6 artifacts only as fixture references. Do not call an LLM in this stage.

Required before live:

- route distinction between original LLM-R2 and recovered-extraction route;
- output extraction fail-closed policy;
- provider env contract compatible with SQL-RewriteBench;
- checkpoint provenance review.

## 4. R-Bot Substrate Freeze

R-Bot should wait until the retrieval corpus, Chroma index, embedding model/provider, selected rule corpus, contamination policy, and Java rewrite substrate are frozen. Only then should a single-row fake/no-live adapter be implemented.

Required before live:

- retrieval index materialization policy;
- corpus/source text manifest and hash review;
- provider/embedding secret-safety plan;
- DB setup and query/dataset mapping policy;
- output artifact contract for final SQL, selected rules, token/cost metadata, and retrieval trace.

## 5. Promotion Rules For Any Method

Each method must eventually follow:

1. no-live fixture adapter tests;
2. tiny bounded local smoke;
3. bounded PostgreSQL diagnostic if engine support is PG-only;
4. only then a 120-shaped local diagnostic if the method can preserve denominator visibility for all PostgreSQL/MySQL/Spark rows;
5. `python -m cli.main user compute-local-metrics` only after a D035 user-run ledger exists.

Old outputs may inform fixtures and expected failure buckets. They must not become new canonical local metrics, official metrics, paper results, retained evidence promotion, or leaderboard input.
