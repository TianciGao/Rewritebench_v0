# Failure Log Excerpt

Full GitHub Actions logs were not available from this workspace:

```text
$ gh run view 26357910722 --job 77587924607 --log
/bin/bash: line 1: gh: command not found
```

Local CI-equivalent reproduction:

```text
$ python scripts/dev/run_user_entry_ci_smoke.py
[run] module help
[pass] module help
[run] wrapper help
[pass] wrapper help
[run] user-entry tests via pytest
[fail] user-entry tests via pytest: exit 1
...
FAILED tests/user_entry/test_user_run_outputs.py::UserRunOutputTests::test_documented_examples_match_current_cli_options
1 failed, 238 passed, 1 skipped, 15 subtests passed
```

Failure class:

- The smoke script failed during the user-entry pytest suite.
- The failure occurred before dry-run smoke and dummy adapter smoke.
- The public Node.js 20 warning was not implicated by local reproduction.

Relevant assertion:

- The test expected old internal runner documentation options in `docs/USER_BENCHMARK_GUIDE.md`.
- The guide now documents the D035 facade options and exported output contract.
