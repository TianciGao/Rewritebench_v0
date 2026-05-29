# Value Comparison

The smoke ran the implemented row-metrics exporter on existing replay `diagnostic_rows.csv` artifacts and then ran the implemented aggregator on the resulting local `/tmp` row-metrics CSVs.

Repair-1 should reproduce `0.395833333333` for both POCR@planned and POCR@candidate. The aggregator output reproduced both values exactly. The diagnostic micro-average also reproduced `0.383177570093`.

SQLGlot no-op should reproduce `0.000000000000` for both POCR@planned and POCR@candidate. The aggregator output reproduced both values exactly. The diagnostic micro-average also reproduced `0.000000000000`.

Micro-average is diagnostic only and not the paper formula.

POCR@curated remains NA / curated_manifest_missing.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.
