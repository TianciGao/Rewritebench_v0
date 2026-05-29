# verieql_exact_candidate_tiny_local_pass_v0

Task mode: local-only verifier-support pass.

This packet records a tiny VeriEQL finite-bound pass over exact/result-consistent real baseline candidate rows from the existing local diagnostic run `runs/user/common_core_pg_noop_db_checker`.

Scope:
- Tool: VeriEQL only.
- Source run: existing PostgreSQL SQLGlot noop local diagnostic run.
- Selected rows: `CONS_0036`, `PERF_0077`, `PERF_0082`.
- Pair type: source vs method candidate.
- Verifier mode: finite bound.
- Bound size: 10.
- Timeout: 30 seconds.
- Runtime output root: `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/output/`.

Result:
- Selected candidate rows: 3.
- Exact-gated rows: 3.
- Verifier attempted rows: 3.
- Equivalent: 1.
- Non-equivalent: 0.
- Not implemented: 2.
- Decidable count: 1.
- Local tiny diagnostic semantic equivalence rate: 1.0 over the one decidable row.
- Verifier decidability rate: 1/3.

Boundary:
- This is not official Semantic Equivalence Rate.
- This is not official metrics.
- This is not paper evidence.
- This is not retained evidence.
- This is not leaderboard input.
- Local result checker exactness was used only as an eligibility gate, not as verifier equivalence evidence.

