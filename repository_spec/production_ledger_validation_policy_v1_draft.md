# Production Ledger Validation Policy v1 Draft

Status: draft validation-gate policy, not implementation-authorizing

## Purpose

Define the validation gates that any future production evidence ledger must pass before it can be used by retained-evidence adapters, metrics computation, paper table rendering, reproduction CLI, public runner outputs, or clean public reports.

This policy turns the synthetic ledger fixture validator into a pre-production smoke layer and defines the stricter gate sequence needed for real adapter output. It does not implement a production ledger validator and does not authorize production retained-evidence parsing.

## Non-goals

- Do not parse production retained evidence.
- Do not implement retained-evidence adapters.
- Do not implement metrics computation.
- Do not implement a reproduction CLI or public runner.
- Do not render paper tables.
- Do not migrate reports/results.
- Do not create production ledger files.
- Do not change denominators, case membership, paper results, or raw legacy evidence.

## Relation To Synthetic Fixture Validator

`scripts/dev/validate_ledger_fixtures.py` and `scripts/dev/smoke_ledger_fixtures.py` are fixture-only smoke gates. They validate synthetic rows, record-type rules, safety flags, status vocabulary, and static denominator joins.

Future production ledger validation must reuse the same policy concepts but must be separate from fixture smoke validation. Fixture smoke is the first gate; it is not evidence that real retained evidence has been parsed correctly.

## Production Ledger Input Assumptions

A future production ledger is expected to be emitted by separately authorized retained-evidence adapters. A validator should accept a materialized ledger file and static release scaffolds:

- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `case_sets/common_core_v0/controls_360.csv`
- `inventory/case_registry.csv`
- any approved portability or verifier support denominator references once defined

The validator must be non-mutating. It should read the ledger and scaffolds, write validation reports to an explicit audit output directory, and fail closed on unsafe or ambiguous rows.

## Schema Gates

Production ledgers must pass:

- Required-column checks against `evidence_ledger_column_schema_v1_draft.md`.
- Allowed `record_type` vocabulary checks.
- Field type checks for booleans, enumerations, numeric timing fields, paths, IDs, and status fields.
- Nullable policy checks, including required explanations for missing values.
- Stable `record_id`, `candidate_id`, `artifact_id`, and `support_pair_id` checks by row type.
- Forbidden-field combination checks such as timing fields on verifier rows or speedup fields on control rows.
- Duplicate identity checks at the row grain.

## Record-type Gates

Every row must have exactly one `record_type` and must satisfy that type's required and forbidden field rules.

Required record types:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

Support-only rows must remain support-only unless a later policy explicitly promotes them. Control rows, plan artifacts, verifier support pairs, and retained summaries must not become rewrite-method performance rows.

## Denominator Gates

Validation must preserve denominator boundaries:

- Same-engine rewrite rows must join to the Track A 120 planned denominator scaffold.
- User-run rows are benchmark-scoped only when they join to the approved Track A denominator.
- Control rows must join to the `controls_360.csv` scaffold and must not use Track A denominator IDs.
- PORT portability rows use portability-specific semantics and must not silently join to Track A same-engine rows.
- Verifier support pairs use support-pair semantics and must not be treated as rewrite-generation baselines.
- Plan artifacts and retained summary rows are not metric denominator rows by default.

No validation or later metric layer may create a global leaderboard that mixes incompatible denominator families.

## N.A. And Unsupported Status Gates

Production rows must preserve explicit missingness and non-applicability. The validator should accept only approved status values and require them to appear in the right fields.

Required status handling includes:

- `unsupported`
- `not_applicable`
- `unknown`
- `verifier_unknown`
- `timing_missing`
- `target_timing_missing`
- `evidence_not_retained`
- `manual_review_required`
- `blocked`
- `failed`
- `mismatch`
- `exact`
- `N.A.`

Missing timing must not be converted to zero. `N.A.` must not be converted to failure. Unknown verifier support must not be counted as semantic-equivalence failure unless a later approved metric policy changes that rule.

## Metric-readiness Gates

Production ledger validation does not compute metrics, but it must confirm whether a ledger contains the fields required by Metrics Contract v1.

Primary metric readiness gates:

- Generation Rate: `generated`, denominator, method, case, engine, and candidate identity fields present for candidate rows.
- Execution Coverage Rate: `executed` and execution status fields present.
- Result Consistency Rate: executed-result and checker fields present.
- Semantic Equivalence Rate: result-consistent candidate rows link to verifier support or explicit verifier unknown status.
- GM_Speedup: result-consistent timed rows have valid timing fields and timing eligibility.
- Speedup Ratio Percentiles: same readiness as GM_Speedup, with enough validated speedup ratios for later percentile computation.
- Attribution Coverage: attribution-eligible rows must link to approved attribution evidence or render `N.A.` until the attribution schema is implemented.
- Cross-Engine Execution: portability rows must identify source and target engine scope and execution status.
- Cross-Engine Consistency: portability rows must include target-engine consistency evidence after execution.
- Speedup Retention: paired source and target timing must exist or rows must explicitly render `target_timing_missing` or `N.A.`.

All metric computation remains blocked until these gates pass and metrics implementation is separately authorized.

## No-global-leaderboard Guard

Validators must reject or flag any ledger, summary, or metadata file that collapses:

- different `record_type` values;
- same-engine and portability denominators;
- control rows and rewrite candidate rows;
- verifier support rows and method-generated rows;
- support summaries and metric rows;
- engines or methods without explicit denominator-aware grouping.

## No-mutation Guard

Production ledger validation must not:

- write to `reports/`;
- write to `results/`;
- write into case-local `runs/`;
- update case packages;
- update `case_sets/`;
- update inventory files;
- alter retained evidence;
- alter denominator values;
- alter paper results.

Validation reports should be written only to an explicit audit output directory.

## Public Hygiene Guard

Future production ledgers must be public-safe before any clean export or curated retained-evidence publication. Validation should fail or require manual review for:

- absolute local paths;
- WSL, host-specific, or private workspace paths;
- raw stdout/stderr traces;
- prompt logs or model traces;
- API keys, tokens, credentials, or private endpoints;
- unsanitized raw debug logs;
- hidden production paths inside synthetic fixture outputs.

## CI And Developer Workflow Expectation

The synthetic fixture smoke workflow remains the lightweight CI gate for schema and validator development. A future production ledger validator should be a separate opt-in command and should not run in default CI until production ledger inputs are approved and public-safe.

Recommended workflow:

1. Run synthetic fixture smoke.
2. Build a production ledger only after adapter implementation is separately authorized.
3. Run production ledger validation.
4. Allow metrics computation only on a validated ledger and only after metrics implementation is separately authorized.
5. Allow paper table rendering only after metrics validation and separate renderer authorization.

## Future Implementation Phases

1. Define a non-mutating production ledger validator interface.
2. Implement schema and record-type validation against fixture-derived rules.
3. Add denominator scaffold joins.
4. Add public hygiene checks.
5. Add metric-readiness checks without computing metrics.
6. Add CI or scheduled validation only after production ledger inputs are approved.
7. Gate metrics, paper rendering, reproduction CLI, and public runner outputs on validation pass status.

## Explicit Authorization Boundary

This policy does not authorize production retained-evidence parsing, retained-evidence adapter implementation, metrics computation, reproduction CLI implementation, public runner implementation, paper table rendering, reports/results migration, denominator updates, paper-result updates, case membership changes, or raw legacy evidence modification.
