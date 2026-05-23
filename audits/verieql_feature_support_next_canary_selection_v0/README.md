# VeriEQL Feature Support Next Canary Selection v0

Task: `verieql_feature_support_next_canary_selection_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: `next_canary_selected_no_verifier_run`

This audit reviewed the bounded `CONS_0007` VeriEQL canary result, inspected VeriEQL feature-support clues, statically scanned Common-core `source_vs_positive` pairs, and selected the next safest bounded VeriEQL canary candidate.

No new VeriEQL run was performed. No SQLSolver run was performed. No Semantic Equivalence Rate, official metric, report/result, retained evidence, or leaderboard output was created.

Primary recommendation:

- Next one-pair canary: `PERF_0062 source_vs_positive pos_01`.
- Reason: it is the lowest-risk Common-core pair found by static scan, with one `SELECT` per side, no `EXISTS`, no nested `SELECT`, no window function, no date/interval feature, no outer join, and no set operation.
- Expected outcome: unknown until a real bounded run is separately authorized; the syntax should at least avoid the confirmed `EXISTS` blocker.

Fallbacks:

- `PORT_0024 source_vs_positive pos_01` if a compact aggregate/CASE pair is desired and PORT role caveats are acceptable.
- `CONS_0036 source_vs_positive pos_01` only if a CONS-only canary is required; it is higher risk because the positive contains a nested `SELECT`.

Files:

- `verieql_feature_support_notes.md`
- `cons0007_unsupported_review.md`
- `candidate_pair_scan.csv`
- `next_canary_recommendation.md`
- `command_log.md`
- `protected_surface_check.md`
- `boundary_checklist.md`
