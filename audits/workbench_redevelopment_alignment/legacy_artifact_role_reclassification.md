# Legacy Artifact Role Reclassification

Date: 2026-05-16

## Purpose

This document reclassifies legacy artifacts after Common-core 40 canonical case-package migration and registry alignment. It does not move, copy, delete, or rewrite any legacy file.

## Legacy Scripts

Role: reference, wrap, refactor, or adapter candidates.

Legacy scripts should not be copied wholesale into the public release. They may inform:

- runner behavior;
- parser/checker wrappers;
- evidence adapters;
- report rendering logic;
- validation smoke tests.

Future public scripts should be designed against canonical case packages, aligned case sets, evidence ledger, output policy, and metrics contract.

## Legacy Reports/Results

Role: retained evidence source and comparison target.

Legacy reports/results should be mapped into a future evidence ledger or curated retained-evidence path. They are not the canonical data model and should not govern public architecture.

No legacy report/result should be copied before public hygiene, denominator, paper-result, and manual-review checks.

## Legacy Runs

Role: evidence surface and retention-mapping source.

Case-local `runs/` and report-run workspaces preserve retained evidence and local historical state. They should remain read-only inputs unless a bounded task explicitly maps, sanitizes, or summarizes them.

New user outputs must not write into case-local `runs/`.

## Old Paper Tables

Role: comparison target, not canonical data model.

Paper tables remain fixed unless a separate approved task authorizes regeneration or update. Future renderers should read from an evidence ledger and metrics contract, then compare against retained legacy tables as needed.

## Non-Common-Core Cases

Role: governed backlog/universe.

Non-common-core cases remain outside the public v0 denominator. They require separate governance, including the 197 vs 190 case universe reconciliation, before public expansion.

## Immediate Boundary

The redevelopment phase does not change metrics, paper results, denominator values, case membership, or raw legacy evidence.
