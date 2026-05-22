# Timing Protocol Alignment

This file proposes timing protocol defaults for a future design task. It does not implement timing.

## Core Principle

Timing is exact-gated and paired. A speedup ratio is interpretable only when the candidate is result-consistent and source/candidate timing is collected in the same engine, environment, and run context.

## Proposed Defaults

- Source/candidate pairing: required for every timed row.
- Engine context: source and candidate timings for same-engine rows must use the same engine.
- Cross-engine context: target-engine speedup requires target-engine source/reference timing and target-engine candidate timing in the same target engine context.
- Environment context: record machine, OS, Python, engine version, relevant engine connection settings, and run timestamp.
- Warmup count: default `1` warmup source/candidate pair, configurable.
- Repetitions: default `5` measured source/candidate pairs, configurable.
- Statistic for metric input: median runtime in milliseconds.
- Runtime sample arrays: retain full ordered sample arrays for source and candidate.
- Timeout: default should be route/engine configurable; timeout means no speedup ratio for that row.
- Failure/N.A.: missing, timed out, failed, inconsistent, or unsupported rows are not zero speedup and should be reported as N.A. for performance.
- Cache/connection assumptions: use the same connection/session policy for source and candidate within a row; record whether schema setup was reused.
- Reset assumptions: record whether transaction/session/cache reset was performed; do not claim cold-cache or warm-cache comparability without metadata.

## Ordering Recommendation

Use paired execution order within each repetition. A future schema task should decide whether source always precedes candidate, candidate always precedes source, or order alternates to reduce bias.

## Timing Artifact Requirements

Each timing artifact should include:

- timing protocol version
- route/method/case/engine identifiers
- source SQL artifact path
- candidate SQL artifact path
- source/candidate execution statuses
- checker exact/result-consistency status
- warmup count
- measured repetitions
- source runtime sample array
- candidate runtime sample array
- source median ms
- candidate median ms
- speedup ratio if eligible
- timeout/failure/N.A. reason
- environment metadata
- claim boundary: local diagnostic, non-official, or official retained evidence after later promotion
