# PERF_0033 Migration Notes

Migration date: 2026-05-16.

This migration used a copy-first canonical-layout process. The legacy repository was not modified. The hard-negative explanation is static-inferred as `manager_id_predicate_changed`: changes the item manager predicate from i_manager_id = 36 to i_manager_id = 37. Raw Spark plan text was not copied into public retained evidence; sanitized public copies redact local temporary paths and map originals as do-not-delete legacy artifacts. Validation scripts are retained legacy validation assets and were not executed; future public runner output must not write to case-local `runs/` by default. Denominator and paper results are unchanged. No speedup or timing claim was created.
