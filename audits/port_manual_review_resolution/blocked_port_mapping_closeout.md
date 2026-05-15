# Blocked PORT Evidence-Mapping Closeout

Date: 2026-05-15

## Scope

This closeout covers the six Common-core PORT cases that were previously blocked for public physical migration by Spark plan local-path evidence:

- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `PORT_0024`

`PORT_0004` is not part of this closeout because it was cleared earlier and was not blocked by Spark plan local-path evidence.

This is an evidence-mapping closeout only. It is not full case migration, not Common-core 40 migration, not physical migration of full case packages, not evidence regeneration, not deletion or cleanup, and not a database rerun.

## Summary Table

| Case | Evidence-mapping pilot closed | Sanitized plan copies | Result-check summary | Full case migration |
|---|---:|---:|---:|---|
| `PORT_0008` | yes | 2 | not required | not started |
| `PORT_0012` | yes | 2 | not required | not started |
| `PORT_0013` | yes | 2 | not required | not started |
| `PORT_0022` | yes | 2 | not required | not started |
| `PORT_0025` | yes | 2 | not required | not started |
| `PORT_0024` | yes | 2 | present | not started |

## What Was Verified

For each case, the closeout verified:

- case-local `MIGRATION_PILOT.md` exists;
- case-local `evidence/runs_retention.yaml` exists and parses as YAML;
- sanitized public Spark plan copies exist for `rewrite_neg_01` and `rewrite_pos_01`;
- sanitized plan files pass the required local-path and credential-keyword scan;
- formal validation CSV exists and marks artifacts public-safe;
- denominator and paper-result flags remain unchanged;
- original Spark plan artifacts remain mapped with do-not-delete status;
- `MIGRATION_RUN_LOG.md` contains a finalized entry with no legacy modification, no denominator change, no paper-results change, and no raw legacy evidence change.

For `PORT_0024`, the closeout also verified:

- `evidence/retained_controls/spark_result_check.sanitized_summary.json` exists;
- the sanitized summary parses as JSON;
- raw stdout/stderr log paths are replaced by placeholders;
- no raw stdout/stderr logs were copied into the release evidence slice.

## Closed At Evidence-Mapping Level

The following cases are now closed at the formal sanitized evidence-mapping pilot level:

- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0025`
- `PORT_0024`

This means the release repo now has case-local evidence slices that preserve public-safe Spark plan evidence through sanitized copies while keeping raw originals mapped and do-not-delete.

## What Remains

Full case migration has not occurred for any of these six cases.

Before full case migration, each case still needs an approved copy-first migration of source SQL, rewrite SQL, schema, checker, validation scripts, manifest, provenance, taxonomy, and any additional public evidence indexes. Those future steps must preserve the existing denominator, paper results, Common-core membership, route evidence, case admission status, and benchmark claims.

Raw legacy evidence remains in the legacy repository and must not be deleted. Original Spark plans, original result-check records, and any raw stdout/stderr logs remain mapped and private/archive-only unless separately approved later.

## PORT_0024 Difference

`PORT_0024` required extra result-check handling because its Spark `result_check.json` referenced stdout/stderr logs. The public release slice includes only a sanitized summary:

- `cases/PORT/PORT_0024/evidence/retained_controls/spark_result_check.sanitized_summary.json`

The sanitized summary preserves non-sensitive control-validation fields and replaces raw log paths with placeholders. Raw logs were not copied or inspected for this closeout.

## Non-Changes

No full case migration has occurred.

Denominators and paper results were not changed.

Common-core membership, route evidence, case admission status, and benchmark claims were not changed.

Legacy artifacts were not modified, moved, deleted, renamed, regenerated, or sanitized in place.

## Recommended Next Safe Actions

Recommended next phase: design a formal case package validator before full case migration, then run one copy-first physical migration pilot.

Candidate follow-up sequence:

- First, define a validator for required case package fields, evidence indexes, public-hygiene checks, and denominator-preservation assertions.
- Then, run a copy-first full case migration pilot on either `PORT_0004` for a lower-risk baseline or `PORT_0008` to test full migration with sanitized retained evidence already present.
- In parallel or immediately after the first full pilot, close the reports/results retained-evidence map before Common-core 40 migration.

Do not proceed directly to full Common-core 40 migration.
