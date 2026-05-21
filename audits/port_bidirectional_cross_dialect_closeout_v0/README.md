# PORT Bidirectional Cross-Dialect Closeout v0

Verdict: `closed_for_current_user_entry_phase`.

This audit closes the bidirectional PORT cross-dialect local diagnostic subphase for the current user-entry phase. It summarizes the manifest role mapping, runner consumption, controlled forward route, controlled reverse route, checker-normalization boundary, same-engine protection, and remaining deferred work.

This closeout is local diagnostic only. It is not official metrics, not paper reproduction, not timing or speedup, not reports/results migration, not retained-evidence promotion, not a leaderboard input, and not a release tag or export branch.

## Completed Status

- All 9 Common-core PORT cases have `local_diagnostic.schema_version: port_target_engine_diagnostic_v0` with explicit target-engine-aware `engine_roles`.
- The metadata distinguishes target engine roles instead of relying on case-level guessing.
- The resolver and runner consume selected-engine role metadata.
- The runner does not infer source, target, or reference roles from filenames, SQL text, or pool name alone.
- The runner avoids sending MySQL-like `source.sql` directly to PostgreSQL for the forward cross-dialect route.
- The runner avoids sending PostgreSQL-like `source.sql` directly to MySQL for the reverse cross-dialect route.
- Forward route validated: MySQL source-reference to PostgreSQL target-candidate for `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`, controlled exact 5/5.
- Reverse route validated: PostgreSQL source-reference to MySQL target-candidate for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`, controlled exact 4/4.
- Opt-in cross-dialect checker normalization remains gated to cross-dialect local diagnostics.
- Same-engine defaults remain protected for PERF, CONS, LONGTAIL, and same-engine PORT routes.

## Remaining Deferred Work

Real user adapter evaluation for PORT remains future work. The no-op adapter is not a PORT target candidate for cross-dialect exactness. The controlled target-reference adapters are diagnostic adapters, not benchmark baselines. Spark live execution, timing/speedup, official metrics, paper rendering, reports/results migration, retained evidence integration, release tag/export branch creation, and any leaderboard remain deferred.

## Recommendation

Close this PORT cross-dialect local diagnostic subphase for the current user-entry phase and return to the main user-entry roadmap. Any real PORT user-adapter evaluation or additional engine work should be separately authorized under the same local-only boundaries.
