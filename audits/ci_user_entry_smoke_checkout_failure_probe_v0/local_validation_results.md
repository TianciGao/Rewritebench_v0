# Local Validation Results

Local reproduction:
- The checkout failure did not reproduce locally.
- Local repository state was clean before validation.
- The branch was confirmed as `feature/case-package-v2-external-schema`.
- Commit `0c53cc7d492bc14cf4bf9d97506ce86e002b4976` was confirmed to be contained in `origin/feature/case-package-v2-external-schema`.

Commands and results:
- `python -m pip install -e .`: passed.
- `python -m pip install pytest PyYAML`: passed; requirements already satisfied.
- `python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.

User-entry smoke output summary:
- Module help: passed.
- Wrapper help: passed.
- User-entry pytest suite inside the smoke script: passed.
- Dry-run smoke: passed.
- Dummy adapter smoke: passed.
- Protected paths unchanged check: passed.
- `runs/user` smoke outputs unstaged check: passed.

Ledger fixture smoke output summary:
- Fixture rows checked: 38.
- Expected-valid passed: 17.
- Expected-invalid failed as expected: 21.
- Unexpected pass/fail: 0/0.
- Production retained evidence parsed: false.
- Metrics computed: false.
- Adapter implemented: false.

Cleanup:
- The editable install produced local `src/sql_rewrite_bench.egg-info/`; it was removed.
- The ledger smoke refreshed a generated tracked smoke report; that validation-only refresh was restored because it is outside this task's allowed modifications.

Conclusion:
- Local validation supports that the failing CI run did not reach Python/tests and does not indicate a local user-entry smoke regression.

