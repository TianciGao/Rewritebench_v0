# Case Package Contract v1

Status: first draft for clean public release migration

This contract defines the target structure and evidence semantics for SQL-RewriteBench public case packages. It is a migration target, not a claim that the legacy repository already follows this layout.

## 1. Benchmark Unit

The benchmark unit is a case package, not a raw SQL string. A case package preserves the source SQL, positive rewrite or target adaptation, hard negatives, schema/data context, checker paths, plan/failure artifacts when available, provenance, taxonomy tags, and reporting metadata.

## 2. Paper-Facing Constraints

The public release must preserve:

- Common-core v0 = 40 cases;
- pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL;
- Track A same-engine denominator = 120 planned rows;
- role-aware and denominator-aware reporting;
- no global leaderboard;
- visibility of unsupported, failed, mismatched, no-op/source-like, checker-failed, timing-missing, and missing-artifact states.

Common-core membership belongs in `case_sets/`, not by physically duplicating cases.

## 3. Target Case Layout

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/
  schema/
  data/
  checker/
  validation/
  evidence/
  metadata/
  notes/
  runs/
```

The target layout may be reached gradually. Existing legacy paths must remain traceable through manifests and retention mappings during migration.

## 4. Primary Index

`manifest.yaml` is the primary case-local index. It should point to SQL artifacts, schema/data context, checker and validation assets, provenance, taxonomy, denominator/reporting metadata, and evidence indexes.

Manifest updates must not change case admission status, Common-core membership, denominators, paper results, or scientific claims unless separately approved.

## 5. Required Components

Required for a release-grade case package:

- source SQL or source query identity;
- at least one positive rewrite, target adaptation, or clearly declared variant where applicable;
- hard negatives for checker-control cases where applicable;
- schema/data context sufficient to understand validation;
- checker or normalization configuration when result comparison is used;
- provenance metadata;
- taxonomy metadata aligned to the 4+1 framing;
- denominator/reporting metadata where the case participates in frozen sets;
- `evidence/runs_retention.yaml` when legacy `runs/` exists.

## 6. Optional Components

Optional but recommended:

- validation scripts;
- plan collection scripts;
- witness design notes;
- risk notes;
- engine support metadata;
- sanitized retained plan artifacts;
- summarized retained result-check artifacts.

## 7. Legacy-Allowed Components

`runs/` is allowed as a legacy retained evidence surface. It is not the default location for new run outputs.

Legacy layouts may keep root-level SQL files, root-level taxonomy files, or historical validation assets during migration if the manifest and `runs_retention.yaml` preserve traceability.

## 8. Evidence Directory

`evidence/` is the target public evidence index surface. It may contain:

- `runs_retention.yaml`;
- sanitized retained controls;
- sanitized retained plans;
- hard-negative evidence summaries;
- package validation summaries;
- archive reference records.

Evidence files must distinguish public-safe retained evidence from private/original archive references.

## 9. `evidence/runs_retention.yaml`

Every migrated case with legacy `runs/` should have `evidence/runs_retention.yaml`.

It records:

- original legacy paths;
- public-safe retained artifacts;
- sanitized public copies;
- private/original archive mappings;
- external archive references;
- regenerable outputs;
- manual-review status;
- do-not-delete entries;
- static references that would break if files move.

## 10. Sanitized Evidence Mapping

Sanitized public evidence must preserve evidence-bearing content while removing local paths, raw log paths, prompt/API traces, credentials, and other release-hygiene risks.

The mapping must link each sanitized public artifact to its original legacy artifact and record the redaction scope.

## 11. External and Private Archive Mapping

Original artifacts that are evidence-bearing but not public-safe should be retained through private/original archive or external archive references.

Archive mapping must not hide negative results, failed states, unsupported states, or missing artifacts. It only separates public hygiene from raw traceability.

## 12. Reporting Discipline

Reports must remain role-aware and denominator-aware. PORT evidence, verifier support, observability evidence, same-engine rewrite evidence, and timing evidence must not be collapsed into a single leaderboard.

Performance claims require exact and timed rows. Hard negatives are checker controls, not method-generated failures.
