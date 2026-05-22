# Recommendation

Close the current Common-core SQLGlot noop local diagnostic sequence as `closed_with_fail_visible_limitations`.

Recommended next safe actions, each requiring separate authorization:

1. MySQL label-policy triage:
   - Start with `PERF_0062`.
   - Include related MySQL rows where values matched positionally but generated expression labels differed: `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024`.
   - Do not relax checker behavior globally.
   - Require representative PERF/CONS/LONGTAIL and PORT regression checks before any behavior change.

2. SQLGlot noop PORT limitation documentation:
   - Document PostgreSQL PORT parse/emit failures.
   - Document MySQL/Spark PORT literalized identifier and target-semantics limitations.
   - Keep real user-adapter rows separate from controlled target-reference PORT diagnostics.

3. Target-aware SQLGlot route design:
   - If changing PORT behavior is desired, create a separately named route.
   - Do not silently change `--route noop`.
   - Treat target-aware semantics as a new local diagnostic route with separate comparability boundaries.

Pausing the SQLGlot line is also valid. The current fail-visible closeout is sufficient for the local diagnostic phase and should not be interpreted as official retained SQLGlot baseline evidence.
