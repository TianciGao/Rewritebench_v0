# SQLGlot Optimize Boundary Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula.

SQLGlot optimize is 34/40 candidate-present for PostgreSQL PG40. The six missing rows are `CONS_0009`, `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`; they remain no-candidate fail-closed rows for POCR@planned and are excluded from POCR@candidate.

No SQLGlot no-op candidate was used as an optimize substitute. Missing optimize candidates should remain visible in future PG40 promotion-pilot tables unless actual optimize candidates are produced in a separate candidate-capture task.

Recommendation: include SQLGlot optimize in future PG40 pilot review only with explicit missing-row fail-closed wording. Do not report it as a complete 40-candidate route.
