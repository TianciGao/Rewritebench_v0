# Performance Metric Options

This file compares performance regression reporting choices. It does not finalize a choice and does not compute metrics.

## Option A: Keep Regression@20 As-is

Pros:

- Preserves continuity with prior paper-facing language.
- Simple threshold-style interpretation.
- Easy to explain if the threshold is already familiar to reviewers.

Cons:

- Threshold metrics can hide the distribution of degradation.
- Sensitive to boundary choices and timing-missing handling.
- Requires precise definition of exact and timed eligibility.

Required ledger fields:

- `case_id`
- `engine`
- `method_role`
- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`

Denominator implications:

- Must use exact and timed eligible Track A rows only.
- Must not include unsupported, non-exact, or timing-missing rows as zero.

Paper narrative implications:

- Least disruptive to existing text, but strongest risk of appearing threshold-driven.

Implementation readiness:

- Not ready until timing eligibility and retained timing adapters are approved.

Recommendation:

- Keep only if the team wants strict paper continuity and can defend the threshold.

## Option B: Keep Regression@20 And Add Median / P25 / P75 / IQR

Pros:

- Preserves paper continuity while adding distribution visibility.
- Makes regression interpretation less brittle.
- Helps reviewers understand whether degradation is isolated or broad.

Cons:

- Adds more table columns and documentation.
- Requires clear handling of missing timing and exact/timed slices.

Required ledger fields:

- Same as Option A plus stable grouping keys for route, engine, and method role.

Denominator implications:

- Same exact/timed eligibility as Option A.
- Distribution summaries must state row counts.

Paper narrative implications:

- Maintains Regression@20 while presenting a more nuanced workbench report.

Implementation readiness:

- Not ready until timing policy and metric naming are finalized.

Recommendation:

- Strong default if the paper narrative must preserve Regression@20.

## Option C: Replace Regression@20 With Distribution/Quartile-first Reporting

Pros:

- Avoids brittle threshold framing.
- Better matches a public workbench that is denominator-aware and failure-aware.
- Supports method/engine route comparisons without global leaderboard framing.

Cons:

- Changes paper-facing metric vocabulary.
- Requires careful explanation against prior paper tables.
- May need team approval if Regression@20 appeared in submitted or reviewed text.

Required ledger fields:

- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`
- grouping keys.

Denominator implications:

- Exact/timed eligible rows only.
- Must show N for every distribution.

Paper narrative implications:

- Cleaner public workbench story, but higher documentation cost.

Implementation readiness:

- Not ready until final performance contract is approved.

Recommendation:

- Best long-term public workbench direction if team accepts metric wording changes.

## Option D: Use Both Threshold And Distribution But Mark Threshold Diagnostic

Pros:

- Preserves Regression@20 as a diagnostic continuity marker.
- Lets distribution summaries become primary public view.
- Reduces overinterpretation of a single threshold.

Cons:

- Requires clear primary/support labeling.
- Could confuse readers unless reports are structured carefully.

Required ledger fields:

- Same as Options A and C.

Denominator implications:

- Same exact/timed eligible slice for both threshold and distribution.
- Must report exact/timed row counts.

Paper narrative implications:

- Smooth transition from paper metric to workbench metric.

Implementation readiness:

- Not ready until team confirms naming and roles.

Recommendation:

- Recommended compromise: distribution-first public reporting with Regression@20 retained as diagnostic if paper continuity is needed.
