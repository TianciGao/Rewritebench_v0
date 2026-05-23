# Synthetic Pair Definitions

Runtime input directory:

```text
/tmp/sqlrb_verieql_synthetic_decidable_smoke_v0/input/
```

Pair 1:

- `pair_id`: `synthetic_select1_equivalent`
- `pair_type`: `support_pair_smoke`
- Source SQL: `SELECT 1`
- Candidate SQL: `SELECT 1`
- Expected high-level intent: equivalent
- Result: unsupported by VeriEQL because query has no `FROM` clause

Pair 2:

- `pair_id`: `synthetic_select1_nonequivalent`
- `pair_type`: `support_pair_smoke`
- Source SQL: `SELECT 1`
- Candidate SQL: `SELECT 2`
- Expected high-level intent: non-equivalent
- Result: unsupported by VeriEQL because query has no `FROM` clause

Why pair 2 was run:

- The task allowed pair 2 if safe to run together.
- Both rows were temp-only `support_pair_smoke` rows with no case package, no database, no Common-core membership, and no repository output surface.
- Running both together avoided interpreting one unsupported singleton as a selective failure.

Boundary flags on pair records:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
