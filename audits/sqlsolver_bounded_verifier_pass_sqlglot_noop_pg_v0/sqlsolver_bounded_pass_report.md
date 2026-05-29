# SQLSolver Bounded Pass Report

## Subset Selection Policy

The subset was selected deterministically from `audits/track_a_120_verifier_pair_materialization_plan_v0/verifier_pair_materialization_manifest.csv`, filtered to `route_id=sqlglot_noop`, `run_id=sqlglot_noop_track_a_120_canonical_v0`, and `engine=postgres`. The selector sorted by case id within each pool and chose the first two eligible exact/result-consistent rows from each available pool: `CONS`, `LONGTAIL`, `PERF`, and `PORT`.

Selected pairs: `8` from `35` available SQLGlot no-op PostgreSQL exact/result-consistent manifest pairs.

## Commands Used

SQLSolver was invoked through the external JAR command shape with redacted paths:

```bash
java -jar [external_sqlsolver_jar] -sql1=[sql1_input] -sql2=[sql2_input] -schema=[schema_input] -output=[sqlsolver_output]
```

The current shell did not provide SQLSolver-specific env vars. The previously staged external SQLSolver root/JAR/lib were present outside the release repository and were used with redacted provenance. Java was available.

## Identity Guard Summary

- `CONS_0005`: source_identity=`equivalent`, candidate_identity=`equivalent`, passed=`true`
- `CONS_0007`: source_identity=`equivalent`, candidate_identity=`equivalent`, passed=`true`
- `LONGTAIL_0011`: source_identity=`unknown`, candidate_identity=`unknown`, passed=`false`
- `LONGTAIL_0012`: source_identity=`equivalent`, candidate_identity=`equivalent`, passed=`true`
- `PERF_0006`: source_identity=`unknown`, candidate_identity=`equivalent`, passed=`false`
- `PERF_0007`: source_identity=`unknown`, candidate_identity=`unknown`, passed=`false`
- `PORT_0003`: source_identity=`unknown`, candidate_identity=`unknown`, passed=`false`
- `PORT_0005`: source_identity=`unknown`, candidate_identity=`unknown`, passed=`false`

Identity guard passed pairs: `3`

Identity guard failed pairs: `5`

Blocked actual checks:

- `LONGTAIL_0011`: source_identity=unknown; candidate_identity=unknown
- `PERF_0006`: source_identity=unknown; candidate_identity=equivalent
- `PERF_0007`: source_identity=unknown; candidate_identity=unknown
- `PORT_0003`: source_identity=unknown; candidate_identity=unknown
- `PORT_0005`: source_identity=unknown; candidate_identity=unknown

## Actual Source-Candidate Verdict Summary

Actual source-candidate checks were executed only after both identity guards returned `equivalent`.

- `CONS_0005`: `equivalent` (0.88313s)
- `CONS_0007`: `equivalent` (0.949885s)
- `LONGTAIL_0012`: `equivalent` (1.144278s)

Counts over actual attempted checks:

- `equivalent`: `3`
- `non_equivalent`: `0`
- `unknown`: `0`
- `timeout`: `0`
- `unsupported`: `0`
- `tool_error`: `0`

## Tool Behavior

SQLSolver behaved consistently with prior coverage-limited expectations: deterministic core CONS and one LONGTAIL pair passed identity guards and verified equivalent, while several LONGTAIL/PERF/PORT rows returned `unknown` even for identity checks. That makes this pass useful as bounded verifier-support evidence, but too coverage-limited to justify SER promotion or a broad all-route verifier run.

## Broader Pass Advisability

Do not proceed directly to a full SQLGlot no-op PostgreSQL SQLSolver pass as a metric-producing activity. The next safe step is a modeling-gap triage packet for the identity-guard `unknown` rows, especially `PERF_0006`, `PERF_0007`, `PORT_0003`, `PORT_0005`, and `LONGTAIL_0011`. A larger pass may be safe only after deciding whether `unknown` identity guards are expected SQLSolver limitations, schema modeling gaps, or input-shaping issues.

VeriEQL should still wait. This SQLSolver-first bounded pass already exposed enough verifier-support coverage limits to triage before adding another verifier.

## Why This Is Not Official SER

This packet is bounded local diagnostic verifier-support evidence only. `bounded_SER_if_decidable=1.0` is computed only over `3` decidable actual source-candidate checks in this small subset and is explicitly not official SER, not a paper metric, not retained evidence, and not a leaderboard input.
