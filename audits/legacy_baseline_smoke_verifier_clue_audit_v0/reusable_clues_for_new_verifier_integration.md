# Reusable Clues For New Verifier Integration

## Safe To Reuse As Design Clues

- Candidate selection: `CONS_0007` first, `CONS_0035` secondary/caveated.
- Static SQL-shape signals: aggregates, EXISTS, correlated subquery risk, interval/date literals, LIMIT/OFFSET, nested SELECT, window functions.
- Guardrail posture: verifier support is support-only, not rewrite generation, speedup, or leaderboard.
- Pair roles: source-positive and source-negative map well to the new `source_vs_positive` and `source_vs_hard_negative` pair types.
- SQLSolver verdict mapping: `EQ`, `NEQ`, `UNKNOWN`, `TIMEOUT`.
- VeriEQL JSONL input shape: `index`, metadata fields, `schema`, `constraint`, `pair`.
- Timeout ideas: SQLSolver 60s wall timeout and Z3 10000 ms; VeriEQL 600s bounded module-mode timeout.
- Constraint bridge warning: empty constraints can create misleading refutations; explicit constraint policy is required.

## Not Safe To Reuse Directly

- Any legacy SQLSolver or VeriEQL output as official Semantic Equivalence Rate.
- Any legacy support rate as a new-repo metric.
- Temporary `/tmp` tool paths as stable command paths.
- Legacy generated files as retained evidence without mapping.
- Static readiness output as proof of tool availability.

## Integration Notes For Current Wrappers

The current release wrappers accept external command paths and produce D035-shaped local verifier outputs. The legacy VeriEQL source is not directly compatible with the current wrapper because VeriEQL expects JSONL batch input through `parallel.cli_within_timeout`, not direct `source.sql candidate.sql` arguments.

A future VeriEQL adapter compatibility task should:

- accept `SQLRB_VERIEQL_ROOT`
- build JSONL pair input
- run `python -m parallel.cli_within_timeout` from the VeriEQL root
- pass `-f`, `-t`, and `-o`
- parse output JSONL
- preserve fail-closed local-only behavior

A future SQLSolver task should prefer external command-path reuse over vendoring. If a jar path is used, the task must explicitly define the Java/Z3 invocation contract and raw artifact retention.
