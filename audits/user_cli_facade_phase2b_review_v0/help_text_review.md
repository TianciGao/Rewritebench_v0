# Help Text Review

The command-level help for every implemented `sqlrb user ...` command was reviewed after hardening:

- `evaluate`
- `list-cases`
- `explain-selection`
- `show-output-schema`
- `show-boundary`
- `compute-local-metrics`
- `summarize`

Each command now includes the shared boundary:

> Boundary: local diagnostic output only; no official metrics, paper results, retained-evidence promotion, or leaderboard output.

The top-level facade description also states that commands write local diagnostic outputs only and do not compute official metrics, paper results, promote retained evidence, or create leaderboard output.

Verifier help for `evaluate` now states that verifier flags are reserved for future support and that Semantic Equivalence Rate remains `N.A.` without verifier evidence.
