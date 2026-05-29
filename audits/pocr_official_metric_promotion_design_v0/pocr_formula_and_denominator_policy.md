# POCR Formula And Denominator Policy

This design preserves the current paper formula as the curated-subset formula while adding denominator-aware route-level views for promotion review.

Per-row operation coverage:

```text
OC_i = |Ahat_i| / |Aexp_i|
```

`Aexp_i` is the set of expected operation atoms for row `i`. It is sourced only from `operation_atom` entries in the case-local root-level `skills.md`.

`Ahat_i` is the subset of those operation atoms that receives Stage-B transformation-supported evidence.

Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No atoms may be inferred from taxonomy labels, SQL shape, positive SQL, source SQL, candidate SQL, retained evidence, or ad hoc analysis.

Stage A annotation alone is not counted. Candidate SQL spans, source SQL spans, and positive SQL spans alone are not sufficient. Stage B transformation-aware validation is required, and implementation support must include source-to-candidate transformation evidence.

## POCR@planned

```text
POCR@planned_r = mean over P_r of OC_i^fc
```

`P_r` is the planned POCR-eligible row set for route `r`.

`OC_i^fc = OC_i` when Stage B validates row evidence.

`OC_i^fc = 0` for no candidate, generation failure, extraction failure, route mismatch, candidate mismatch, annotation missing, or schema-invalid after retry.

Rows with no expected operation atoms are `not_applicable_no_expected_operation_atoms` and are counted separately rather than silently entering the denominator.

POCR@planned is the denominator-aware route-level headline candidate because it keeps planned failures visible.

## POCR@candidate

```text
POCR@candidate_r = mean over B_r of OC_i^fc
```

`B_r` is the candidate-bound row set with candidate SQL and deterministic `case_id`, `engine`, `method_id`, `route_id`, and `candidate_sha256` binding.

No-candidate rows are outside the POCR@candidate denominator, but candidate mismatch, route mismatch, annotation missing, and annotation fail-closed states remain explicit status rows when they occur after candidate binding.

POCR@candidate is a diagnostic candidate-quality view, not the only promotion view.

## POCR@curated

POCR@curated is deferred until a predeclared curated manifest exists. Until then it must be reported as `NA` / `curated_manifest_missing`.

The current paper formula remains the curated-subset formula. Once a frozen curated manifest exists and Stage-B-supported numerators are available, POCR@curated can be calculated from that manifest. It must not be invented after the fact from generated, executed, exact, or timed rows.

## Macro And Micro Averages

The main proposal uses per-row macro averaging: compute `OC_i` per row, then average across the selected denominator rows.

Do not compute POCR by total supported atoms divided by total expected atoms unless it is separately labeled as a micro-average diagnostic. That micro-average is not the current official proposal.

POCR@planned and POCR@candidate are the first two promotion views.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
