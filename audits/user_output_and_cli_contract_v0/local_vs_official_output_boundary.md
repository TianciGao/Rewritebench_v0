# Local vs Official Output Boundary

`output/` is for local/user-run outputs.

`output/` artifacts are not:

- official metrics;
- paper results;
- retained evidence;
- leaderboard inputs;
- top-level official `reports/` or `results/` updates.

Top-level `reports/` and `results/` remain official/paper/release-facing surfaces and must not be touched by user-run tasks unless a separate official reporting or promotion task is authorized.

Promotion from `output/` to official `reports/`, `results/`, or retained evidence requires a separate task that validates route identity, denominator identity, environment metadata, verifier/timing evidence, artifact paths, and claim boundaries.

No leaderboard output is allowed.
