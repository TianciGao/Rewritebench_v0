# Decisions Needed Before Implementation

Maintainer/team checklist:

- Keep Regression@20 unchanged, modify it, supplement it, or mark it diagnostic-only?
- Add quartile/distribution performance summaries?
- Define parseability, SQL extractability, and runnable SQL separately?
- Define PlanAvailability versus PlanFrontier split?
- Approve failure bucket taxonomy?
- Define user submission `candidate_id` format?
- Decide retained LLM evidence scope: frozen-only or rerunnable?
- Decide timing-missing policy?
- Decide unsupported policy?
- Decide preflight-blocked policy?
- Decide whether `ValidRewriteYield` is retained, renamed, merged into another metric, or dropped?
- Decide exact public table names?
- Confirm whether result consistency is separate from Exact@planned?
- Confirm whether verifier support is evidence-only or has a support-rate metric?
- Confirm output root and run manifest requirements for future user runs?

No implementation should start until these decisions are recorded in an approved metrics contract or follow-up decision log entry.
