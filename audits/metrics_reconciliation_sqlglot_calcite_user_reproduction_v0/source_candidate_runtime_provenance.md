# Source/Candidate Runtime Provenance

New user-side reproduction runtimes come from per-row timing JSON files under `output/results/<run_id>/timing/<engine>/rows/`. Each timing JSON stores `source_runtime_samples_ms`, `candidate_runtime_samples_ms`, medians, requested/measured repetitions, warmup count, timeout, cache policy, schema setup policy, execution order policy, and environment metadata path.

Source runtimes in the new reproduction are newly measured during the nightly user-side evaluation pipeline. Candidate runtimes are also newly measured during the same pipeline. They are not reused from prior canonical runs.

The new timing policy recorded `measured_repetitions=2`, `warmup_count=1`, `timeout_seconds=30.0`, `schema_setup_policy=fresh_schema_per_timing_row`, `execution_order_policy=source_then_candidate`, and `cache_policy=recorded_not_controlled`. Prior canonical timing policies recorded `measured_repetitions=5` with the same high-level policy ID.

DB/environment metadata is present through `timing/<engine>/environment_metadata.json` and per-row `environment_metadata_path` fields, but cache effects remain recorded-not-controlled. This provenance is sufficient for local diagnostic interpretation and insufficient for paper-facing replacement without separate metric-definition and promotion authorization.
