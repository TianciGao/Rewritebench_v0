# No-Op Control Review

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

SQLGlot no-op remains a candidate/control route, not a reference.

SQLGlot no-op remains a candidate/control route, not a reference.

## Supported Atoms By Engine

- `mysql`: supported operation atoms `0`, schema-valid rows `40`, fail-closed rows `0`, presence-only atoms `18`, insufficient-evidence atoms `89`.
- `postgres`: supported operation atoms `0`, schema-valid rows `37`, fail-closed rows `3`, presence-only atoms `15`, insufficient-evidence atoms `83`.
- `spark`: supported operation atoms `0`, schema-valid rows `40`, fail-closed rows `0`, presence-only atoms `19`, insufficient-evidence atoms `88`.

Possible over-accept cases: `0`.

Manual review requirement: not required for no-op over-accept, because transformation-supported operation atoms remain zero. Remaining fail-closed no-op rows, where present, are retained as diagnostic boundary rows.

Conclusion: SQLGlot no-op remains safe as a Stage B over-accept guard for this promotion review packet.
