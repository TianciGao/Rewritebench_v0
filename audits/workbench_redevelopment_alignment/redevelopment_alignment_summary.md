# Workbench Redevelopment Alignment Summary

Date: 2026-05-16

## Purpose And Scope

This audit records the project-level pivot from migration-first work to redevelopment-led public workbench construction.

This task did not migrate cases, copy reports/results, implement scripts, run DB engines, run validation scripts, run LLM calls, run timing workloads, compute metrics, update paper tables, update reports/results, change denominator values, change case membership, update `case_sets/`, or modify raw legacy evidence.

## Why Strategy Is Changing

Common-core 40 canonical case-package migration is complete, Common-core v0 membership/denominator scaffolds are aligned, and reports/results retained-evidence mapping exists. Continuing by mechanically moving legacy scripts and reports would preserve legacy complexity instead of producing a clean public workbench.

Legacy artifacts mix DB runners, LLM runners, local paths, scratch outputs, logs, timing artifacts, and paper renderers. They should now be reference inputs, retained evidence sources, or adapter targets.

## What Remains Unchanged

- Common-core v0 remains 40 cases.
- Pool split remains PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Track A remains 120 planned same-engine rows.
- Paper results are unchanged.
- Denominator values are unchanged.
- Case membership is unchanged.
- Raw legacy evidence is unchanged.
- No global leaderboard is introduced.

## What Is Now Prioritized

- Evidence ledger schema.
- Metrics contract.
- Runner/output policy.
- Retained evidence adapter.
- User-facing candidate runner design.
- Reproduction CLI design.
- Report renderer design.
- Public documentation and README path.

## What Is Deferred

- Implementing a unified reproduction CLI.
- Implementing paper table renderer.
- Implementing metric computation.
- Copying reports/results into public retained locations.
- Rerunning DB validation or timing workloads.
- LLM baseline reruns.
- Non-common-core case migration or denominator expansion.

## Relation To Old Layout Plan

The old migration plan correctly established the target public layout, canonical case packages, retained evidence policy, and Common-core 40 public v0 scope. The redevelopment phase keeps those outputs but stops treating legacy script/report movement as the governing architecture.

## Required Confirmation Before Metrics Implementation

Before implementing the unified reproduction interface, paper table renderer, or metric computation, the maintainer/team must confirm final metric definitions, including fallback/regression reporting, parseability/extractability/runnable SQL fields, observability wording, output-root policy, and whether public v0 includes LLM reruns or retained evidence only.

## Next Safe Action

Resolve open metrics and reproduction-interface questions, then approve the evidence ledger schema and public runner output policy before writing implementation code.
