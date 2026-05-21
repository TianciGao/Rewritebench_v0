# Denominator Policy

Common-core membership is governed by `case_sets/`, not by scanning `cases/`.

Public v0 denominator facts:

- Common-core v0 = 40 cases.
- Track A same-engine denominator = 120 planned rows.
- The Track A planned rows are case-engine rows, not unique-case counts.

Reporting must keep planned, generated, executed, exact, and timed denominators visible when those quantities apply.

Do not collapse incompatible denominators. Role-specific, engine-specific, route-specific, and timing-eligible denominators must remain distinguishable.

User-entry local diagnostics under `runs/user/...` do not change denominator membership and do not create official metric inputs unless a separate policy explicitly authorizes that promotion.

Denominator changes require separate maintainer approval and must update the governed `case_sets/` artifacts, not inferred directory state.
