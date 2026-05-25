# POCR Positive vs No-op Calibration v0

This packet compares human positive-control SQL against existing no-op/source-like candidates for four POCR fixture cases.

- Fixture cases: PERF_0006, CONS_0005, PORT_0003, LONGTAIL_0011
- Candidate classes evaluated: positive_control, noop_control
- Live calls attempted: 8
- Provider/model: `openai_compatible` / `gpt-5.4`
- Schema-valid annotations: 6
- Malformed/schema-invalid annotations: 2
- positive_control static validated operation atoms: 8
- noop_control static validated operation atoms: 8
- Calibration risks: {'low': 2, 'positive_control_no_validated_atoms': 2, 'presence_not_rewrite_risk': 4}

This is calibration only. It does not compute official POCR, aggregate route-level POCR, run DB/checker/timing, rerun baselines, or promote paper-facing metrics.
