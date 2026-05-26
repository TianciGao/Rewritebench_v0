# POCR Annotation JSONL Artifact Contract

This document defines the route-bound Stage A annotation artifact contract for Positive Operation Coverage diagnostic support.

`skills.md` defines the case-local atom contract. Candidate SQL is the baseline or method output artifact. Annotation JSONL is the per-candidate Stage A annotation artifact. Stage B transformation-aware validation consumes annotation JSONL and candidate/source/positive SQL context. Annotation JSONL is diagnostic evidence; it is not itself official POCR.

Candidate SQL is not converted into JSONL. Candidate SQL is referenced by annotation JSONL through route-bound candidate identity fields.

## Standard Annotation Output Tree

Future POCR annotation artifacts should be written under the D035 user-output layout:

```text
output/results/<run_id>/pocr/annotations/
  <method_id>/
    <route_id>/
      <engine>/
        safe_annotation_outputs.jsonl
        annotation_manifest.csv
        annotation_schema_validation.csv
        prompt_manifest.csv
        provider_call_manifest.csv
```

Do not create these files in this repository as part of contract work. They are runtime outputs under a caller-provided output root.

## Relationship To Candidate SQL Storage

The annotation artifact binds to the candidate identity defined in `candidate_sql_outputs.md`.

Candidate SQL:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/<engine>/<CASE_ID>__<engine>.sql
```

Annotation:

```text
output/results/<run_id>/pocr/annotations/<method_id>/<route_id>/<engine>/safe_annotation_outputs.jsonl
```

Required binding fields:

- `run_id`
- `case_set_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_rel_path`
- `candidate_sha256`
- `candidate_id`
- `denominator_scope`

## Annotation JSONL Row Schema

Each line in `safe_annotation_outputs.jsonl` is one JSON object for one candidate row.

Required top-level fields:

- `annotation_schema_version`
- `run_id`
- `case_set_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_id`
- `candidate_rel_path`
- `candidate_sha256`
- `skills_md_sha256` or `skills_contract_hash`
- `prompt_template_id`
- `prompt_template_version`
- `provider_label`
- `model_label`
- `call_timestamp_utc`
- `decoding_parameters`
- `annotation_status`
- `atoms`

Each atom object includes:

- `atom_id`
- `atom_type`
- `expected`
- `observed_status`
- `rationale_short`
- `evidence_refs`
- `confidence`

Allowed `atom_type` values:

- `operation_atom`
- `semantic_guard_atom`

Allowed `observed_status` values:

- `implemented`
- `not_implemented`
- `contradicted`
- `unclear`
- `not_applicable`

## Annotation Status Vocabulary

Allowed annotation statuses:

- `schema_valid`
- `schema_invalid`
- `malformed_json`
- `missing_annotation`
- `duplicate_annotation`
- `case_mismatch`
- `engine_mismatch`
- `method_mismatch`
- `route_mismatch`
- `candidate_mismatch`
- `skills_contract_mismatch`
- `provider_call_failed`
- `skipped_no_candidate`
- `skipped_unsupported_engine`

## Manifest Files

`annotation_manifest.csv` fields:

- `run_id`
- `case_set_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_rel_path`
- `candidate_sha256`
- `annotation_jsonl_rel_path`
- `annotation_status`
- `annotation_schema_version`
- `prompt_template_id`
- `prompt_template_version`
- `provider_label`
- `model_label`
- `call_timestamp_utc`
- `live_api_used`
- `diagnostic_only`
- `official_pocr_computed`
- `paper_metric_promoted`
- `notes`

`annotation_schema_validation.csv` fields:

- `run_id`
- `case_id`
- `engine`
- `method_id`
- `route_id`
- `candidate_sha256`
- `row_number`
- `validation_status`
- `error_type`
- `error_message`
- `fail_closed`
- `notes`

`prompt_manifest.csv` fields:

- `run_id`
- `prompt_template_id`
- `prompt_template_version`
- `prompt_hash`
- `skills_contract_hash`
- `input_fields`
- `system_message_hash`
- `boundary_instructions_present`
- `notes`

`provider_call_manifest.csv` fields:

- `run_id`
- `case_id`
- `engine`
- `method_id`
- `route_id`
- `provider_label`
- `model_label`
- `call_timestamp_utc`
- `temperature`
- `max_tokens`
- `response_format`
- `token_counts_if_available`
- `call_status`
- `error_type`
- `diagnostic_only`
- `notes`

## Route Binding And Replay Policy

Replay requires exact `case_id`, `engine`, `method_id`, `route_id`, and candidate identity match. Annotation artifacts are route-bound evidence and are not reusable across arbitrary route labels.

- route mismatch must fail closed.
- method mismatch must fail closed.
- case mismatch must fail closed.
- engine mismatch must fail closed.
- candidate_sha256 mismatch must fail closed unless a separately authorized alias/remapping policy exists.
- `skills_contract_hash` mismatch must fail closed unless a separately authorized migration policy exists.
- duplicate annotation rows fail closed or are deterministically rejected.
- missing annotation rows remain `missing_annotation`.
- malformed JSON remains `malformed_json` / `schema_invalid`.

Matching-route replay example:

- candidate route: `direct_llm_original_pg40_pocr_diagnostic`
- annotation route: `direct_llm_original_pg40_pocr_diagnostic`
- result: may be accepted as diagnostic input if the rest of the schema and candidate binding match.

Route-mismatch replay example:

- candidate route: `direct_llm_original_pg40_user_replay`
- annotation route: `direct_llm_original_pg40_pocr_diagnostic`
- result: fail closed as `route_mismatch`.

Candidate SHA mismatch example:

- candidate file path resolves but `candidate_sha256` differs from the annotation row.
- result: fail closed as `candidate_mismatch`.

## Evidence Refs Contract

Supported `evidence_refs` syntax:

- `candidate_sql_span:<literal substring>`
- `source_sql_span:<literal substring>`
- `positive_sql_span:<literal substring>`
- `candidate_token_span:<normalized tokens>`
- `source_candidate_diff:changed`

Evidence boundaries:

- `candidate_sql_span` alone is presence evidence only.
- `source_sql_span` alone is not operation coverage evidence.
- `positive_sql_span` alone is not operation coverage evidence.
- Operation support requires transformation-aware Stage B validation.
- LLM rationale is not evidence.
- Runtime/speedup is not operation evidence.
- Taxonomy tags are not operation evidence.
- Checker exactness is not operation evidence in this POCR layer.
- `semantic_guard_atom` is not operation coverage numerator.

## Diagnostic Vs Official Boundary

Annotation JSONL is diagnostic evidence. Stage A annotation alone is not counted. Stage B transformation-aware validation is diagnostic only.

No official POCR is computed by merely generating annotation JSONL. No route-level POCR score is emitted. No paper-facing metric is promoted. No global leaderboard is produced.

## PG40 Vs Track A 120 Annotation Scope

PG40 annotation JSONL covers PostgreSQL-only rows. PG40 annotation JSONL cannot fill Track A 120 POCR cells.

Track A 120 requires 40 cases x 3 engines candidate rows and corresponding route-bound annotation rows. Missing candidate rows must remain visible as `skipped_no_candidate` or an equivalent fail-closed/missing annotation status.

Annotation scope must match denominator scope.

## Relationship To Live API

This Step 3 contract does not call API. Future live annotation generation requires explicit authorization and an explicit live flag. API keys must come from environment only.

Do not store API keys or secrets in annotation JSONL, manifests, logs, or audit packets. Provider/model labels, prompt/template identifiers, call timestamps, decoding parameters, token counts if available, and safe call status metadata should be recorded.

## Non-Goals

- No annotation JSONL is generated in this task.
- No live API is called.
- No API key is read.
- No candidate SQL is moved, copied, or deleted.
- No DB/checker/timing run occurs.
- No official POCR is computed.
- No paper-facing metric is promoted.
- No route-level POCR score is emitted.
- No leaderboard is produced.
