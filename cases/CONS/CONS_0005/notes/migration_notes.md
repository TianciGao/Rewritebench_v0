# CONS_0005 Canonical Migration Notes

Date: 2026-05-16

## Scope

This is a one-case copy-first canonical-layout migration for `CONS_0005` only. Legacy files remain unchanged and mapped. No DB engines were run and no evidence was regenerated during migration.

## Hard-Negative Approval

The hard-negative expected rejection for `neg_01` is maintainer-approved for migration. `neg_01` does not preserve NULL-sensitive correlated `NOT IN` semantics. On retained witness evidence, source and positive outputs are empty, while negative output is `1	3`.

## Spark Plan Evidence

Raw legacy Spark plan text files contain local temporary path traces and were not copied raw into public retained evidence. Sanitized public copies are under `evidence/retained_plans/spark/`; raw originals remain do-not-delete legacy artifacts mapped in `evidence/runs_retention.yaml`.

## Validation Assets

The scripts in `validation/` are retained legacy validation assets. They were not executed during this migration, are not yet canonical public user runners, and future public runner output must not write to case-local `runs/` by default.

## Claim Boundary

Denominator unchanged. Paper results unchanged. Common-core membership unchanged. Case admission status unchanged. Raw legacy evidence unchanged. No global leaderboard is introduced.
