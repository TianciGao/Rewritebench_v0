# Speedup Diagnostic Comparison

Speedup diagnostics are computed only within each route's exact-timed
denominator.

| speedup field | SQLGlot noop, 35 timed exact rows | Calcite HEP fail-closed, 22 timed exact rows |
| --- | ---: | ---: |
| diagnostic GM speedup | 0.995912 | 1.009852 |
| P10 | 0.988128 | 0.981979 |
| P25 | 0.995110 | 0.989623 |
| P50 / median | 1.002522 | 0.995700 |
| P75 | 1.009285 | 1.005620 |
| P90 | 1.016506 | 1.008519 |

Boundary:

- Do not compare GM speedup as a global rank because the timed exact denominators differ.
- Do not call either route a winner.
- Do not compute formal Regression@20.
- These are local diagnostic speedup summaries only.
