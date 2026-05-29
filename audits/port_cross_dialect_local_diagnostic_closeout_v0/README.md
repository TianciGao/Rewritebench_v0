# PORT Cross-Dialect Local Diagnostic Closeout v0

Verdict: `closed_for_current_user_entry_phase`.

This packet closes the PORT cross-dialect local diagnostic path for the current user-entry phase. The closeout is audit-only: it does not modify checker behavior, runner/source code, manifests, SQL, schemas, checker configs, case sets, reports/results, denominators, paper results, retained evidence, tags, or branches.

## Completed Milestones

- PORT PostgreSQL source-execution failure triage identified five MySQL-like source SQL failures as cross-dialect diagnostic gaps, not schema or method-quality failures.
- All 9 Common-core PORT manifests now carry explicit `local_diagnostic` metadata.
- Same-engine PORT cases are `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`.
- Cross-dialect reference PORT cases are `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- The five originally failing PostgreSQL source-execution cases now have explicit source-reference and target-candidate roles.
- The resolver and runner consume `diagnostic_mode` and avoid executing MySQL-like `source.sql` directly in PostgreSQL for declared cross-dialect rows.
- MySQL source-reference execution works in live local diagnostic mode for the five cross-dialect rows: 5/5 executable.
- The controlled PostgreSQL target-reference adapter validates target-candidate execution for the same five rows: 5/5 executable.
- Local checker handoff works for MySQL source-reference result artifacts to PostgreSQL target-candidate artifacts.
- Opt-in cross-dialect checker normalization is gated to `local_diagnostic.diagnostic_mode == cross_dialect_reference` and `local_diagnostic.checker.comparison == source_reference_result_to_target_candidate_result`.
- The normalized controlled rerun reached exact 5/5.
- Same-engine defaults remain protected; PERF, CONS, LONGTAIL, and same-engine PORT rows are not forced into cross-dialect positional comparison.

## Closeout Answers

- All 9 Common-core PORT manifests covered by explicit `local_diagnostic` metadata: yes.
- Same-engine PORT cases: `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`.
- Cross-dialect reference PORT cases: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`.
- Five originally failing PostgreSQL source-execution rows now have explicit roles: yes.
- Runner consumes `diagnostic_mode`: yes.
- Runner avoids PostgreSQL execution of MySQL-like `source.sql` for cross-dialect cases: yes.
- MySQL source-reference live local diagnostic works: yes, 5/5 executable.
- PostgreSQL target-candidate controlled diagnostic works: yes, 5/5 executable.
- Checker normalization reaches exact 5/5 in the controlled diagnostic: yes.
- Opt-in checker normalization is gated to cross-dialect local diagnostics: yes.
- Same-engine defaults preserved: yes.
- PERF / CONS / LONGTAIL protected: yes.

## Remaining Deferred Work

The closeout does not authorize or perform broader evaluation work. Real user PORT adapter evaluation remains future work. The no-op adapter is not a PORT target candidate. Spark live execution, timing/speedup, official metrics, paper rendering, reports/results migration, retained evidence integration, release tag/export branch creation, and any leaderboard remain deferred.

## Boundary

This is local diagnostic only. The normalized exact 5/5 controlled run is not an official metric, not paper reproduction, not a timing/speedup result, not a reports/results update, not retained evidence promotion, and not a leaderboard input.

## Recommended Next Safe Action

Close this PORT local diagnostic subphase and return to the main user-entry roadmap. Any future MySQL same-engine backend or real PORT user-adapter evaluation should be separately authorized under the same local-only boundaries.
