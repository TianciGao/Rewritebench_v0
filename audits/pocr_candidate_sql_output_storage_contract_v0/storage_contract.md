# Storage Contract

Future user-run candidate SQL outputs should follow the D035 output layout:

```text
output/results/<run_id>/candidate_sql/
  <method_id>/
    <route_id>/
      <engine>/
        <CASE_ID>__<engine>.sql
```

This keeps local user-run artifacts under `output/results/<run_id>/` and avoids updating top-level `reports/` or `results/`, which are official, paper, or release-facing surfaces.

The candidate SQL root should be accompanied by three manifests under the same run result root:

```text
output/results/<run_id>/candidate_sql_manifest.csv
output/results/<run_id>/candidate_root_manifest.csv
output/results/<run_id>/candidate_sha256_manifest.csv
```

No `output/` files are created by this documentation task.

## Why D035

D035 separates user-run outputs from official/paper/release surfaces. Candidate SQL can be large, route-bound, and locally generated. Keeping it under `output/results/<run_id>/candidate_sql/` lets future user-facing tools emit reproducible artifacts without touching top-level reports/results or retained evidence.

## Status Vocabulary

`candidate_status` is artifact status only. It is not correctness, execution status, checker status, timing eligibility, formal equivalence, or POCR.

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

## Boundary

Existing `runs/user` candidate roots are valuable read-only local/user-run assets. They should be referenced in manifests, not silently copied. PG40 candidate roots cannot fill Track A 120 POCR cells. No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.
