# Timing Readiness

Exact-gated timing is ready as a separate local diagnostic task over the 66 exact/result-consistent rows from this packet.

Timing must remain exact-gated:

- do not time the 25 mismatch rows;
- do not time the 9 candidate execution failure rows;
- do not time the 20 fail-closed/no executable candidate rows;
- do not time rows with unsupported engine/source-role outcomes.

No timing was collected in this task. The next timing task should use the existing local timing defaults unless separately changed:

- warmup: 1
- measured repetitions: 5
- timeout: 30 seconds
- statistic: median

Any timing output remains local diagnostic only and must not be promoted to official paper metrics without separate authorization.
