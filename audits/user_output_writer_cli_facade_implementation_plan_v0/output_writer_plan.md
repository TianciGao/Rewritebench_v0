# Output Writer Plan

## Proposed Module

Add a narrow internal helper module in a future implementation task:

```text
src/sql_rewrite_bench/user_output.py
```

This module should translate existing local diagnostic artifacts into the D035 user-facing output contract without changing core execution behavior.

## Proposed Boundaries

`user_output.py` should own:

- output path resolution for `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`
- path validation for user-facing output roots
- `run_manifest.json` writing
- boundary report writing
- machine-readable result artifact placement
- log artifact placement
- human-readable report generation
- failure bucket report generation
- tag-slice report generation
- metrics summary report generation when local metrics already exist

It should not own:

- case selection
- adapter execution
- DB execution
- checker semantics
- timing collection
- local metrics formulas
- verifier execution
- official reports/results promotion

## Candidate Function Boundaries

```text
resolve_user_output_roots(output_root, run_id, repo_root) -> UserOutputRoots
validate_user_output_root(output_root, run_id, repo_root) -> None
write_run_manifest(context, roots) -> Path
write_boundary_report(context, roots) -> Path
export_result_artifacts(run_dir, roots) -> list[Path]
export_log_artifacts(run_dir, roots) -> list[Path]
export_report_artifacts(run_dir, roots) -> list[Path]
write_failure_bucket_reports(run_dir, roots) -> list[Path]
write_tag_slice_reports(run_dir, roots) -> list[Path]
write_metrics_summary_report(run_dir, roots) -> Path | None
write_verifier_placeholder(roots) -> list[Path]
```

## Phase 2A Export Strategy

For the first implementation slice, keep `runs/user/<run_id>/` as the execution output and add a bounded export step that writes the user-facing contract. Prefer copying small text artifacts by default for portability. Links may remain a later developer-only optimization if needed.

The export should write:

```text
output/results/<run_id>/run_manifest.json
output/results/<run_id>/ledger.csv
output/results/<run_id>/quality_summary.json
output/results/<run_id>/failure_buckets.csv
output/results/<run_id>/tag_slices.csv
output/results/<run_id>/candidates/
output/results/<run_id>/execution/
output/results/<run_id>/checker/
output/results/<run_id>/timing/
output/results/<run_id>/metrics/
output/results/<run_id>/verifier/
output/logs/<run_id>/command.log
output/logs/<run_id>/adapter_stdout.log
output/logs/<run_id>/adapter_stderr.log
output/logs/<run_id>/engine_env.json
output/logs/<run_id>/failures.log
output/logs/<run_id>/timing.log
output/logs/<run_id>/verifier.log
output/reports/<run_id>/summary.md
output/reports/<run_id>/failure_buckets.md
output/reports/<run_id>/tag_slices.md
output/reports/<run_id>/metrics_summary.md
output/reports/<run_id>/verifier_summary.md
output/reports/<run_id>/boundary.md
```

Verifier files may be explicit placeholders only until VeriEQL and SQLSolver integration is authorized.

## Manifest Inputs

`run_manifest.json` should be assembled from current run arguments, `config.yaml`, git metadata, selection metadata, and output root paths. It must include local-only flags:

```text
local_diagnostic_only=true
official_metric_input=false
paper_result_input=false
retained_evidence_promoted=false
leaderboard_input=false
```

## Report Writers

Report generation should stay deterministic and derived from existing machine-readable artifacts:

- `summary.md` from `summary.json`, `quality_summary.json`, and ledger counts
- `failure_buckets.md` from `failures.csv` and ledger failure buckets
- `tag_slices.md` from `tag_slices.csv`
- `metrics_summary.md` from `metrics/local_metrics_summary.json` when present
- `verifier_summary.md` as N.A. until formal verifier artifacts exist
- `boundary.md` from fixed local-only boundary text

## Guardrails

- Do not write to top-level `reports/` or `results/`.
- Do not create official or paper-facing artifacts.
- Do not rank methods or emit leaderboard fields.
- Do not merge route outputs.
- Do not infer verifier evidence.
- Do not change exact/mismatch semantics.
