# Official Runtime Contract Review

Official source reviewed:

- GitHub: `https://github.com/XuanheZhou/LearnedRewrite`
- Local source clone inspected read-only: `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/`

## Runtime

The official README describes LearnedRewrite/evolveRewrite as a Java/Calcite-based SQL rewrite system. It states that a Java environment is required and recommends JDK 11 or later.

The local machine has Java available:

```text
openjdk version "17.0.18" 2026-01-20
```

## HTTP Server

The official README documents an HTTP server start shape:

```bash
java -jar /path/to/rewriter_java.jar --server.port=6336
```

It documents a `/rewriter` API:

```text
POST /rewriter
{ "sql": "...", "schema": ... }
```

## Observed Response Shape

The upstream source clone contains a `request.txt` example log. It was inspected only to infer response shape. The observed successful response contains a top-level `status` and `message`, with a `data` object containing `rewritten_sql`, `origin_sql`, `is_rewritten`, cost fields, and plan/tree details.

For the release adapter, the safe extraction target is:

```text
data.rewritten_sql
```

The adapter must still fail closed if the configured runtime returns malformed JSON, no `rewritten_sql`, empty SQL, prose only, or multiple SQL statements.

## Compatibility Gaps

- The current release adapter scaffold has fail-closed real `cmd` and `http` hooks; it does not yet invoke a real runtime.
- A schema JSON serialization policy must be implemented and tested before Common-core SQL is sent.
- The official schema example appears TPC-H oriented and cannot be blindly reused for Common-core schemas.
- MySQL and Spark support are not recovered. Initial real runtime smoke should be PostgreSQL-only.
- The runtime can produce Calcite-style quoted identifiers and multiline SQL; single-SQL extraction must preserve content while rejecting multiple statements.

## No-Vendor Boundary

The official source, JAR, dependency JARs, schema examples, request logs, datasets, generated outputs, and checkpoints remain external. Nothing from upstream was copied into the release repo.
