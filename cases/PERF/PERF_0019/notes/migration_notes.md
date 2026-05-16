# PERF_0019 Migration Notes

Migration date: 2026-05-16.

This package was migrated using a copy-first release-repo process. The legacy repository was read-only and unchanged. Performance boundary: no timing run, speedup claim, latency claim, ranking claim, leaderboard claim, or paper-result claim was created. Hard-negative static explanation: The hard negative changes the excluded order-comment phrase, altering the left-join count distribution on the retained witness. Spark plan evidence was sanitized for local temporary paths and raw legacy plans remain mapped as do-not-delete originals. Validation scripts are retained legacy validation assets and future public runner output must not write to case-local `runs/` by default. Denominator and paper results are unchanged.
