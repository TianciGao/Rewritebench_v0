# Future Checker Normalization Prompt

Task title:
Add explicit opt-in cross-dialect checker normalization for PORT local diagnostics

Purpose:
Implement a narrow checker normalization improvement for local diagnostics only. The prior audit found that controlled PORT cross-dialect mismatches are caused by output column-label differences and decimal-string rendering differences after both MySQL source-reference and PostgreSQL target-candidate execution succeed.

Scope:

- Modify checker behavior only as needed for an explicit opt-in cross-dialect comparison policy.
- Do not change SQL files, manifests, case membership, reports/results, denominators, paper results, raw retained evidence, timing, or leaderboard code.
- Do not compute official metrics.
- Do not treat `pos_01.sql` as a source oracle.
- Do not infer SQL roles from filenames.

Required behavior:

- Add an explicit policy for alias-insensitive or position-based result comparison where case metadata/config authorizes it.
- Add decimal-string normalization or tolerance only under explicit policy.
- Keep current same-engine behavior unchanged unless the same explicit policy is present.
- Preserve fail-closed behavior for missing or malformed checker policy.

Required tests:

- Add focused tests for the four controlled PORT mismatch shapes: column label only and column label plus decimal formatting.
- Add regression tests proving existing PERF, CONS, and LONGTAIL same-engine checker behavior is unaffected.
- Add negative tests showing policy is not applied implicitly from filenames or `pos_01.sql` presence.

Validation boundary:

- Local diagnostic only.
- No official metrics.
- No timing or speedup.
- No reports/results updates.
- No paper tables.
- No global leaderboard.
