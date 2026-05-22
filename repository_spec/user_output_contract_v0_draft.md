# User Output Contract v0 Draft

Status: draft design only.

This draft defines the intended user-facing output and CLI/interface contract for SQL-RewriteBench local evaluation workbench v0. It is aligned with D034 and D035.

This draft does not implement output writing, CLI code, verifier integration, timing collection, metrics computation, reports/results updates, retained-evidence promotion, paper rendering, leaderboard output, or physical layout migration.

## Output Roots

Future user-facing local runs should use:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

The older `output/<run_id>/...` shape is superseded by D035.

## Results Artifacts

`output/results/<run_id>/` should contain:

```text
run_manifest.json
ledger.csv
quality_summary.json
failure_buckets.csv
tag_slices.csv
candidates/
execution/
checker/
timing/
metrics/
verifier/
```

`run_manifest.json` must include run identity, git/workbench identity, case-set and engine scope, adapter route/method identity, denominator identity, verifier/timing flags, output roots, contract version, and local-only boundary flags.

Required local-only flags:

```json
{
  "local_diagnostic_only": true,
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

## Log Artifacts

`output/logs/<run_id>/` should contain:

```text
command.log
adapter_stdout.log
adapter_stderr.log
engine_env.json
failures.log
timing.log
verifier.log
```

Logs must avoid credentials, private endpoints, and unnecessary absolute local paths.

## Report Artifacts

`output/reports/<run_id>/` should contain:

```text
summary.md
failure_buckets.md
tag_slices.md
metrics_summary.md
verifier_summary.md
boundary.md
```

Reports are human-readable local diagnostic summaries derived from result artifacts. They must not update top-level `reports/` or `results/`.

## Failure Buckets And Tag Slices

Machine-readable failure and tag summaries:

- `output/results/<run_id>/failure_buckets.csv`
- `output/results/<run_id>/tag_slices.csv`

Human-readable failure and tag summaries:

- `output/reports/<run_id>/failure_buckets.md`
- `output/reports/<run_id>/tag_slices.md`

`failure_buckets.csv` expected fields:

- `failure_bucket`
- `count`
- `engines`
- `pools`
- `representative_cases`
- `explanation`

`tag_slices.csv` expected fields:

- `tag_axis`
- `tag`
- `selected`
- `candidate_generated`
- `candidate_executable`
- `exact`
- `mismatch`
- `label_only_mismatch`
- `timed`
- `dominant_failure_bucket`
- `notes`

## Verifier Placeholder

Future verifier artifacts should live under:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/
```

VeriEQL and SQLSolver are verifier/support tools, not rewrite baselines. Semantic Equivalence Rate remains `N.A.` until formal verifier evidence exists.

## CLI Contract

Preferred command shape:

```bash
sqlrb user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id <run_id> \
  [--collect-timing] \
  [--verifier verieql] \
  [--verifier sqlsolver]
```

Convenience commands:

- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- `sqlrb user compute-local-metrics --run-id <run_id> --output-root output`
- `sqlrb user summarize --run-id <run_id> --output-root output`
- `sqlrb user show-boundary --run-id <run_id> --output-root output`

## Facade Policy

Users should not call internal `src/sql_rewrite_bench/` modules directly.

Future public facade target:

- `src/cli`

Internal package:

- `src/sql_rewrite_bench`

Development and validation tools:

- `src/dev`

## Transition Policy

Existing `runs/user/` remains a legacy/development local run surface during transition. New user-facing runs should target `output/results|logs|reports/<run_id>/`.

Do not delete or move existing `runs/user/` outputs. Do not commit generated `output/` runtime artifacts.

## Boundary

`output/` local run outputs are not official metrics, paper results, retained evidence, or leaderboard input. Promotion from `output/` to official `reports/`, `results/`, or retained evidence requires a separate promotion task.
