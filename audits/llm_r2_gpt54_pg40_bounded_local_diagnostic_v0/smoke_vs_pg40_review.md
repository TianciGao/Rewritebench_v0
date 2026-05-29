# Smoke vs PG40 Review

Prior 6-row smoke from `audits/llm_r2_gpt54_bounded_live_e2e_smoke_v0/`:

- selected: 6
- generated: 6
- executable: 5
- exact: 5
- timed: 5
- frontier: `LONGTAIL_0011` candidate_execution_failed

Current PG40 diagnostic from `local_metrics.py` and run ledger:

- selected: 40
- generated: 40
- executable: 39
- exact: 39
- timed: 34
- frontier: LONGTAIL_0011=candidate_execution_failed

Live GPT-5.4 outputs can drift across reruns. The PG40 metric values above come from `local_metrics.py`; no route metrics were hand-computed.
