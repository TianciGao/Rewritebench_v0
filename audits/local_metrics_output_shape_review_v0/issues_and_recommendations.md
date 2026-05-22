# Issues And Recommendations

## Issues Found

### Minor: literal `leaderboard` token appears in false boundary fields

Severity: low.

The reviewed outputs do not create a leaderboard, rank methods, select winners, emit `best_method`, or emit `winner`. They do include explicit negative boundary fields such as `leaderboard_input=false` and `leaderboard_output_created=false`.

This is consistent with prior local-only boundary schemas, but it conflicts with a literal interpretation of a check that says no output should include the token `leaderboard`.

## Non-Issues

- `preflight_passed` is present only as a funnel diagnostic, not part of Generation Rate.
- `source_executable` is present only as a diagnostic/environment guard, not part of Execution Coverage Rate.
- Local per-row `speedup_ratio` appears only in row-level timing diagnostics and exact + timed performance summaries.
- Semantic Equivalence Rate, Cross-Engine GM Speedup Ratio, Regression@20, and POCR remain N.A., deferred, or not implemented.
- No official metric flag, paper-result flag, retained-evidence promotion flag, reports/results output, paper table, ranking, or leaderboard artifact was observed.

## Recommended Next Safe Action

Accept the current output shape for broader local diagnostic projection if explicit false `leaderboard` boundary fields are acceptable. If a strict zero-token wording policy is required, authorize a narrow output-vocabulary patch before broader projection.
