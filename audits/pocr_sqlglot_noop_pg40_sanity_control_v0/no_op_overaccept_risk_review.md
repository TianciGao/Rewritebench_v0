# No-Op Over-Accept Risk Review

SQLGlot no-op is a sanity/control route for source-like or low-transform candidates. It should not receive transformation-supported operation atoms merely because source-like spans are present in candidate SQL.

Observed diagnostic replay totals:

- transformation-supported operation atoms: 0
- presence-only operation atoms: 15
- insufficient-transformation-evidence operation atoms: 75
- rejected-noop-equivalent operation atoms: 0
- possible over-accept cases: 0

Finding: Stage B remained conservative for this no-op control run. No transformation-supported operation atom was emitted. Presence-only and insufficient-evidence outcomes remain diagnostic evidence that Stage A can cite spans without Stage B counting them as transformation support.

The remaining quality boundary is annotation robustness: 6 rows failed closed as schema-invalid at replay time because Stage A output was malformed or provider-failed. Those rows should remain visible and can be retried later only under an explicit targeted retry task.

This is not official POCR.
No route-level POCR score is emitted.
No paper-facing metric is promoted.
Stage A annotation alone is not counted.
Stage B transformation-aware validation is diagnostic only.
Semantic guard atoms are not part of operation coverage numerator.
No global leaderboard is produced.
