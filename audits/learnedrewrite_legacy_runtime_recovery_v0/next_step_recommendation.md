# Next Step Recommendation

Verdict: option C.

No configured external LearnedRewrite runtime was available, so LearnedRewrite remains blocked for real Common-core use.

Recommended next setup action:

1. Keep upstream source/JARs outside the release repo.
2. Configure an external runtime URL or command through environment variables only.
3. Use the official HTTP server path first if possible:

```bash
java -jar /tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar --server.port=6336
```

4. Run one synthetic non-benchmark `/rewriter` request using the JSON in `synthetic_preflight_request_safe.json`.
5. Confirm response parsing and single-SQL extraction.
6. Only after that, authorize a 1-2 row PostgreSQL-only LearnedRewrite external-runtime D035 user-facade smoke without DB/checker/timing.

Do not run Track A 120, DB/checker/timing, metrics, or Common-core LearnedRewrite SQL until the synthetic preflight and adapter real-runtime contract are stable.
