# Repair-1 And No-Op Dry-Run Lessons

Repair-1 PostgreSQL PG40 dry-run:

- planned rows: 40
- candidate-bound rows: 40
- schema-valid rows: 40
- fail-closed rows: 0
- expected operation atoms: 107
- Stage-B-supported operation atoms: 41
- POCR@planned macro dry-run: `0.395833333333`
- POCR@candidate macro dry-run: `0.395833333333`
- diagnostic micro-average: `0.383177570093`

SQLGlot no-op PostgreSQL PG40 dry-run:

- planned rows: 40
- candidate-bound rows: 40
- schema-valid rows: 34
- fail-closed rows: 6
- expected operation atoms: 107
- Stage-B-supported operation atoms: 0
- POCR@planned macro dry-run: `0.000000000000`
- POCR@candidate macro dry-run: `0.000000000000`
- diagnostic micro-average: `0.000000000000`

Macro and micro differed for Repair-1 because row-level expected atom counts vary across cases. This confirms that aggregate totals are not a substitute for D039 macro-average.

The no-op control value of zero supports the conservative Stage B boundary: source-like span presence was not promoted to transformation support.

These lessons support implementing a reusable aggregator after this row-level contract is accepted.

Macro-average over per-row OC_i is required. Total supported atoms divided by total expected atoms is diagnostic micro-average only.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
