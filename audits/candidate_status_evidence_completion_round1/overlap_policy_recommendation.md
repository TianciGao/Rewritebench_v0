# Overlap Policy Recommendation

## Purpose

The 45 overlap rows are filled candidate-status rows that remain unauthorized only because multiple approved parser-v1 sources contributed to the same scaffold row. This file proposes a future policy. It does not authorize those rows.

## Option A: Keep All 45 Overlap Rows Unauthorized

This is the safest no-op option. It preserves current authorization boundaries and avoids any source-precedence mistake, but leaves known row-level non-timing evidence blocked.

## Option B: Approve P001 Generation/Readiness + P002 Candidate Status With P003 Failure-Enrichment Only

This is the recommended next policy.

- P001 supplies Direct-LLM generation/readiness evidence for original rows.
- P002 supplies original/repair candidate status, including observed generated/ready/executed/exact/result status where present.
- P003 supplies Repair-1 failure-stage/failure-type enrichment only.
- P003 must not override P002 success or exactness.
- Timing, speedup, plan, paper, and reports/results fields remain blocked.

## Option C: Approve P002 As Primary Status And Ignore P003 Unless Failure Fields Are Missing

This is close to Option B but slightly less explicit about P001 generation/readiness. It may be acceptable if the maintainer wants a single primary candidate-set source for most status fields.

## Option D: Require Row-By-Row Manual Review

This is the most conservative substantive option. It minimizes policy risk but is slower and may add review burden without materially changing the source-overlap pattern.

## Recommendation

Choose Option B in a separately authorized task. It matches the observed overlap split: 26 `P001|P002` Direct-LLM original rows and 19 `P002|P003` Repair-1 rows. The future task should create a new overlay only; it should not rewrite parser-v1 output or compute metrics.
