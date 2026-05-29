# Local Metrics Summary Review

Copied from `runs/user/direct_llm_repair_1_track_a_120_canonical_v0/metrics/local_metrics_summary.json` and the user-facing `/tmp` metrics copy.

Counts:

```text
selected=120
candidate_generated=120
preflight_passed=120
source_executable=115
candidate_executable=115
exact=111
mismatch=4
unsupported_fail_closed=5
timing_eligible=98
timed=98
speedup_denominator=98
```

Rates:

```text
generation_rate=1.0
execution_coverage_rate=0.9583333333333334
result_consistency_rate=0.925
```

Performance:

```text
gm_speedup_ratio=0.9978498743494606
speedup_p10=0.9350245899377606
speedup_p25=0.9941671005127753
speedup_p50=1.0037084775530145
speedup_p75=1.0119714589375732
speedup_p90=1.0704591883635644
```

Deferred diagnostics:

```text
semantic_equivalence_rate_status=not_applicable; reason=formal_verifier_evidence_missing
pocr_status=not_applicable; reason=external_skill_adapter_pending
```

Boundary: these are non-official local diagnostic metrics only.
