# Non-Promotion Boundary

Current SQLSolver and VeriEQL diagnostics must not be promoted now.

Reasons:

- They were audit/local diagnostic runs, not canonical user-facing reruns.
- Runtime files were intentionally written under `/tmp/...`.
- Output summaries were intended as readiness/coverage diagnostics.
- Paper-facing authorization has not been granted.
- Identity guard and coverage caveats must be visible in any future output.

Allowed use of current diagnostics:

- readiness evidence;
- support coverage comparison;
- blocker triage;
- input to future contract and policy design.

Disallowed use:

- official Semantic Equivalence Rate;
- paper table input;
- retained evidence promotion;
- leaderboard or method ranking;
- replacement for a future user-facing rerun.
