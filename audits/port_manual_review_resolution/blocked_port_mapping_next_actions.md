# Blocked PORT Mapping Next Actions

Date: 2026-05-15

## Recommendation

Do not move directly into full Common-core 40 migration.

Recommended next phase:

1. Design a formal case package validator.
2. Use that validator in one copy-first full case migration pilot.
3. In parallel or before scaling, close the reports/results retained-evidence map.

## Option A: Full Copy-First Case Migration Pilot Using PORT_0004

What it would test:

- Full target case package layout without the extra sanitized Spark plan-evidence complication.
- Copy-first migration mechanics for source SQL, rewrites, schema, checker, validation, manifest, provenance, and evidence index wiring.

Why it is useful:

- `PORT_0004` was cleared earlier and is lower-risk than the six blocked Spark-plan cases.
- It can test the full migration workflow with less public-hygiene complexity.

Risk:

- It may under-test sanitized retained evidence behavior because it was not one of the Spark local-path blocked cases.

Touches legacy repo:

- Read-only source access only if done correctly; writes should remain in the release repo.

Denominator/paper-results risk:

- Low if migration is copy-first and no case-set, denominator, result, or admission files are changed.

Recommended priority:

- Priority 2. Good first physical pilot if the validator exists or is developed alongside it.

## Option B: Full Copy-First Case Migration Pilot Using PORT_0008

What it would test:

- Full target case package layout plus integration of already-realized sanitized retained Spark plan evidence.
- Transition from evidence-mapping pilot slice to full case package migration.

Why it is useful:

- `PORT_0008` was the first accepted formal evidence-mapping pilot.
- It exercises the migration path most relevant to the blocked-PORT closeout series.

Risk:

- Higher than `PORT_0004` because it tests full migration plus sanitized evidence integration.
- The earliest pilot has a slightly older metadata shape, so the validator should accept or normalize that before physical migration.

Touches legacy repo:

- Read-only source access only if done correctly; writes should remain in the release repo.

Denominator/paper-results risk:

- Low to medium. Risk remains controlled if the pilot forbids case-set, denominator, result, and paper-table changes.

Recommended priority:

- Priority 3. Use after validator design, or after a lower-risk `PORT_0004` pilot if extra caution is preferred.

## Option C: Design A Formal Case Package Validator Before Full Case Migration

What it would test:

- Required target package fields.
- YAML/JSON parse checks.
- Public-hygiene scans.
- `runs_retention.yaml` required semantics.
- Denominator, paper-result, case-membership, and raw-evidence non-change assertions.

Why it is useful:

- It prevents every future physical pilot from relying only on manual checklist review.
- It gives a reusable gate before any Common-core 40 migration.

Risk:

- It delays physical migration slightly.
- It may need iteration as real migrated packages expose edge cases.

Touches legacy repo:

- No writes. It can be developed entirely in the release repo.

Denominator/paper-results risk:

- Very low. It should reduce future denominator and paper-result risk.

Recommended priority:

- Priority 1. Do this before scaling and preferably before the first full physical migration pilot.

## Option D: Close Reports/Results Retained-Evidence Map

What it would test:

- Which reports/results artifacts are paper-facing retained evidence.
- Which files are scratch, logs, local workspaces, timing outputs, or generated intermediates.
- How paper evidence can be referenced without importing private/local residue.

Why it is useful:

- Reports/results are a known blocker for public release hygiene.
- It is needed before final paper-facing public release closure.

Risk:

- Reports/results may contain mixed provenance and local paths requiring careful classification.
- It could expand scope if not constrained to mapping only.

Touches legacy repo:

- Read-only inspection only if done correctly; writes should be audit outputs in the release repo.

Denominator/paper-results risk:

- Medium if report numbers are edited. Low if the task is mapping-only and explicitly forbids changing paper results.

Recommended priority:

- Priority 2. Can proceed in parallel with validator design, but should stay mapping-only until a migration policy is approved.
