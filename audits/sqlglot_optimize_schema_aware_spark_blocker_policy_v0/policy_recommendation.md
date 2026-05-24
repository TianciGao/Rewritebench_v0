# Policy Recommendation

## CONS_0005 / Spark

Classification:

- `spark_semantic_mismatch_candidate`
- `true_candidate_semantic_drift`

Recommendation:

- keep as mismatch;
- do not normalize;
- do not time;
- block larger Spark schema-aware optimize trial until this semantic rewrite behavior is understood.

Reason:

- source row count is 0;
- candidate row count is 1;
- value mismatch reason is `row_count_mismatch`.

## CONS_0036 / Spark

Classification:

- `spark_label_only_mismatch_candidate`
- `checker_normalization_policy_candidate`

Recommendation:

- keep as mismatch for this task;
- consider a future explicit label-normalization policy task;
- candidate future policy should be narrow, Spark-aware, and value-gated.

Minimum future policy guardrails:

- require row count equality;
- require value equality before label relaxation;
- limit to label case differences unless separately justified;
- keep local diagnostic and official/paper surfaces separate;
- add tests for same-engine default behavior and any cross-dialect normalization gates.

## Do Not Implement Now

Checker normalization should not be implemented in this task. This packet records policy readiness only.

## Route Status

`sqlglot_optimize_schema_aware` is ready for exact-gated timing over the current six exact rows only. It remains partial for broader Track A local diagnostics.
