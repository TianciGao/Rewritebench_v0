# Rewritebench_v0

Clean public-release construction repository for SQL-RewriteBench.

## Run Your Own Rewrite Adapter

The current B-line user-entry MVP supports non-DB adapter capture for Common-core v0 case-engine rows. It resolves selections from release metadata, invokes a user adapter command, and writes local experiment outputs only under `runs/user/<run_id>/`.

See [docs/USER_BENCHMARK_GUIDE.md](docs/USER_BENCHMARK_GUIDE.md).

Current user-entry limits: no DB execution, no checker execution, no timing, no official metrics, no paper results, no retained evidence update, and no global leaderboard.
