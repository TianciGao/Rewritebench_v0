# Validation Notes

Smoke validation:

- User-facade command exited 0.
- Selected rows: 2.
- Candidate generated rows: 2.
- Candidate preflight passed rows: 2.
- Failure bucket: `none=2`.
- Adapter metadata present for both rows.
- Adapter metadata showed `provider=fake`, `live_call=false`, and
  `api_key_present=false`.

Required validation:

- `pytest tests/user_entry/test_direct_llm_repair_1_adapter.py -q`: passed,
  `8 passed`.
- `python -m py_compile baselines/direct_llm_repair_1/adapter.py`: passed.
- CSV parse checks: passed.
- Markdown/text non-empty checks: passed.
- no-live review: passed.
- no DB/checker/timing/local_metrics/verifier command review: passed.
- no runtime outputs staged: passed.
- `git diff --check`: passed.
- changed-file secret scan: passed.
- protected-path review: passed.

No new user-facade test file was needed for this smoke.

Runtime cleanup:

- The temporary source run under
  `runs/user/direct_llm_repair_1_fake_provider_user_facade_smoke_v0` was
  removed before commit.
- `/tmp` runtime outputs were not committed.
