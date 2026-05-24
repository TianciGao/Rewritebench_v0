# Bounded Verifier Pass Plan

This is a planning document only. No verifier command was executed.

## Recommended First Tool

Try SQLSolver before VeriEQL. Existing project-control notes show SQLSolver was stronger on the SQLGlot no-op PostgreSQL exact subset, while VeriEQL remained coverage-limited after identity guard. SQLSolver also has an explicit JAR/CLI wrapper path and a simple source/candidate/schema invocation shape.

## Recommended First Route and Scope

First target: `sqlglot_noop` / `sqlglot_noop_track_a_120_canonical_v0`, PostgreSQL exact subset.

Reason: deterministic route, 35 PostgreSQL exact/result-consistent pairs, prior verifier-support evidence exists, and no live LLM behavior is involved. Start smaller than the full 35 rows: a 5-10 pair deterministic subset from `verifier_pair_materialization_manifest.csv`, preferably sorted by `case_id` and including multiple pools.

Current eligible-pair counts:

- `direct_llm_original`: 102 eligible exact/result-consistent pairs
- `sqlglot_noop`: 97 eligible exact/result-consistent pairs
- `sqlglot_optimize_schema_aware`: 66 eligible exact/result-consistent pairs
- `calcite_hep_fail_closed`: 81 eligible exact/result-consistent pairs

By engine:

- `calcite_hep_fail_closed`: postgres=25, mysql=26, spark=30
- `direct_llm_original`: postgres=39, mysql=32, spark=31
- `sqlglot_noop`: postgres=35, mysql=31, spark=31
- `sqlglot_optimize_schema_aware`: postgres=29, mysql=20, spark=17

## Draft Command Shape, Not Executed

The exact command should be finalized in a separately authorized task. A future D035-compatible shape should look like:

```bash
python -m cli.main user verify \
  --pair-manifest audits/track_a_120_verifier_pair_materialization_plan_v0/verifier_pair_materialization_manifest.csv \
  --route-id sqlglot_noop \
  --run-id sqlglot_noop_track_a_120_canonical_v0 \
  --engine postgres \
  --tool sqlsolver \
  --pair-limit 10 \
  --identity-guard \
  --output-root /tmp/sqlrb_track_a_120_bounded_sqlsolver_first_pass_v0/output \
  --verifier-run-id track_a_120_sqlsolver_first_pass_v0
```

If the current CLI does not yet expose this exact-candidate `user verify` scope, implement that facade separately before running tools. Do not bypass D035 output boundaries with ad hoc paper-facing outputs.

## Validation Gates Before Running

- Confirm `verifier_pair_materialization_manifest.csv` parses and contains only exact/result-consistent pairs.
- Confirm source SQL, candidate SQL, and schema paths exist for the selected subset.
- Confirm SHA256 hashes still match file contents.
- Confirm SQLSolver external command/JAR is configured outside the repository.
- Confirm output root is under `/tmp` or an explicitly authorized local-only output path.
- Confirm no top-level `reports/`, `results/`, retained evidence, paper files, or `runs/user` artifacts will be modified.

## Abort Criteria

- Any source-vs-source or candidate-vs-candidate identity guard returns `non_equivalent`, `unknown`, `timeout`, `unsupported`, `not_implemented`, `tool_error`, `no_verifier_support`, or `not_attempted` for the bounded subset at a systemic rate.
- Tool invocation writes outside the authorized output root.
- The tool requires vendoring source/JAR/dependencies into the release repo.
- The wrapper cannot retain raw output paths and normalized verdicts without secrets or local machine paths leaking into committed files.

## Output Paths

Recommended local-only output root:

- `/tmp/sqlrb_track_a_120_bounded_sqlsolver_first_pass_v0/output/results/track_a_120_sqlsolver_first_pass_v0/verifier/`
- `/tmp/sqlrb_track_a_120_bounded_sqlsolver_first_pass_v0/output/logs/track_a_120_sqlsolver_first_pass_v0/`
- `/tmp/sqlrb_track_a_120_bounded_sqlsolver_first_pass_v0/output/reports/track_a_120_sqlsolver_first_pass_v0/`

## Project-Control Writeback Requirements

A future bounded verifier pass must append `MIGRATION_RUN_LOG.md`, update `MIGRATION_STATUS.md`, report whether SQLSolver/VeriEQL ran, report identity guard outcomes, report SER status as `computed`, `coverage_limited`, or `N.A.`, and explicitly preserve denominator, case membership, paper results, retained evidence, and raw legacy evidence.
