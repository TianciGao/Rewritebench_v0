# Direct LLM Repair-1 Fake-Provider User-Facade Smoke

Task: `direct_llm_repair_1_fake_provider_user_facade_smoke_v0`

This packet records a tiny D035 user-facade smoke for the Repair-1 scaffold.
The run invoked `baselines/direct_llm_repair_1/adapter.py` through the user
evaluation facade by way of a temporary `/tmp` wrapper that supplied explicit
per-row original-candidate and feedback fixture paths.

Smoke result:

- Selected rows: 2
- Candidate SQL outputs generated: 2
- Candidate preflight passed: 2
- DB execution: not enabled
- Checker: not enabled
- Timing: not enabled
- local_metrics.py: not run
- Verifier: not run
- Live LLM calls: none

Rows used:

- `CONS_0005 / spark` with `checker_mismatch_feedback`
- `LONGTAIL_0012 / spark` with `candidate_execution_error_feedback`

Unsupported-engine rows were not included. The five unsupported Spark boundary
rows from the Direct LLM original frontier remain excluded from Repair-1.

Runtime artifacts were written only under `/tmp` and a temporary local
`runs/user/direct_llm_repair_1_fake_provider_user_facade_smoke_v0` source run
that was reviewed and removed before commit. No runtime outputs are committed.
