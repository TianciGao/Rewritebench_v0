# Local Metric Interpretation

This packet reports local diagnostic speedup summaries over exact-timed rows only.

Allowed interpretation:

- 66 exact/result-consistent rows were timed.
- There were no timing failures.
- The diagnostic GM speedup over the 66 exact-timed rows is 1.022011.
- Engine speedups are computed over each engine's own exact-timed denominator.
- The 54 non-exact/frontier rows remain visible and must not be treated as timed failures or silently excluded from denominator-aware route-card coverage.

Forbidden interpretation:

- Do not call this official Track A performance.
- Do not compute formal Regression@20 from this packet.
- Do not compute POCR.
- Do not compute official Semantic Equivalence Rate.
- Do not create a leaderboard ranking.
- Do not update paper tables or top-level `reports/` or `results/`.

The correct next aggregation is a local diagnostic route-card projection that combines the execution/checker denominator chain with this exact-gated timing packet.
