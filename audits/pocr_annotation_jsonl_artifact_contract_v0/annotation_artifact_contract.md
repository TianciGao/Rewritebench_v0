# Annotation Artifact Contract

POCR annotation artifacts should follow the D035 user-output layout:

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

This tree separates candidate SQL from Stage A annotation artifacts while preserving route binding.

Candidate SQL remains under:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/<engine>/<CASE_ID>__<engine>.sql
```

Annotation JSONL binds to candidate SQL through `run_id`, `case_set_id`, `case_id`, `pool`, `engine`, `method_id`, `route_id`, `candidate_rel_path`, `candidate_sha256`, `candidate_id`, and `denominator_scope`.

annotation JSONL is diagnostic evidence. It is not official POCR, not a paper-facing metric, and not a leaderboard artifact.
