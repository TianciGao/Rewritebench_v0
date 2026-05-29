# Candidate SQL Output Storage Contract

This document defines the storage contract for future user-run candidate SQL outputs. It standardizes where candidate SQL should be written under the D035 user-output layout and how existing `runs/user` candidate roots should be referenced.

This is a storage/output contract only. It does not move existing files. It does not copy, delete, normalize, regenerate, or rewrite candidate SQL. It does not promote any candidate SQL to retained evidence. No official POCR is computed.

## Standard Output Tree

Future user-run candidate SQL should be written under:

```text
output/results/<run_id>/candidate_sql/
  <method_id>/
    <route_id>/
      <engine>/
        <CASE_ID>__<engine>.sql
```

Recommended example:

```text
output/results/direct_llm_repair_1_pg40_v0/candidate_sql/
  direct_llm_repair_1/
    direct_llm_repair_1_pg40/
      postgres/
        PERF_0006__postgres.sql
```

This follows D035: local user-run outputs belong under `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`. Top-level `reports/` and `results/` are official, paper, or release-facing surfaces and must not be updated by local user-run tasks.

## Candidate Manifests

Future user runs that emit candidate SQL should also emit:

```text
output/results/<run_id>/candidate_sql_manifest.csv
output/results/<run_id>/candidate_root_manifest.csv
output/results/<run_id>/candidate_sha256_manifest.csv
```

Do not create these files in the repository root. They are runtime outputs under the caller-provided output root.

### candidate_sql_manifest.csv

Fields:

- `run_id`
- `case_set_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_rel_path`
- `candidate_filename`
- `candidate_present`
- `candidate_status`
- `generated_status`
- `extraction_status`
- `source_run_id`
- `source_candidate_root`
- `sha256`
- `size_bytes`
- `created_by`
- `diagnostic_only`
- `retained_evidence`
- `notes`

### candidate_root_manifest.csv

Fields:

- `run_id`
- `method_id`
- `route_id`
- `engine_scope`
- `denominator_scope`
- `case_set_id`
- `candidate_root_rel_path`
- `candidate_count`
- `expected_count`
- `complete`
- `legacy_source_root`
- `migration_policy`
- `notes`

### candidate_sha256_manifest.csv

Fields:

- `run_id`
- `candidate_rel_path`
- `sha256`
- `size_bytes`
- `notes`

## Candidate Status Vocabulary

`candidate_status` describes artifact presence and extraction state. It is not correctness, checker status, execution status, timing status, or semantic equivalence.

Allowed values:

- `candidate_present`
- `candidate_missing`
- `generation_failed`
- `extraction_failed`
- `unsupported_engine`
- `preflight_blocked`
- `schema_invalid_candidate_file`
- `ambiguous_candidate`
- `legacy_source_only`

## Legacy runs/user Policy

`runs/user/**/candidate_sql` remains a legacy local/user-run source surface. It may be read as a source map for diagnostics, but it must not be deleted, moved, overwritten, normalized, or copied without inventory and retention mapping.

Existing `runs/user` candidate roots are not official retained evidence by default. They are not leaderboard inputs. Future contracts should reference them through manifest fields such as `source_run_id`, `source_candidate_root`, and `legacy_source_root` rather than silently copying them into new locations.

## PG40 and Track A 120 Examples

PostgreSQL-only PG40 output:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/postgres/<CASE_ID>__postgres.sql
```

Track A 120 output:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/postgres/<CASE_ID>__postgres.sql
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/mysql/<CASE_ID>__mysql.sql
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/spark/<CASE_ID>__spark.sql
```

PG40 candidate roots cannot fill Track A 120 POCR cells. Track A 120 requires 40 cases x 3 engines = 120 planned rows. Diagnostic PG40 output must be labeled PostgreSQL-only.

## Route Binding

Candidate SQL is bound by:

- `case_id`
- `engine`
- `method_id`
- `route_id`
- `run_id`
- candidate SHA-256
- `case_set_id`
- `denominator_scope`

This binding is required for future annotation JSONL replay. Route-bound annotation artifacts must not be reused against arbitrary method or route labels.

## POCR Relationship

Candidate SQL is an input to POCR Stage A annotation. Candidate SQL alone is not annotation JSONL. Candidate SQL alone cannot produce transformation-supported operation atoms. Annotation JSONL must be generated separately and must be route-bound.

POCR operation atoms come only from case-local root-level `skills.md`. Operation support requires transformation-aware Stage B evidence relative to source. API-generated annotation JSONL remains diagnostic evidence only unless separately promoted.

No paper-facing metric is promoted. No route-level POCR score is emitted. Official POCR remains separately gated.

## Table 1 Readiness Note

The Step 1b reconciliation found:

- Direct LLM original and Direct LLM Repair-1 have Track A 120 candidate readiness.
- SQLGlot no-op has PG40 candidate readiness only.
- SQLGlot optimize schema-aware and Calcite HEP fail-closed currently lack complete mapped candidate roots.
- LearnedRewrite is incomplete for PG40, with only 29 generated candidate files.
- R-Bot adapted GPT-5.4 and LLM-R2 adapted GPT-5.4 have PG40 readiness.

The Positive Operation Coverage Rate column remains deferred / N.A. until annotation generation, Stage B replay, and separate promotion policy are authorized.

## Non-Goals

- No files are moved.
- No output/ files are created by this contract.
- No candidate SQL is copied or deleted.
- No annotation JSONL is generated.
- No official POCR is computed.
- No paper-facing metric is promoted.
- No route-level POCR score is emitted.
- No leaderboard is produced.
