# Common-core 40 Risk Summary

This readiness audit did not migrate cases. It groups risks that must be handled before future Common-core migration waves.

## Spark / Local-Path Plan Sanitization

All remaining unmigrated cases showed Spark plan/local-path sanitization pressure under static inspection. The public release should create sanitized retained plan copies while mapping raw originals as do-not-delete legacy artifacts.

## Checker / Hard-Negative Approval

CONS cases and several LONGTAIL/PORT cases contain hard negatives. The expected rejection reason must be explicit before migration. Use `CONS_0005` and `LONGTAIL_0011` as patterns, but do not infer approvals blindly.

## Validation Script Output-Policy Caveats

Legacy validation scripts typically write into case-local `runs/`. Future migrations must copy or adapt them as retained legacy validation assets and state that future public runner outputs should not write to case-local `runs/` by default.

## Performance / Speedup Overclaim

PERF cases are performance-sensitive but this migration track must not compute speedups or create timing claims. Retained timing/report artifacts, if any, must be mapped without creating new paper results.

## Workload-Frequency Overclaim

LONGTAIL cases may show realistic SQL structure. That is structural coverage only and must not become a production-frequency or workload-frequency claim.

## Reports / Results Dependency

Prior contract audit marks all 40 cases as report and paper-freeze referenced. Future migrations must preserve role-aware and denominator-aware reporting boundaries.

## runs/ Ambiguity

`runs/` is retained legacy evidence. It must be mapped through `evidence/runs_retention.yaml`; deletion is not recommended or authorized.

## Public Hygiene

Local paths, raw logs, and prompt/token-like categories must not appear in public retained evidence. Hygiene findings are listed in `common_core40_public_hygiene_findings.csv` without raw secret lines.

## Missing Files

All 40 case directories exist and include manifests, source SQL, positive rewrites, schema, validation assets, and runs. Provenance/taxonomy are often manifest-embedded rather than separate files, so future migrations must generate canonical metadata from manifest/audit facts.

## Mixed / Unknown Layouts

Legacy current layout is not canonical. Every non-piloted case still needs generated metadata, canonical path mapping, and validator v0.3 gates after migration.
