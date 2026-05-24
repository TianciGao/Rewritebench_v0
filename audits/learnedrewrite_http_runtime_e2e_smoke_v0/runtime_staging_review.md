# Runtime Staging Review

External runtime candidate:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

Required external asset:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rules_for_selected/
```

Temp staging directory:

```text
/tmp/sqlrb_learnedrewrite_http_runtime_e2e_smoke_v0/runtime_staging/
```

Staging used:

- copied `rules_for_selected/` into the temp workdir only;
- started the external JAR by absolute path from the temp workdir;
- used local port `6336`;
- shut down the runtime after the smoke.

No JAR, source file, dependency JAR, runtime asset, request log, or generated
output was copied into the release repo.

Runtime shutdown check passed: after the smoke, no `rewriter_java.jar` process
and no listener on port `6336` remained.
