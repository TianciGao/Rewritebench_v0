# POCR Transformation-Aware Stage B Calibration v0

This packet compares human positive-control SQL against existing no-op/source-like candidates for four POCR fixture cases using transformation-aware Stage B operation evidence.

- Fixture cases: PERF_0006, CONS_0005, PORT_0003, LONGTAIL_0011
- Candidate classes evaluated: positive_control, noop_control
- Live calls attempted: 8
- Provider/model: `openai_compatible` / `gpt-5.4`
- Schema-valid annotations: 6
- Malformed/schema-invalid annotations: 2
- positive_control transformation_supported operation atoms: 7
- noop_control transformation_supported operation atoms: 0
- positive_control presence_only operation atoms: 1
- noop_control presence_only operation atoms: 2
- positive_control rejected_noop_equivalent operation atoms: 0
- noop_control rejected_noop_equivalent operation atoms: 0
- Calibration risks: {'low': 6, 'positive_control_no_transformation_support': 2}

This is calibration only. It does not compute official POCR, aggregate route-level POCR, run DB/checker/timing, rerun baselines, or promote paper-facing metrics.
