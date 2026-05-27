# Risk And Fix Recommendations

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

| Risk | Current evidence status | Recommended fix if needed | Blocker before Track A 120 |
| --- | --- | --- | --- |
| Positive SQL used as atom source | Not observed. Prompt and Stage B treat positive SQL as comparison/reference evidence for declared skills atoms. | Consider a small prompt wording patch from "Optional positive SQL context" to "Optional positive SQL reference evidence, not atom source". | No, if wording is reviewed before expansion. |
| SQLGlot no-op used as reference | Not observed. No-op is represented as `method_id=sqlglot_noop` / control route, and no-op substitute use is explicitly forbidden for optimize. | Keep no-op control review in every pilot audit. | No. |
| Span presence over-accept | Not observed in current PG40 no-op. Stage B maps span-only evidence to presence-only or insufficient evidence. | Continue evidence-ref linting and manual review for any no-op support > 0. | No, unless future no-op support appears. |
| Source-like candidate over-accept | Not observed for SQLGlot no-op PG40; support count is 0. | Manual review any source-like route with transformation-supported atoms. | No for current PG40; yes if future source-like support appears. |
| Prompt ambiguity about positive SQL role | Minor wording boundary: current prompt is substantively correct but "context" could be made more explicit. | Optional narrow prompt wording patch before wider Track A 120 annotation. | Not blocking current PG40 review. |
| Aggregator accidental atom inference | Not observed. Aggregator reads row metrics only. | Keep aggregator input schema tests. | No. |
| PG40 diagnostic values promoted too early | Still a live risk in reporting. Audit wording and project-control boundaries prevent promotion in this task. | Require explicit promotion freeze/gate before paper tables. | Yes: promotion freeze must remain separately authorized. |

Overall verdict: `pass_with_boundary`. No fixes were made in this read-only task.

Required boundary: positive SQL is reference evidence, not an atom source. skills.md is the only operation-atom source. candidate/source/positive span presence alone is not operation support.
