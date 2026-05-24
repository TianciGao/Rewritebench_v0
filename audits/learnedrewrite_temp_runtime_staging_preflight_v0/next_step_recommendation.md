# Next Step Recommendation

The temp-only runtime staging fix resolved the prior
`rules_for_selected/standard.txt` blocker for a synthetic non-benchmark request.

Recommended next safe action:

1. Authorize a narrow LearnedRewrite adapter HTTP-mode implementation.
2. Keep runtime execution gated by `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`.
3. Serialize schema JSON in the shape accepted by the runtime.
4. Extract only `data.rewritten_sql` and enforce single-SQL fail-closed policy.
5. Run a 1-2 row PostgreSQL-only LearnedRewrite external-runtime user-facade
   smoke without DB/checker/timing.

Do not run Common-core, Track A 120, DB/checker/timing, local metrics, verifier,
official metrics, paper rendering, or retained-evidence promotion until the
adapter HTTP hook and bounded user-facade smoke are stable.
