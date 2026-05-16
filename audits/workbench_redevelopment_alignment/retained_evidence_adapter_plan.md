# Retained Evidence Adapter Plan

Date: 2026-05-16

## Purpose

This plan describes how legacy retained evidence should be read into a future evidence ledger. It does not copy evidence, sanitize evidence, compute metrics, or update reports/results.

## Inputs

Future adapters should read:

- canonical case package manifests;
- `case_sets/common_core_v0/`;
- `inventory/case_registry.csv`;
- `inventory/source_registry.csv`;
- case-local `evidence/runs_retention.yaml`;
- reports/results retained-evidence map;
- public-safe retained controls, hard-negative evidence, and retained plans.

## Adapter Output

Adapters should emit evidence ledger rows with:

- case identity;
- case-set and denominator identity;
- engine;
- route;
- method role;
- candidate/control identity;
- generated/ready/executed/exact/timing state;
- checker state;
- plan availability;
- retained artifact reference;
- failure status and notes.

## Legacy Reports/Results Adapter

The reports/results adapter should:

- use `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv` as a selection input;
- keep `copy_now=false` candidates reference-only until approved;
- reject raw logs, local workspaces, prompt/model traces, and timing artifacts unless explicitly reviewed;
- preserve denominator labels without recalculating metrics.

## Case Package Adapter

The case package adapter should:

- read `manifest.yaml`;
- read `metadata/denominator_eligibility.yaml`;
- read `evidence/runs_retention.yaml`;
- map public-safe retained controls, plans, and hard-negative evidence into ledger rows;
- preserve sanitized-original relationships.

## User-Run Adapter

The user-run adapter should:

- read from an explicit output root outside case packages;
- write ledger rows for submitted candidate SQL;
- avoid mutating retained evidence;
- capture public-safe run manifests.

## Validation Gates

- Ensure case IDs exist in `inventory/case_registry.csv`.
- Ensure denominator IDs exist in the case-set scaffold.
- Ensure public artifact paths do not expose local paths or secrets.
- Ensure metric fields remain blank unless authorized by the metrics contract.

## Boundaries

Adapters are not metric calculators by default. They normalize evidence and provenance for later approved metrics/reporting stages.
