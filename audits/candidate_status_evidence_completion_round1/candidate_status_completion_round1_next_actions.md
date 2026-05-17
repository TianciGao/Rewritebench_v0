# Candidate Status Completion Round 1 Next Actions

## Option A: Approve Overlap Priority Policy And Create Metric-Input Overlay V1

This would unblock some or all 45 denied overlap rows by applying a maintainer-approved source-priority rule. It should create a separate overlay and not rewrite parser-v1 output.

## Option B: Approve SQLGlot Parser Manifest And Implement SQLGlot Non-Timing Parser V1

This should wait until row grain, route mapping, duplicate-source handling, and sanitized column scope are approved. Direct parser approval from raw mixed-scope sources is not recommended yet.

## Option C: Create Sanitized Non-Timing Projection For SQLGlot Sources Before Parser

This is the most efficient SQLGlot next step. It can strip timing, speedup, stdout/stderr, and raw path payload columns while preserving only row keys and approved non-timing status fields for maintainer review.

## Option D: Stop Status Completion And Move To Timing Adapter Planning

This is possible but premature if the goal is to improve status-only denominator coverage. Timing should remain a separate adapter line.

## Recommendation

Do Option A first if the maintainer wants immediate progress on already-filled rows, then Option C for SQLGlot. Do not compute metrics, authorize SQLGlot parser use, or update reports/results until those next tasks are separately approved.
