# Overnight Governance And Redevelopment Investigation Bundle

Date: 2026-05-17

## Purpose And Scope

This read-only investigation bundle prepares governance and redevelopment planning artifacts after Common-core 40 canonical case-package migration. It covers staged/backlog membership planning for non-Common-core cases, reconciliation of seven unregistered legacy directories, legacy script redevelopment reference inventory, public release skeleton gap audit, and future prompt drafting.

No cases were migrated. No official `case_sets/staged_v0` or `case_sets/backlog_v0` files were created. No reports/results were copied. No scripts or `src/` implementation files were created. No metrics were computed, no paper tables were rendered, no denominator values changed, and no legacy files were modified.

## Confirmed Current State

- Common-core 40 canonical case packages are complete.
- `case_sets/common_core_v0/` and Common-core inventory scaffolds are aligned.
- Non-Common-core cases remain outside the public v0 main denominator.
- Metrics implementation, retained-evidence adapter implementation, reproduction CLI implementation, and public runner implementation remain unauthorized.
- Reports/results curated migration has not been performed.

## Staged/Backlog Findings

The prior case-universe audit identified 157 non-Common-core cases. This bundle reclassified all 157 into proposed planning buckets only:

- `manual_review_required`: 13
- `orphan_or_unregistered`: 7
- `proposed_backlog_v0`: 76
- `proposed_staged_v0`: 61


These are planning labels, not official release memberships. The strongest candidates for a later preview are the proposed staged and backlog buckets, but they still require maintainer approval and, in many cases, evidence indexing or hygiene review before migration.

## Unregistered Directory Findings

The seven detected but unregistered legacy directories were inspected read-only:

- `LONGTAIL_0006`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `LONGTAIL_0017`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0079`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0087`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: local_absolute_path, WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0092`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0100`: reason `new_unregistered_case`, disposition `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PORT_0007`: reason `new_unregistered_case`, disposition `staged_review_candidate`; checker directory absent; PORT_0007 has validation/checker.yaml only; runs/evidence absent; no retained execution evidence located; manifest explicitly says registry not updated/not registered


All seven require human review before registry admission or migration. Six have complete core SQL/schema/validation assets but no `runs/` or `evidence/` directories and no checker directory. `PORT_0007` is a draft portability package with provenance and checker material under `validation/`, but it still lacks witness implementation, retained runs, and formal validation.

## Script Inventory Findings

Legacy script/tool files reviewed: 123. `scripts/` exists with 122 files, `tools/` exists with 1 file, and `baselines/` is absent in the legacy snapshot.

Recommended classifications:

- `refactor_candidate`: 27
- `reference_only`: 68
- `wrap_candidate`: 28

Future layer mapping:

- `baselines`: 1
- `scripts/dev`: 91
- `scripts/metrics`: 2
- `scripts/reproduce`: 28
- `src/sql_rewrite_bench`: 1


The script inventory should be treated as redevelopment input, not implementation guidance to copy wholesale. Scripts with DB, output-path, local-path, case-local-runs, or LLM/API terms require careful refactoring or exclusion.

## Release Skeleton Gap Findings

Skeleton items reviewed: 24. Missing items: 18.

Priority counts:

- `must_add_before_release_v0`: 7
- `optional`: 2
- `present_required`: 5
- `should_add_before_release_v0`: 10

Highest-priority gaps include public `README.md`, license/citation/contributing metadata, `benchmark_spec/`, `docs/`, user/reproduction script namespaces, curated `reports/`/`results/`, tests, `src/`, and CI workflows. None were created by this audit.

## Recommended Next 3-5 Tasks

1. Run a staged/backlog official membership preview task that drafts but does not yet migrate non-Common-core membership files.
2. Run a benchmark_spec/public-docs skeleton formalization task covering README, benchmark spec, docs map, and release boundaries.
3. Run a legacy script redevelopment detailed design task to decide which legacy scripts become wrappers, adapters, or private/archive references.
4. Run a retained evidence reports/results triage task to select a minimal public-safe evidence copy set.
5. Run a public hygiene audit focused on scripts, planned reports/results targets, and release skeleton outputs.

## What Not To Do Yet

Do not migrate non-Common-core cases, create official staged/backlog membership, implement metrics, implement runners, copy reports/results, or compute paper tables until the relevant governance and metric/output decisions are approved.
