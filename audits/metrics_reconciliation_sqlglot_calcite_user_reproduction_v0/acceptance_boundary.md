# Acceptance Boundary

These are local diagnostic metrics only. This audit does not update paper-facing tables, promote official metrics, create a leaderboard, compute official Positive Operation Coverage Rate, generate POCR annotation JSONL, or run POCR Stage B validation.

Performance remains exact+timed only. If discrepancies remain, the new user-side reproduction should be treated as pipeline smoke/local diagnostic evidence, not replacement evidence.

Reconciled SQLGlot counts and failure buckets support accepting the new SQLGlot user-side outputs as local diagnostic reproduction evidence with boundary. The SQLGlot GM differences remain expected rerun/provenance differences and should not replace canonical paper-facing or route evidence values unless a separate metric-promotion task authorizes replacement.

The Calcite new reproduction is blocked by missing runtime env and should be treated as blocked-runtime smoke/local diagnostic only.

Paper-facing table update authorized: no. Official metric promotion authorized: no. Leaderboard output authorized: no.
