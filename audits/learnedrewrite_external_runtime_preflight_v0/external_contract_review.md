# External Contract Review

## Official Source Reviewed

Official repository:

- <https://github.com/XuanheZhou/LearnedRewrite>

The official README describes LearnedRewrite/evolveRewrite as a Java/Calcite-based SQL transformation demo. It recommends JDK 11 or newer, documents starting an HTTP server with a `java -jar .../rewriter_java.jar --server.port=6336` shape, and documents an API endpoint:

```text
POST /rewriter
{ "sql": "...", "schema": { ... } }
```

The prior design packet also recorded that the official source includes Java source, a packaged JAR, Calcite dependency JARs, and local request-file behavior. These artifacts must remain external and must not be copied into this release repo.

## Expected Runtime Inputs

Expected future request inputs:

- source SQL text;
- schema JSON or schema-like object;
- target dialect/engine metadata if the external runtime supports it;
- timeout.

The current release wrapper can already resolve source SQL, target engine, and schema references, but it does not yet serialize a full schema JSON payload for a real runtime.

## Expected Runtime Outputs

The release wrapper requires exactly one complete candidate SQL statement after extraction. The fake-mode contract currently accepts JSON fields such as `rewritten_sql`, `candidate_sql`, or `sql`, then applies the single-SQL extraction policy.

For real HTTP mode, the response field must be confirmed by synthetic preflight before any Common-core run. If the real runtime returns a different response shape, the wrapper must fail closed until a narrow response adapter is implemented.

## Current Wrapper Compatibility

Compatible pieces:

- D035 row env input contract exists.
- PostgreSQL-first support policy exists.
- Candidate output path contract exists.
- Single-SQL extraction and fail-closed behavior exist.
- Metadata records local-only and no-vendor boundaries.

Current gaps:

- `http` and `cmd` modes are fail-closed placeholders and do not invoke an external runtime.
- No schema JSON serialization policy has been implemented for real runtime requests.
- No runtime response field has been confirmed against a live external endpoint.
- No runtime version/help probe contract is implemented for command mode.
- MySQL and Spark remain unsupported by policy.

## No-Vendor Boundary

Do not copy or vendor:

- upstream Java source;
- `rewriter_java.jar`;
- dependency JARs;
- checkpoints;
- datasets;
- generated outputs;
- request logs;
- private paths or secret-looking upstream values.

## Preflight Verdict

External runtime integration is not ready for Common-core rows. It first needs a configured external runtime command or local URL and one successful synthetic non-benchmark request/response preflight.
