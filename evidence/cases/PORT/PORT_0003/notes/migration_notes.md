# Migration Notes

Date: 2026-05-16

This case was migrated copy-first into the canonical public-release layout as part of `port_wave_2_batch_001`. The legacy repository was inspected read-only and was not modified.

## Portability Boundary

This migration did not run database engines, did not create a new cross-engine execution result, did not create a transfer-speed claim, and did not create a complete nine-case PORT closure claim. Any portability interpretation remains tied to retained evidence and the paper protocol.

## Hard Negative

`neg_01` is an intentional hard negative with static-inferred reason `order_limit_direction_changed`. The hard negative flips the absolute-longitude ORDER BY direction and can select the wrong top-1 school. The approval status remains `migration_planning_static_inference_needs_review_if_not_explicit_in_legacy`.

## Spark Plan Sanitization

Raw Spark plan text files were not copied into public retained evidence. Public Spark plan evidence is sanitized or reused from an already validated sanitized evidence-mapping pilot; raw originals remain mapped as do-not-delete legacy artifacts.

## Raw Log Handling

Raw stdout/stderr logs were not copied into public evidence. Result and plan summaries are retained through JSON/TSV evidence where public-safe, and raw run artifacts remain mapped rather than deleted.

## Validation Asset Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not final public user runners, and future public runner outputs must not write to case-local runs/ by default.

## Paper Boundary

Denominator, paper results, Common-core membership, case admission status, and raw legacy evidence were unchanged.
