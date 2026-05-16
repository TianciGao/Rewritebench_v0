# Adapter Row-grain Policy v1 Draft

Status: draft policy, not implementation-authorizing

Purpose: define what one evidence ledger row represents and how future retained-evidence adapters should emit rows.

This draft does not implement adapters, scripts, metrics, report renderers, public runners, or a reproduction CLI.

## One-row Principle

One ledger row represents one typed evidence observation at the smallest grain that can be interpreted without mixing roles.

The standard candidate grain is:

`case_id x engine x route x method_role x candidate_id x denominator_id x evidence_source`

The standard control grain is:

`case_id x engine x control_route x control_id x evidence_source`

The standard artifact grain is:

`case_id or scope x engine if known x route/method/control if known x artifact_id x evidence_source`

## Record Type Taxonomy

Adapters must emit one of these record types:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

If a source artifact cannot be reduced to one of these without guessing, it should remain a `retained_summary_artifact` or be skipped with a manual-review note.

## Row-grain Examples

- Source control: `PERF_0006 x postgres x source x control`.
- Positive control: `CONS_0007 x spark x positive x control`.
- Hard-negative control: `PORT_0024 x mysql x hard_negative x control`.
- Same-engine rewrite candidate: `PERF_0013 x postgres x same_engine_rewrite x calcite_hep x candidate_id`.
- Failed generation row: candidate-scoped row with `generated=false`, `ready=false`, and `failure_stage=generation`.
- Execution failure row: candidate-scoped row with `executed=false` or `result_status=fail` and `failure_stage=execution`.
- Exact timed row: candidate-scoped row with `executed=true`, `exact=true`, `timed=true`, and non-null timing fields only after metrics approval.
- Plan artifact row: artifact-scoped row with `record_type=plan_observability_artifact`.
- PORT portability row: PORT case scoped row with `route=portability`.
- Verifier support pair: SQL pair x verifier tool x support result.
- Paper summary artifact: summary/index row with no metric denominator.
- Future user candidate: user output-root row with `record_type=user_run_candidate_cell`.

## Denominator ID Usage

`denominator_id` must reference an approved scaffold or be null.

Track A same-engine rewrite rows use IDs from:

`case_sets/common_core_v0/denominator_same_engine_120.csv`

Control rows may reference control IDs from:

`case_sets/common_core_v0/controls_360.csv`

Support-only rows, plan artifacts, verifier pairs, and summary artifacts must not reuse Track A denominator IDs unless a future metric contract explicitly defines a denominator-aware support metric.

## Method Role Usage

`method_role` identifies the role that produced or explains the row. It must separate controls, method candidates, verifier support, retained references, and user candidates.

Examples:

- `control`
- `direct_llm`
- `repair_1`
- `sqlglot`
- `calcite_hep`
- `r_bot`
- `verifier_support`
- `retained_legacy_reference`
- `user_candidate`

## Route Usage

`route` identifies the evidence path:

- `source`
- `positive`
- `hard_negative`
- `same_engine_rewrite`
- `portability`
- `plan_observability`
- `verifier_support`
- `summary`

Routes are metric boundaries. They must not be collapsed into one leaderboard.

## Candidate ID Usage

`candidate_id` must be stable within a case, engine, route, method role, and evidence source.

For retained evidence adapters, IDs should be deterministic from source artifact path plus parsed row keys. For user-run rows, IDs should be derived from a run manifest or submitted candidate identity. For controls, deterministic IDs may mirror `controls_360.csv`.

## Control Route Usage

Control routes are `source`, `positive`, and `hard_negative`.

Hard negatives are checker controls. A rejected hard negative is expected evidence for checker strictness, not a method-generated failure and not a rewrite performance row.

## Artifact ID Usage

Artifact rows use `artifact_id` as the artifact-level identity. In the current 28-field draft, artifact identity may be carried in `candidate_id` until a later schema revision adds a dedicated `artifact_id`.

Artifact rows should set `method_role=retained_legacy_reference` or another support role, and should not enter same-engine rewrite denominators.

## Support-pair Usage

Verifier support rows represent one SQL pair, verifier tool, and support result. They are support evidence only and must not be counted as rewrite-generation baseline rows.

## Why Record Types Must Not Be Mixed

Different record types answer different questions:

- controls validate package and checker behavior;
- rewrite candidates evaluate generated or transformed SQL;
- plan artifacts support observability;
- portability rows evaluate cross-engine boundaries;
- verifier support pairs document external support evidence;
- summaries preserve traceability;
- user-run rows represent future external submissions.

Mixing these into one leaderboard would hide denominator, route, timing, and support-only boundaries.

## Adapter Emission Rules

Adapters should:

- load fixed membership from `case_sets/common_core_v0/`;
- load case facts from `inventory/case_registry.csv` and manifests;
- parse retained artifacts only when row grain is clear;
- emit `unknown`, `not_applicable`, `requires_manual_review`, or null instead of inventing values;
- keep raw logs and local workspaces archive-only unless separately curated;
- avoid writing into case-local `runs/`;
- avoid metric computation.

## Failed And Missing Evidence

Failed, missing, unsupported, preflight-blocked, checker-rejected, and timing-missing evidence must be represented explicitly.

Adapters must not drop failed rows simply because they are not exact or not timed. Future metrics can decide whether to include or exclude them.
