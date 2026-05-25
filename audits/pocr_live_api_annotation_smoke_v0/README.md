# POCR Live API Annotation Smoke v0

This packet records a bounded live API smoke for POCR Stage A annotation only, plus fail-closed Stage B review.

Selected cases:

- `PERF_0006`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Candidate input:

- Existing route-labeled local candidate SQL artifacts from `runs/user/common_core_pg_noop_db_checker/candidate_sql/`.
- Candidate route label: `common_core_pg_noop_db_checker`.
- Method label: `noop_adapter`.
- The files were read only. No baseline was run or rerun.

Live call result:

- Provider label: `openai_compatible`.
- Model label: `gpt-5.4`.
- Live calls attempted: 4.
- Schema-valid Stage A annotations: 3.
- Schema/JSON failure: 1 (`PERF_0006`, malformed JSON from provider response).

Stage B result:

- `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` remained `insufficient_evidence`.
- `PERF_0006` remained `schema_invalid`.
- No atom was promoted to official POCR numerator.
- No route-level POCR was aggregated.

Boundaries:

- No DB/checker/timing run.
- No baseline rerun.
- No user-output integration.
- No official Positive Operation Coverage Rate computation.
- No paper-facing reports/results update.
- No case package or `skills.md` modification.
- No `skill/` folder created.
- No `output/`, top-level `reports/`, top-level `results/`, or `runs/` files modified by this task.

Next safe action: after reviewing this live smoke, design a bounded candidate-source resolver and diagnostic POCR draft runner, still separate from user-output integration.
