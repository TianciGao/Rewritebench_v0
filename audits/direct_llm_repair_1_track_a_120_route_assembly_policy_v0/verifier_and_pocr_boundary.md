# Verifier And POCR Boundary

SQLSolver remains coverage-limited verifier support.

The current SQLSolver boundary is:

- same-8 identity guards passed 2/8;
- explicit `no_verifier_support` rows were 3/8;
- residual unclassified identity blockers were 3/8;
- actual source-candidate checks were equivalent 2/2 attempted; and
- `ready_for_sqlglot_noop_pg_35=false`.

This coverage limit does not block the Repair-1 local diagnostic route because verifier limitations are support-tool limitations, not rewrite-method failures.

SER policy:

- No official SER is produced by route assembly.
- SER remains `N.A.` when no formal verifier evidence is included.
- SER may be reported as `coverage_limited` only when bounded formal verifier-support evidence is included and clearly labeled.
- Local result-checker exactness is not SER evidence.
- `no_verifier_support`, `unsupported`, `unknown`, `timeout`, and `tool_error` verifier outcomes are excluded from decidable SER denominators and reported separately.

POCR policy:

- POCR remains deferred.
- No operation atoms are inferred in this task.
- `tag_slices` are not POCR.
- failure buckets are not POCR.
- plan deltas are not POCR unless a future operation-atom evidence contract explicitly authorizes them.

Failure buckets and tag slices remain diagnostic/support outputs only. They are not primary metrics, ranking scores, or leaderboard inputs.
