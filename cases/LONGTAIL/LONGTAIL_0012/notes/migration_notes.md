# Migration Notes: LONGTAIL_0012

- Migration date: 2026-05-16.
- Copy-first principle: public-safe SQL, schema, witness load scripts, retained result checks, and retained plan summaries were copied from legacy evidence into canonical paths.
- Legacy unchanged: the source repository and raw legacy evidence were not modified.
- Structural boundary: this LONGTAIL case contributes structural robustness evidence for optional vote-count enrichment with windowed ranking and outer-join row preservation.
- Workload-frequency boundary: workload_frequency_claim_created is false and production_frequency_claim_created is false.
- Benchmark-result boundary: migration did not create a new benchmark result, timing claim, ranking claim, speedup claim, or leaderboard claim.
- Hard-negative approval: maintainer approved neg_01 expected rejection reason `optional_vote_count_left_join_changed_to_inner_join` for public-release migration.
- Spark plan handling: raw Spark plan text remains mapped as legacy evidence, while public retained Spark plans use sanitized copies with local path traces removed.
- Validation script caveat: copied scripts are retained legacy validation assets; they were not executed during migration; future public runner outputs must not write to case-local `runs/` by default.
- Boundary statement: denominator, paper results, Common-core membership, case_sets, reports, results, and raw legacy evidence are unchanged.
