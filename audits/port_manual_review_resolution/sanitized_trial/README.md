# PORT Spark Plan Sanitization Trial

This directory contains Route B trial artifacts for six blocked Common-core PORT cases.

This is a trial, not final retained evidence. No legacy files were modified, sanitized in place, moved, deleted, renamed, or overwritten. Sanitized copies were generated only in this release-repo audit area from read-only legacy inputs.

The original artifacts remain retained through mapping and may later be placed in private or external archive. Raw local path traces are not allowed in sanitized trial outputs. This trial does not change Common-core membership, denominators, paper results, case admission status, or benchmark claims.

## Scope

Cases covered: PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025.

Artifacts covered: Spark plan text files identified by the PORT manual-review audit. PORT_0024 also has a sanitized summary trial for its Spark result-check record because the original references stdout/stderr log paths.

## Trial Outputs

- `redaction_manifest.csv`: one row per sanitized trial artifact.
- `redaction_validation.csv`: validation flags for each sanitized trial artifact.
- `original_to_sanitized_mapping.csv`: original-to-sanitized and original retention mapping.
- `case_clearance_after_sanitization_trial.md`: case-level trial clearance summary.
- `PORT_*/mapping.yaml`: per-case mapping records.

## Policy

Sanitized public copies preserve plan structure and evidence role while replacing local path and runtime-specific path material with stable placeholders. Original raw artifacts remain do-not-delete until final retention mapping and human approval.

## Validation Note

The validation CSV keeps the required schema, including a column label for host-name findings. A literal whole-tree substring scan can therefore flag that schema label even when generated evidence content is clean. Artifact-content validation ignores CSV header labels and validates generated sanitized artifacts and report values separately.
