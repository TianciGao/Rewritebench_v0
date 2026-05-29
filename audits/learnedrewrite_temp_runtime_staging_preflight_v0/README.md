# LearnedRewrite Temp Runtime Staging Preflight

This packet records a temp-only runtime asset staging fix for the LearnedRewrite
synthetic preflight blocker observed in
`audits/learnedrewrite_external_runtime_synthetic_preflight_v0/`.

The external runtime candidate was:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

The missing relative asset `rules_for_selected/standard.txt` was found under
the external source tree. To avoid modifying the external source root, only the
`rules_for_selected/` support directory was copied into a temporary runtime
workdir under `/tmp/sqlrb_learnedrewrite_runtime_staging_v0/`. No runtime asset
was copied into the release repo.

Exactly one synthetic non-benchmark `POST /rewriter` request was sent. It used
an artificial `tiny_orders` SQL/schema fixture, not Common-core SQL or schema.
The runtime returned HTTP 200 parseable JSON with `status=true`,
`message=SUCCESS`, and `data.rewritten_sql`.

Result:

- temp staging used: yes
- runtime started: yes
- synthetic preflight attempted: yes, exactly one POST
- single SQL extractable: yes
- benchmark evidence produced: no
- metrics computed: no

Next safe action: authorize a narrow LearnedRewrite HTTP-runtime adapter
implementation and then a 1-2 row PostgreSQL-only external-runtime user-facade
smoke without DB/checker/timing. Do not run Common-core or Track A 120 yet.
