# Verifier Role Boundary

VeriEQL and SQLSolver are verifier/support tools.

They may inspect SQL pairs and produce formal or bounded equivalence verdicts. They do not emit rewritten candidate SQL and must not be treated as user methods or rewrite baselines.

Allowed future role:

- Support Semantic Equivalence Rate when formal verifier evidence exists.
- Provide row-level and pair-level diagnostic evidence for source/candidate, source/positive, source/hard-negative, and future target-engine support pairs.
- Produce tool-specific logs and raw outputs under the local user-run `output/` tree.

Disallowed role:

- No candidate generation.
- No rewrite route ranking.
- No leaderboard participation.
- No same-engine speedup-table membership.
- No official metric input unless separately promoted.
- No replacement of local result consistency checks.

Semantic Equivalence Rate policy:

- `N.A.` when no formal verifier evidence exists.
- Computable only from `semantic_equivalence_summary.json` after verifier output exists.
- Unknown, timeout, unsupported, and tool-error outcomes are reported separately.
