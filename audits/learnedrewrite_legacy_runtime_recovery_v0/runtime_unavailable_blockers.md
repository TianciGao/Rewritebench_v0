# Runtime Unavailable Blockers

No synthetic preflight was attempted.

Current blockers:

- `SQLRB_LEARNEDREWRITE_CMD` is not configured.
- `SQLRB_LEARNEDREWRITE_URL` is not configured.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1` is not set.
- No process was listening on port `6336`.
- The legacy local repo contains no checked-in LearnedRewrite JAR.
- The external source clone under `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/` contains `rewriter_java.jar`, dependency JARs, a schema example, and request examples, but those remain external artifacts and must not be copied into the release repo.
- The current release adapter has fail-closed real `cmd`/`http` hooks and does not yet implement real runtime invocation or schema JSON serialization.

Starting the upstream JAR from `/tmp` in this task would require runtime setup outside the already configured wrapper contract. It was not done.

Suggested setup steps for a future task:

1. Keep all upstream source and JARs outside the release repo.
2. Start the external runtime in a temp or external working directory:

```bash
java -jar /tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar --server.port=6336
```

3. Set `SQLRB_LEARNEDREWRITE_URL` to the local `/rewriter` endpoint without committing it to any env file.
4. Set `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1` only for the explicitly authorized preflight process.
5. Send exactly one synthetic non-benchmark request before any Common-core SQL.
6. Implement or enable the adapter `http` mode only after response shape and schema JSON serialization pass synthetic tests.
