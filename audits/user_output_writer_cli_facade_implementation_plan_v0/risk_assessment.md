# Risk Assessment

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Route mixing in output summaries | Misleading local metrics or comparisons | Require route_id, method_id, denominator_id, and run_id in manifest and summaries. |
| Confusion between `output/` and official `reports/`/`results/` | Local diagnostic artifacts could be mistaken for paper evidence | Write `boundary.md`, local-only flags, and avoid top-level official surfaces. |
| Runtime output accidentally committed | Repository churn and accidental evidence promotion | Keep output runtime dirs ignored/uncommitted and add validation checks. |
| Duplicate business logic in `src/cli` | Divergence from internal runner behavior | CLI delegates to `src/sql_rewrite_bench` only. |
| Premature physical layout migration | Path resolver and validator breakage | Do not move cases, case_sets, schemas, inventory, scripts, or docs in Step 2. |
| Verifier placeholders misread as verifier evidence | Semantic Equivalence Rate misinterpretation | Mark verifier outputs N.A. until VeriEQL or SQLSolver artifacts exist. |
| Metrics output interpreted as official | Paper/reporting boundary violation | Keep local-only flags and prohibit reports/results/leaderboard output. |
| Large workspace artifact copying | Slow or bloated local output | Phase 2A should inventory actual artifact sizes and copy minimal text artifacts first. |
