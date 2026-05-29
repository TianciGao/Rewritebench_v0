# PG40 Value Interpretation Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

PG40 diagnostic values must be interpreted conservatively.

- Direct LLM original and Direct LLM Repair-1 both reported `POCR@planned=0.395833333333` and `POCR@candidate=0.395833333333`. This equality may reflect reused evidence, identical or similar candidates on many rows, or identical row-level operation support. It must not be over-interpreted as an official metric tie or paper-facing result.
- SQLGlot no-op reported zero for POCR@planned and POCR@candidate. That is a sanity/control pass showing Stage B did not convert source-like/presence evidence into transformation support. It is not reference evidence.
- SQLGlot optimize reported `POCR@planned=0.325000000000` and `POCR@candidate=0.382352941176`. The planned/candidate gap reflects six missing optimize candidates retained fail-closed in POCR@planned and excluded from POCR@candidate.
- PG40 is not Track A 120. PG40 should not be used to claim full Track A behavior.

Verdict: `pass_with_boundary`.

Boundary retained: POCR@planned and POCR@candidate remain D039 promotion views, POCR@curated remains deferred until a predeclared curated manifest exists, and no paper-facing metric is promoted.
