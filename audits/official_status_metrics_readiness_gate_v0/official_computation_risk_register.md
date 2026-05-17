# Official Computation Risk Register

## Risks

- Partial evidence coverage mistaken for method quality: filled rows are uneven across method routes and must not be presented as full-method quality without denominator warnings.
- Inferred_generated mistaken for observed generated: R1 rows must stay labeled as inferred unless separately authorized for official metric input.
- Unresolved rows silently dropped: 288 unresolved rows must remain visible and denominator reduction is forbidden.
- SQLGlot generated/ready gap: SGL011 supports execution/checker evidence but not source-observed generated or ready status.
- Exact/executed semantic confusion: exact must not imply executed unless a separate policy authorizes that inference; current readiness uses observed execution only.
- Dry-run values copied into paper results: v4 outputs are audit-only and cannot be rendered as paper tables.
- Timing metrics accidentally mixed into status-only metrics: timing, latency, speedup, GM_Speedup, and Speedup Ratio Percentiles remain out of scope.
- Global leaderboard temptation: denominator families and method roles must remain separated; no global leaderboard is allowed.

## Mitigations

- Keep official outputs method-aware, engine-aware, pool-aware, and denominator-aware.
- Emit observed and inferred field counts separately.
- Emit unresolved and unknown counts with every official status-only metric table if later authorized.
- Require validation gates before any official metric artifact is created.
