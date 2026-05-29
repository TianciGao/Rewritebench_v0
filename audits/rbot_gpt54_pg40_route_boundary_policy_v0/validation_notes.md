# Validation Notes

Validation status:

- Markdown non-empty checks: passed for 11 Markdown/text files.
- CSV/JSON parse checks: not applicable for this packet because no CSV/JSON files are generated.
- Source audit existence checks: passed for the R-Bot scaffold, live smoke, prior PG40, recovery, canonical PG40 rerun, and prior-method onboarding packets.
- Copied metric value checks against `audits/rbot_gpt54_pg40_bounded_local_diagnostic_rerun_with_metrics_v0/`: passed.
- No-prohibited-command check: passed; no experiment, runtime, live LLM, DB/checker/timing, `compute-local-metrics`, verifier, MySQL/Spark, Track A 120, official metrics, paper rendering, retained evidence promotion, or leaderboard command was run.
- `git diff --check`: passed.
- Changed-file secret value scan: passed.
- Protected-path review: passed; changed files are limited to this audit packet and project-control writeback.
- Top-level reports/results and `runs/user/` change check: passed.

Expected copied metric values:

- selected 40
- generated 40
- candidate_executable 38
- exact 37
- timed 33
- mismatch 1
- candidate_execution_failed 2
- generation rate 1.0
- execution coverage 0.95
- result consistency 0.925
- GM speedup 0.9777997901126648
- P10/P25/P50/P75/P90 0.5865455274023522 / 0.9845480112740764 / 0.9998615395796396 / 1.0142327268706417 / 1.5983027547333224
