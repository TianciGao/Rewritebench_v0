# Macro Versus Micro Warning

Macro-average over per-row OC_i is the D039 formula.

The D039 proposal computes `OC_i = |Ahat_i| / |Aexp_i|` for each row, then averages `OC_i` across the selected denominator rows.

Total supported atoms divided by total expected atoms is a micro-average diagnostic only. It is included in `route_level_dry_run_summary.csv` only under the explicitly labeled field `diagnostic_micro_average_supported_over_expected`.

Do not replace macro-average with total supported atoms divided by total expected atoms. The micro-average must not be presented as the current paper formula, an official route-level score, or an official POCR value.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
