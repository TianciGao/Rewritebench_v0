# Legacy Runtime Command Recovery

## Local Legacy Repo Findings

The legacy repository at `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/` does not contain a runnable LearnedRewrite JAR. A read-only `find -iname '*.jar'` under that tree returned no paths.

The legacy repo does contain setup and evidence notes that recover two historical setup strands:

- Embedded LLM4Rewrite/JPype path:
  - old JAR path recorded in notes: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/CalciteRewrite/out/artifacts/LearnedRewrite_jar/LearnedRewrite.jar`
  - old runner path recorded in notes: `/tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter/test_learned_rewrite.py`
  - old future command shape recorded as not run:

```bash
cd /tmp/rewritebench_prior_method_audit/LLM4Rewrite/my_rewriter
PYTHONPATH=.. python3 test_learned_rewrite.py \
  --database rewritebench_perf_0006 \
  --logdir /tmp/rewritebench_learnedrewrite_logs
```

- Official standalone HTTP runtime path:
  - official local source clone path inspected read-only: `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/`
  - runtime JAR candidate: `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar`
  - dependency JAR directory: `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/calcite_core_main_jar/`
  - official README command shape:

```bash
java -jar /path/to/rewriter_java.jar --server.port=6336
```

## Env Vars And URLs

No release-wrapper runtime environment was configured during this task:

- `SQLRB_LEARNEDREWRITE_CMD`: not present.
- `SQLRB_LEARNEDREWRITE_URL`: not present.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME`: not present.
- port `6336`: no listening process found by `ss -ltnp`.

No old repo env file or secret-bearing setup file was copied or modified.

## Request/Response Shape

The official README documents:

```text
POST /rewriter
{ "sql": "...", "schema": ... }
```

The inspected upstream `request.txt` example indicates an observed JSON response shape with:

- `status`
- `message`
- `data.rewritten_sql`
- `data.origin_sql`
- `data.is_rewritten`
- cost and plan fields

The release adapter should prefer `data.rewritten_sql` only after a synthetic non-benchmark preflight confirms the same shape for the configured runtime. The old request log itself must remain external and must not be copied as new evidence.

## Usability Verdict

A command shape and a local external JAR candidate exist outside the release repo, but there is no configured runtime URL or command for the current release wrapper. Starting the JAR here would be a runtime setup action rather than a query of an already configured safe external runtime, so no synthetic preflight was attempted.
