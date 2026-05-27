# Risk Register

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

| risk | severity | mitigation | blocker status |
| --- | --- | --- | --- |
| remaining fail-closed rows | medium | Keep all 36 rows explicit; do not drop or infer support; document 20 schema-invalid, 15 no-candidate, and one route mismatch. | not_blocking_with_boundary |
| one route mismatch | medium | Keep fail-closed; document nested route-id typo; consider tiny fix/retry before final freeze. | not_blocking_with_boundary |
| no-op over-accept risk | low | Supported operation atoms remain zero; keep manual-review gate if any future no-op support appears. | not_blocking |
| SQLGlot optimize missing rows | medium | Retain 15 missing rows fail-closed for POCR@planned; no no-op substitutions. | not_blocking_with_boundary |
| manual Stage B subjectivity | medium | Use Stage B transformation evidence policy and do not override row scores in this review. | not_blocking_with_boundary |
| premature paper promotion | high | Prepare review packet only; do not update reports/results or promote metrics without separate authorization. | blocking_if_violated |
