# LearnedRewrite Legacy Runtime Recovery

This packet recovers LearnedRewrite runtime setup clues from the legacy local repo, prior audit notes, the official upstream source clone, and official documentation.

## Findings

- The legacy release-like repo contains LearnedRewrite preflight and bounded-evidence notes, not a checked-in runnable LearnedRewrite JAR.
- Legacy notes recover an embedded LLM4Rewrite/JPype path and an old future command shape, but that path depends on external `/tmp` artifacts, JPype, Java classpath recovery, and PostgreSQL assumptions.
- The official upstream docs recover a cleaner HTTP runtime shape: `java -jar rewriter_java.jar --server.port=6336`, with `POST /rewriter` accepting SQL plus schema.
- A local external JAR candidate exists at `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar`, outside the release repo.
- No `SQLRB_LEARNEDREWRITE_CMD` or `SQLRB_LEARNEDREWRITE_URL` was configured, and port `6336` was not listening.
- No synthetic preflight was attempted.

## Boundary

No Common-core SQL was sent to a real runtime. No LearnedRewrite benchmark run, DB/checker/timing, local metrics, verifier, LLM call, paper rendering, retained-evidence promotion, or leaderboard generation occurred. No upstream or legacy source/JAR/dependency artifact was copied into the release repo.

Old LearnedRewrite results remain legacy facts only and were not copied as new metrics.

## Next Safe Action

Configure an external LearnedRewrite runtime outside the release repo, then run exactly one synthetic non-benchmark preflight request. If that succeeds, authorize a 1-2 row PostgreSQL-only D035 user-facade smoke without DB/checker/timing.
