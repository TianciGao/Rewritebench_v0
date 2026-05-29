# POCR Deferred Boundary

Positive Operation Coverage Rate is paper-facing but deferred.

POCR implementation is not part of this migration task. An external operation-atom/skill script and stable schema are required before POCR can be computed or promoted.

Current boundary:

- No skill folders should be created now.
- No operation atom files should be created now.
- Operation atoms must not be inferred from taxonomy tags.
- Operation atoms must not be inferred from SQL text.
- Operation atoms must not be inferred from `positive.sql`.
- Operation atoms must not be inferred from manifest descriptions.
- Operation atoms must not be inferred from README text.
- Operation atoms must not be inferred from checker files.
- `tag_slices` are diagnostic and cannot substitute for POCR.
- Failure buckets are diagnostic and cannot substitute for POCR.
- Plan deltas cannot substitute for POCR unless a future external operation-atom evidence contract explicitly authorizes them.

Future POCR integration must be separately authorized after the collaborator's external operation-atom script/schema is stable.
