# metric_input_authorization_overlay_v0 Next Steps

## Option A: Status-only Metrics Dry-run Plan

Prepare a dry-run plan from the 130 authorized rows without computing metrics. The plan must explicitly handle partial denominator coverage and must not produce paper results or rates.

## Option B: Manual Overlap Review

Review the 45 denied `needs_source_overlap_review` rows. Define source precedence before any future authorization.

## Option C: Unresolved-row Evidence Triage

Continue row-level non-timing evidence triage for the 425 unresolved rows. These rows remain unauthorized until a separately approved parser fills them and they pass readiness review.

## Option D: Timing Adapter Planning

Defer candidate metrics and plan timing separately. Timing fields and speedup fields remain unauthorized by this overlay.

## Recommendation

Do not compute metrics yet. First perform manual overlap review for the 45 denied rows or prepare a status-only metrics dry-run plan that explicitly handles partial denominator coverage. Keep timing adapter work separate.
