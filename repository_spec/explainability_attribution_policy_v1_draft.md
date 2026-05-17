# Explainability Attribution Policy v1 Draft

Status: draft, not implementation-authorizing

Purpose: define the boundary between the main explainability metric, support designs, LLM annotations, and evidence validation.

This draft does not implement Attribution Coverage, parse plans, compute scores, run LLM calls, render reports, change metrics, update paper tables, or create speedup claims.

## Main Explainability Metric

`Attribution Coverage` is the main explainability metric in Metrics Contract v1.

Draft definition: fraction of attribution-eligible cases with sufficient operator-level attribution evidence from structured plan/SQL analysis.

Attribution evidence should explain which SQL or plan-level operator, predicate, join, aggregation, projection, ordering, limit, portability adaptation, checker guard, or verifier-supported relation supports the rewrite claim.

## Pilot / Support Design

The atom-based Rewrite Opportunity Observability Score is a pilot or support design. It may help structure future attribution analysis, but it is not the main metric unless separately approved.

PlanFrontier, PlanAvailability, plan artifacts, failure-stage visibility, and checker/verifier evidence are support inputs. They may appear in diagnostic tables or evidence summaries, but they do not replace Attribution Coverage.

## Attribution Evidence Layers

### `human_verified`

Attribution reviewed and approved by a maintainer or designated reviewer.

This is the highest-confidence attribution layer.

### `evidence_supported`

Attribution supported by retained public-safe evidence such as SQL structure, checker configuration, verifier support evidence, result comparison summaries, or sanitized plan artifacts.

This layer may be sufficient for future automated reporting if the attribution schema and validation gates are approved.

### `llm_proposed`

Attribution proposed by an LLM or other annotation helper.

This layer is not validation evidence by itself. It must be marked as proposed and must not be counted as attribution coverage unless supported by retained evidence or human verification under an approved policy.

## LLM Annotation Boundary

LLM annotations may be used as draft explanations only if a future approved workflow permits them.

LLM output must not:

- create benchmark results;
- validate correctness;
- validate semantic equivalence;
- create speedup claims;
- replace structured plan/SQL evidence;
- expose prompts, API keys, model traces, or private data in public artifacts.

## Evidence Validation Boundary

Attribution Coverage requires structured evidence validation before computation. Acceptable support may include:

- public-safe SQL source and candidate paths;
- checker expected-rejection records;
- retained result comparison summaries;
- verifier support records for Semantic Equivalence Rate;
- public-safe plan artifacts;
- failure-stage and failure-type records;
- human-reviewed attribution notes.

Unknown, unsupported, archive-only, missing, or private-only evidence should be reported separately and not silently counted as covered.

## No Speedup Claim Without Plan Or Runtime Evidence

Explainability evidence does not create speedup evidence.

No speedup, Speedup Retention, or performance-improvement claim may be made without result-consistent timing evidence under the Metrics Contract v1 performance rules.

Plan artifacts can support attribution, but they do not by themselves prove runtime improvement.

## N.A. And Deferred Conditions

Attribution Coverage should be `N.A.` when:

- attribution-eligible denominator is not defined;
- attribution schema is not implemented;
- required structured evidence is absent;
- evidence is private/archive-only and no public-safe summary exists;
- the method/scope is outside explainability support.

## Implementation Boundary

Implementation is deferred. A future task must define attribution schema fields, adapter extraction rules, validation checks, and public reporting tables before Attribution Coverage can be computed.
