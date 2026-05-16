# CONS Migration Batch Recommendation After Approval

## Primary Batch

Recommended primary batch after maintainer approval: CONS_0007, CONS_0009, CONS_0010, CONS_0011.

Why these cases: they have high-confidence static hard-negative explanations, retained tri-engine result evidence, and represent the core CONS checker patterns: correlated EXISTS predicate boundary, correlated UNION ALL aggregate key drift, self-row exclusion in anti-join semantics, and outer-join NULL preservation.

Expected Codex autonomy: medium-high after approval. The user does not need to be present during the batch if the approval wording in this audit is accepted, but should review the final audit outputs before the next batch.

## Fallback Batch

Smaller fallback batch: CONS_0007, CONS_0009, CONS_0010.

Use this if the maintainer wants to defer the first outer-join NULL-preservation migration until after the correlated-subquery cases pass.

## Later Batch

Recommended second batch: CONS_0012, CONS_0024, CONS_0036, CONS_0037.

Why later: these remain high confidence, but they cover a broader semantic mix: LIMIT/OFFSET threshold, row-preserving LEFT JOIN collapse, aggregate filter literal drift, and DISTINCT aggregate multiplicity.

## Cases Not Included

CONS_0005 is already migrated and is a reference only. No target case is recommended for defer based on this review, but all eight still need maintainer approval before future migration marks the expected rejection as approved.

## Stop Conditions

Stop future CONS migration if any expected rejection wording is not approved, a legacy source file is missing, a public hygiene scan fails after sanitization, copied hashes mismatch, validator v0.3 fails, denominator/paper-result/case membership changes are detected, raw legacy evidence is modified, or a broad `git add .`/broad commit scope is attempted.

## Future Prompt Outline

A future prompt should list the approved cases, require canonical layout, copy SQL/schema/witness/validation assets read-only from legacy, generate checker expected-rejection files from approved wording, sanitize Spark plan text if promoted, map raw runs in `runs_retention.yaml`, run full-case and canonical-case validators, update project-control files, and commit explicit paths only.
