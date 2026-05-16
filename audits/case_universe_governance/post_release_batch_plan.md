# Post-release Batch Plan

Date: 2026-05-17

This plan recommends future non-Common-core migration waves after public v0 governance is approved. It does not migrate cases.

## Wave A: Low-risk Staged Candidates

Scope: registered staged candidates with complete core SQL/schema assets, manageable hygiene risk, and a close Common-core canonical pattern.

Expected action: small bounded canonical migration batches after staged membership approval.

## Wave B: Sanitization-needed Cases

Scope: cases with otherwise reasonable readiness but local path, Spark plan, raw log, or debug/tmp traces.

Expected action: evidence mapping and sanitization review before migration.

## Wave C: Checker / Hard-negative Approval Needed

Scope: cases with missing checker assets, unclear hard-negative role, or expected-rejection reasoning that needs approval.

Expected action: approval sweep and checker-pattern design before migration.

## Wave D: Longtail / Complex / Manual-review Cases

Scope: cases with incomplete engine closure, missing skeleton assets, complex structure, or manual-review flags.

Expected action: case-by-case readiness review and possibly representative pilots.

## Wave E: Defer / Exclude

Scope: unregistered, duplicate/alias, scratch, private, or unsupported directories.

Expected action: registry reconciliation before any release decision.
