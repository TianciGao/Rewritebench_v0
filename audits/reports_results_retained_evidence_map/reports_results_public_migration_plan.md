# Reports/Results Public Migration Plan

## Purpose

This is a plan for a later bounded migration step. It does not copy files now and does not authorize metric recomputation, denominator changes, paper-table regeneration, or result updates.

## What To Copy Later

- Minimal paper-facing retained evidence indexes from legacy `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/`, after manual review.
- Paper table/index provenance artifacts only as retained evidence, not as regenerated paper tables.
- Denominator and membership references only when they match `case_sets/common_core_v0/` and do not change Track A 120 planned rows.
- Selected plan observability, hard-negative accounting, portability/verifier, and reproducibility manifests after public hygiene review.

## Where To Copy Later

- Candidate public retained evidence should go under a future bounded release path such as `results/retained/common_core_v0/` or `reports/evaluation/common_core_v0/`, depending on the final release layout decision.
- Raw local workspaces and logs should not be copied into public retained evidence by default.

## What To Keep Reference-Only

- Legacy run workspaces under `reports/evaluation/common_core_v0/runs/`.
- Timing raw/log artifacts unless a separate timing-retention policy approves public summaries.
- Prompt/model metadata artifacts unless sanitized and reviewed.
- Denominator preflight artifacts that could be confused with changed denominator values.

## What To Exclude

- Raw logs, debug traces, Spark warehouse residue, parquet/crc success markers, pyc files, and local workspace output.
- Scratch scripts and developer-only runner scaffolds unless separately reviewed for public runner migration.

## Validation Gates

- Public hygiene scan for local paths, prompt/API/token/model traces, raw stdout/stderr references, and debug traces.
- CSV/JSON/YAML parsing for copied summaries.
- Cross-check against `case_sets/common_core_v0/cases.csv` and `denominator_same_engine_120.csv`.
- Explicit `copy_now=false` should become true only in a later approved task.

## No-Change Rule

The later task must not change denominator values, paper results, case membership, metric values, or paper tables. Retained evidence mapping is not a new result.

## Future Prompt Outline

1. Read project control, case_sets, inventory, and this audit.
2. Select a minimal reviewed artifact subset from `retained_evidence_candidate_map.csv`.
3. Copy only approved public-safe artifacts into the selected release retained-evidence path.
4. Sanitize or summarize where required.
5. Run public hygiene and parser checks.
6. Update project-control files with explicit no-denominator/no-paper-result boundaries.
