# Official Metric Scope

POCR is proposed as an RQ2 / interpretability / observability metric.

Positive Operation Coverage Rate measures whether a method candidate implements expected rewrite operation atoms defined for a case. It does not measure correctness. It does not measure speed. It does not replace Result Consistency Rate or GM Speedup Ratio.

The metric must be reported beside denominator and lifecycle counts, including generation, execution, exact, and timed rows. A high or low POCR value cannot be interpreted without knowing planned rows, candidate-bound rows, schema-valid annotation rows, fail-closed rows, exact rows, and timed rows.

Promotion into the official paper-facing metric suite is separate from this design audit. This task starts the promotion process, but it does not freeze paper-facing values or authorize result-table updates.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required before an operation atom can enter the implemented set.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
