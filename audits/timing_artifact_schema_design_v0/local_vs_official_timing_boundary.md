# Local Versus Official Timing Boundary

Future local timing diagnostics may produce timing artifacts under `runs/user/`, but those artifacts are not official retained evidence and are not paper metric inputs by default.

## Local Diagnostic Timing

Local timing diagnostics may be useful for:

- smoke-testing timing collection mechanics;
- checking exact-gated timing eligibility;
- validating source/candidate sample retention;
- exercising timeout and N.A. handling;
- preparing a non-official local metrics calculator.

Local timing diagnostics must remain:

- `local_diagnostic_only=true`;
- `official_metric_input=false`;
- `paper_result_input=false`;
- `retained_evidence_promoted=false`;
- `leaderboard_input=false`.

## Official Promotion Boundary

Promotion to official retained timing evidence requires a separate authorized task that defines:

- retained artifact path and retention policy;
- official environment requirements;
- approved timing policy;
- exact source/candidate pairing rules;
- provenance and hash requirements;
- denominator and route identifiers;
- validation gates;
- paper table rendering handoff.

No local `runs/user/` timing artifact should be treated as official evidence without that promotion gate.

## Reports And Results Boundary

This design does not update `reports/`, `results/`, paper tables, or any leaderboard. Future local timing artifacts must not write those surfaces unless a separate reports/results or official metrics task authorizes it.

## Speedup Boundary

This task does not compute speedup. The schema includes `speedup_ratio` as a future nullable field so that a later exact-gated timing implementation can record row-level speedup only when paired samples are complete and medians are positive.
