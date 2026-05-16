# PORT_0008

`PORT_0008` is a canonical-layout public release case package for one portability case derived from PARROT/BIRD source record `pg_res.json[4]`.

This package tests dialect adaptation around type coercion, identifier quoting, and date/time semantics across PostgreSQL-oriented source SQL plus MySQL and Spark target rewrites. It is a copy-first full case migration pilot for `PORT_0008` only.

## Package Scope

- Source SQL is in `sql/source.sql`.
- Positive rewrite SQL is in `sql/positives/pos_01.sql`.
- Hard-negative SQL is in `sql/negatives/neg_01.sql`.
- Engine DDL and witness load files are in `schema/`.
- Retained public evidence is under `evidence/`.
- Stable metadata is under `metadata/`.
- Human notes are under `notes/`.

## Evidence Boundary

Raw legacy run artifacts remain mapped through `evidence/runs_retention.yaml`. The raw Spark plan text files are not published in this canonical package because they contain local runtime path traces. The public Spark plan evidence reuses the previously validated sanitized retained plan files.

## Validation Asset Caveat

The copied validation scripts in `validation/` are retained legacy validation assets. They were not executed during this migration, are not yet canonical user runners, and future public runner output must not write to case-local `runs/` by default.

## Claim Boundary

This migration did not run DB engines, did not regenerate evidence, did not change denominator membership, did not change paper results, did not change Common-core membership, did not change case admission status, and creates no leaderboard.
