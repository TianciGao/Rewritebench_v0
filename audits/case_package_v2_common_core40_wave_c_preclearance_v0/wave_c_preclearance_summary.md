# Common-core 40 Wave C Preclearance v0

## Purpose and scope

This branch-only read-only task resolves public-safety, dialect, schema, and manifest semantic preclearance for the eight remaining Wave C PORT/manual-review Common-core cases before any writable conversion. It does not convert cases, delete dialect variants, create schemas, run DB/checker execution, compute official metrics, update reports/results, update denominators, update case sets, update inventory, or create leaderboard output.

## Wave C case IDs

- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

## Public-safety preclearance summary

All eight cases are precleared as `public_safe_for_conversion` for a future writable v2 conversion task. The read-only scan found sanitized placeholders and environment-variable based validation-script references, not literal secrets, prompt/API/token traces, private host/user paths, or raw stdout/stderr payloads in the release case surfaces. Existing notes and `runs_retention.yaml` entries document that raw runs/logs were not copied wholesale.

D008 status after this task: 0 cases remain D008-blocked for conversion planning. Future writable conversion must still stop if it discovers any new raw/private evidence issue.

## Dialect variant decisions

`PORT_0004`, `PORT_0005`, and `PORT_0013` have Spark dialect variants and must retain them during conversion. Deletion is not allowed in Wave C conversion. The other five cases have no current dialect-variant directory, and conversion should keep that absence unless a separate portability review identifies a semantic need.

## Schema decisions

All eight cases are schema-precleared for per-case external schema packages. Exact DDL/load reuse was not approved because local schema assets differ by case. Future conversion should create:

- `parrot_bird_port0004_v0`
- `parrot_bird_port0005_v0`
- `parrot_bird_port0008_v0`
- `parrot_bird_port0012_v0`
- `parrot_bird_port0013_v0`
- `parrot_bird_port0022_v0`
- `parrot_bird_port0024_v0`
- `parrot_bird_port0025_v0`

## Manifest semantic readiness

All eight cases are manifest-precleared. `PORT_0004` and `PORT_0008` have explicit draft ids in provenance metadata. The remaining six can be converted with explicit non-blocking `draft_origin` caveats/fallbacks from current manifests, metadata, and migration notes. Future conversion must not invent source fields, taxonomy, source identity, draft origin, or dialect semantics.

## Recommended conversion subwaves

- Subwave 1: `PORT_0005` only, as the smallest non-D008 canary with retained Spark dialect variants.
- Subwave 2: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`, D008-cleared with no current dialect-variant directories.
- Subwave 3: `PORT_0004` and `PORT_0013`, D008-cleared with Spark dialect variants retained.

## Deferred/manual-review cases

No Wave C case remains deferred after this preclearance. Future writable tasks should still fail closed if they encounter new private paths, raw logs, unmapped retained artifacts, schema copy mismatches, or manifest fields that would require invention.

## PERF_0077/PERF_0082 follow-up note

`PERF_0077` and `PERF_0082` are already converted Wave B cases, not Wave C cases. Their `source_path` caveats do not block Wave C conversion, but they remain final public source-path closeout blockers and require a separate narrow provenance follow-up.

## Protected boundary summary

No case packages, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, dialect variants, evidence directories, or leaderboard outputs were modified or produced.

## Exact next safe action

Authorize `case_package_v2_common_core40_wave_c_subwave_1_port0005_v0` as a bounded writable conversion for `PORT_0005` only, preserving Spark dialect variants and all protected surfaces before broader Wave C subwaves.
