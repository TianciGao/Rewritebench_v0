# Recommendation

Keep the six rows fail-visible for the current SQLGlot noop snapshot. Do not patch code in this audit task.

Recommended next action, if separately authorized: implement a narrow Spark local diagnostic statement-boundary repair so the Spark executor ignores semicolons inside SQL comments and string literals consistently with candidate preflight. The work should also consider moving or sharing the statement-boundary logic so preflight and backend execution cannot disagree on this class of candidate.

Required guardrails for any future patch:

- Do not change SQLGlot noop behavior.
- Do not modify case SQL, manifests, schemas, or checker configs.
- Do not relax candidate safety for genuine multi-statement SQL.
- Preserve fail-closed behavior for unsupported Spark PORT roles.
- Include regression coverage for block comments with semicolons, trailing semicolon handling, string literals with semicolons, and genuine multi-statement rejection.
- Recheck the six affected Spark same-engine rows or equivalent fixtures.
- Recheck a small Spark same-engine smoke and existing PORT fail-closed behavior.
- Do not compute official metrics, timing/speedup, reports/results, paper outputs, retained evidence promotion, or leaderboard output.

This appears to be a local diagnostic infrastructure gap between preflight and the Spark backend splitter, not a true SQLGlot multi-statement emission and not a Spark parser limitation.
