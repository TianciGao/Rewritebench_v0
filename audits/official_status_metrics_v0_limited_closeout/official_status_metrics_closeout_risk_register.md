# Official Status Metrics Closeout Risk Register

## Limited Official Metrics Mistaken For Full Benchmark Results

Mitigation: label outputs as limited official status metrics and keep Generation Rate blocked.

## Dry-run Values Copied Into Paper Tables

Mitigation: future renderers must read only authorized official outputs and must not ingest dry-run values without explicit approval.

## Blocked Generation Rate Hidden

Mitigation: render Generation Rate as blocked with the blocker reason, not as blank, zero, or omitted.

## Unresolved Rows Hidden

Mitigation: show planned denominator, authorized inputs, and unresolved/unauthorized rows in any future table.

## Denominator Reduction

Mitigation: denominator reduction remains forbidden; planned denominator rows remain visible.

## Global Leaderboard Pressure

Mitigation: enforce Metrics Contract v1 and D009; no global leaderboard or winner language.

## Timing/Performance Accidental Mixing

Mitigation: reject GM_Speedup, Speedup Ratio Percentiles, latency, speedup, and timing fields in status-only renderer scope.

## Reports/Results Mutation Risk

Mitigation: keep future renderer output paths explicit and separately authorized; this closeout writes only under `audits/`.
