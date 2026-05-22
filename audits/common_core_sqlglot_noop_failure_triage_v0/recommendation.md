# Recommendation

Keep the SQLGlot noop failures fail-visible. Do not patch benchmark code or silently reinterpret these rows.

Recommended next actions, if separately authorized:

1. SQLGlot noop PORT limitation documentation or route design:
   - Covers PostgreSQL PORT parse failures and MySQL/Spark PORT literalized-identifier behavior.
   - Must stay separate from controlled target-reference diagnostics.
   - A target-aware SQLGlot route would be a new route/design, not a silent change to `--route noop`.

2. Narrow checker column-label policy triage:
   - Covers `PERF_0062` and same-engine PORT rows where values match positionally but expression labels differ.
   - Must explicitly decide whether same-engine expression label differences are meaningful for each affected case class.
   - Must include PERF/CONS/LONGTAIL and PORT regression checks before any behavior change.

3. Spark statement/preflight-backend investigation:
   - Covers same-engine Spark rows rejected as `Spark diagnostic query must contain exactly one statement`.
   - Should inspect the interaction between SQLGlot-emitted block comments, candidate preflight, and Spark execution query splitting.
   - Must not change SQL files, case membership, denominators, paper results, reports/results, retained evidence, metrics, timing, or leaderboard behavior.

No source execution issue was found in the fail-visible rows. Candidate preflight failed in zero inspected rows; where preflight may be incomplete, the evidence points to Spark candidate execution after preflight passed.
