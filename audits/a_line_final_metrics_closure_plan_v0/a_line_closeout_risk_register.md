# A-line Closeout Risk Register

## Official Limited Status Metrics Mistaken For Full Benchmark Suite

Risk: Execution Coverage Rate and Result Consistency Rate are official only in a limited status scope. They can be mistaken for the complete benchmark metric suite.

Mitigation: label them as limited official status metrics and keep all blocked/N.A./post-release metrics visible.

## Generation Rate Blocked But Hidden

Risk: A renderer or summary could omit Generation Rate or silently treat it as zero.

Mitigation: report Generation Rate as blocked with `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.

## Timing/Performance Mixed Too Early

Risk: raw timing artifacts could be treated as GM_Speedup or percentile inputs before timing eligibility is approved.

Mitigation: keep timing/performance in blocked or N.A. treatment until a timing adapter and validation policy are separately authorized.

## Semantic Equivalence Overclaimed From Verifier Support

Risk: result consistency or unvalidated verifier references could be described as semantic equivalence.

Mitigation: require verifier_support_pair rows and decidability policy before Semantic Equivalence Rate.

## Attribution Coverage Overclaimed Before Annotation Pipeline

Risk: plan availability or LLM-proposed explanations could be counted as Attribution Coverage.

Mitigation: defer Attribution Coverage to post-release attribution schema and validation work.

## Cross-engine Metrics Overclaimed From Bounded PORT Evidence

Risk: PORT or same-engine evidence could be reused as Cross-Engine Execution or Cross-Engine Consistency.

Mitigation: require portability_candidate_cell adapter and separate portability denominator policy.

## Speedup Retention Computed Without Paired Timing

Risk: Speedup Retention could be inferred from source timing or target timing alone.

Mitigation: report N.A. for v0 until paired result-consistent source/target timing exists.

## Reports/Results Mutated Before Renderer Authorization

Risk: planning files could become report outputs by path drift.

Mitigation: keep all A-line closure artifacts under `audits/` and require separate renderer authorization before any `reports/` or `results/` writes.

## Global Leaderboard Pressure

Risk: method comparisons could collapse denominator families and evidence completeness into one ranking.

Mitigation: enforce Metrics Contract v1 and D009; no global leaderboard or winner language.
