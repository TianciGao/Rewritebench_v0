# LearnedRewrite Source Hygiene Review

## Official Source

Official source location:

- `https://github.com/XuanheZhou/LearnedRewrite`

Read-only local reference used for this audit:

- `/tmp/sqlrb_prior_methods_sources/LearnedRewrite`
- observed commit: `4fd732b`

Official paper/reference recorded in the onboarding audit:

- `https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/vldb22-query-rewrite.pdf`

## License And Vendoring

No repository-level `LICENSE`, `COPYING`, or `NOTICE` file was found in the official source clone during the prior onboarding review or this design pass.

Vendoring verdict:

- Do not vendor upstream source code.
- Do not vendor `rewriter_java.jar`.
- Do not vendor Calcite dependency JARs from the upstream repository.
- Do not vendor checkpoints, datasets, generated outputs, request logs, or local runtime artifacts.

The release repo may contain only a thin external-wrapper adapter and fixture tests written in this repo.

## Source Hygiene Notes

The official source includes:

- Java source files under `src/`.
- A packaged `rewriter_java.jar`.
- many dependency JARs under `calcite_core_main_jar/`.
- an HTTP server entrypoint documented as `java -jar .../rewriter_java.jar --server.port=6336`.
- an API shape documented as `/rewriter POST {sql: "...", schema: {...}}`.
- code paths that can write local request files such as `request.txt`.

The official source also contains an API-key-looking hard-coded field in an upstream helper source file. The value was not copied into this repo or this audit packet. Future wrapper work must not copy that file content into release artifacts.

## External Runtime Policy

LearnedRewrite must be treated as an external runtime:

- The user or developer supplies an external checkout, JAR path, or HTTP endpoint.
- The release adapter reads only environment variables that point to that external runtime.
- The adapter writes only D035 row workspace metadata and candidate SQL.
- The adapter fails closed if the runtime is missing, unavailable, times out, emits invalid JSON, omits `rewritten_sql`, or emits ambiguous SQL.

Suggested future environment variables:

- `SQLRB_LEARNEDREWRITE_URL`: HTTP endpoint, for example `http://127.0.0.1:6336/rewriter`.
- `SQLRB_LEARNEDREWRITE_CMD`: optional external command wrapper for a row-scoped CLI.
- `SQLRB_LEARNEDREWRITE_TIMEOUT`: per-row timeout in seconds.
- `SQLRB_LEARNEDREWRITE_MODE`: `fake`, `http`, or `cmd`.
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`: fixture-only fake JSON response for tests.

No secret is required for LearnedRewrite.

## Safe References

It is safe to reference:

- official repo URL;
- paper URL;
- documented API shape;
- expected `rewritten_sql` output field;
- high-level dependency notes;
- read-only legacy evidence paths as fixture design references.

It is not safe to copy:

- upstream Java source;
- upstream JARs;
- dependency JARs;
- local request logs;
- hard-coded secret-looking values;
- old generated candidate outputs as current canonical outputs.
