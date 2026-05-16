# Reports/Results Retained Evidence Map

Date: 2026-05-16

## Purpose And Scope

This audit maps legacy reports/results artifacts to retained-evidence categories for the fixed Common-core v0 release scope. It uses the aligned Common-core membership files under `case_sets/common_core_v0/` and the public inventory files under `inventory/` as the membership basis.

No legacy reports/results were copied or modified. No release `reports/` or `results/` directories were updated. No metrics were recomputed, no paper tables were regenerated, no denominator values were changed, and no new benchmark results were created.

## Legacy Paths Inspected

- `reports`: exists, 13186 files
- `results`: missing
- `reports/evaluation/common_core_v0`: exists, 13156 files
- `results/retained`: missing
- `results/local`: missing
- `runs`: missing

The legacy `results/`, `results/retained`, `results/local`, and top-level `runs/` paths are absent in this snapshot. Relevant artifacts are concentrated under legacy `reports/`, especially `reports/evaluation/common_core_v0/`.

## Common-core 40 Membership Basis

The mapping is bounded to the fixed Common-core v0 scope: 40 cases with pool split PERF 16, CONS 9, PORT 9, and LONGTAIL 6. Track A remains 120 planned same-engine rows. The aligned release files are references only; this task does not change membership or denominator values.

## Artifact Categories Found

- local_run_workspace: 4885
- raw_log_or_debug_output: 4094
- method_output_retained_reference: 3080
- timing_raw_or_timing_log: 522
- paper_facing_retained_evidence: 276
- unknown_manual_review_required: 233
- paper_summary_table: 69
- denominator_or_membership_reference: 14
- scratch_or_dev_output: 12
- sensitive_or_hygiene_review_required: 5

## Recommended Public Actions Found

- archive_private_or_external: 8979
- retain_by_reference_only: 3510
- copy_to_results_retained_later: 357
- defer_manual_review: 238
- summarize_in_public_report_later: 94
- exclude_from_public_release: 12

## Paper-Facing Retained Evidence Candidates

The retained candidate map contains 3439 candidate rows. All rows have `copy_now=false`; later migration must decide whether to copy, summarize, archive, or keep each candidate reference-only. Candidate classes include paper-facing evidence freezes, paper table/index artifacts, denominator references, method output references, plan observability artifacts, hard-negative accounting, portability/verifier artifacts, and reproducibility/provenance manifests.

## Local/Scratch/Log Candidates

Legacy report workspaces under `reports/evaluation/common_core_v0/runs/` contain local run workspaces, logs, generated SQL/JSON/TSV outputs, Spark warehouse residue, timing artifacts, and method-specific execution/generation outputs. These are not public retained evidence by default and should be kept reference-only, summarized, or archived privately unless separately reviewed.

## Sensitive Or Manual-Review Candidates

6762 unique artifacts require manual review by static heuristic. Manual-review drivers include local path/hygiene patterns, prompt/API/token or model-trace terms, raw logs/debug traces, unclear denominator linkage, unclear paper relevance, and timing evidence ambiguity.

## Recommended Next Step

Run a bounded reports/results public migration planning task that selects a minimal set of paper-facing artifacts for public retained evidence. That task should still avoid metric recomputation, denominator changes, paper-table regeneration, and raw log publication.

## What Must Not Be Done Yet

Do not copy raw legacy report workspaces wholesale. Do not publish raw logs or local run workspaces. Do not update paper tables, result metrics, denominator values, case membership, or raw legacy evidence without a separate explicit task.
