# Final Values Boundary Note

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

Micro-average is diagnostic only and not the paper formula.

## Diagnostic Values

### Direct LLM original
- `postgres`: POCR@planned `0.412500000000`, POCR@candidate `0.412500000000`.
- `mysql`: POCR@planned `0.429166666667`, POCR@candidate `0.429166666667`.
- `spark`: POCR@planned `0.433333333333`, POCR@candidate `0.433333333333`.
- `overall`: POCR@planned `0.425000000000`, POCR@candidate `0.425000000000`.

### Direct LLM Repair-1
- `postgres`: POCR@planned `0.395833333333`, POCR@candidate `0.395833333333`.
- `mysql`: POCR@planned `0.350000000000`, POCR@candidate `0.350000000000`.
- `spark`: POCR@planned `0.420833333333`, POCR@candidate `0.420833333333`.
- `overall`: POCR@planned `0.388888888889`, POCR@candidate `0.388888888889`.

### SQLGlot no-op
- `postgres`: POCR@planned `0.000000000000`, POCR@candidate `0.000000000000`.
- `mysql`: POCR@planned `0.000000000000`, POCR@candidate `0.000000000000`.
- `spark`: POCR@planned `0.000000000000`, POCR@candidate `0.000000000000`.
- `overall`: POCR@planned `0.000000000000`, POCR@candidate `0.000000000000`.

### SQLGlot optimize
- `postgres`: POCR@planned `0.358333333333`, POCR@candidate `0.421568627451`.
- `mysql`: POCR@planned `0.275000000000`, POCR@candidate `0.343750000000`.
- `spark`: POCR@planned `0.358333333333`, POCR@candidate `0.367521367521`.
- `overall`: POCR@planned `0.330555555556`, POCR@candidate `0.377777777778`.

Interpretation:
- POCR@planned includes planned denominator rows with fail-closed zero contribution where applicable.
- POCR@candidate is the candidate-bound diagnostic view.
- SQLGlot no-op zero is sanity/control evidence, not reference evidence.
- SQLGlot optimize planned/candidate gap is driven by missing candidate rows retained fail-closed in POCR@planned.
- These values are not official POCR, not a paper metric, and not a global leaderboard.
