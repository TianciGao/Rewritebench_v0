# POCR Full-40 Positive-vs-Noop Control Calibration v0

This packet compares human positive-control SQL against existing no-op/source-like candidates for all 40 Common-core v0 cases using transformation-aware Stage B operation evidence.

- Common-core cases evaluated: 40
- Candidate classes evaluated: positive_control, noop_control
- Live calls attempted: 80
- Provider/model: `openai_compatible` / `gpt-5.4`
- Schema-valid annotations: 72
- Malformed/schema-invalid annotations: 8
- positive_control transformation_supported operation atoms: 80
- noop_control transformation_supported operation atoms: 0
- positive_control presence_only operation atoms: 10
- noop_control presence_only operation atoms: 12
- positive_control rejected_noop_equivalent operation atoms: 0
- noop_control rejected_noop_equivalent operation atoms: 0
- Calibration risk rows: {'atom_or_positive_alignment_gap': 8, 'low': 72}
- Calibration risk cases: {'atom_or_positive_alignment_gap': 4, 'low': 36}

Outcome: the no-op control received zero transformation-supported operation atoms across all 40 cases. Positive control received transformation support on 36/40 cases, with four case-level atom/positive-alignment gaps retained for review.

This is calibration only. It does not compute official POCR, aggregate route-level POCR, run DB/checker/timing, rerun baselines, or promote paper-facing metrics.

Next safe action: if this diagnostic boundary is accepted, authorize one real-route diagnostic pass; otherwise keep POCR deferred/N.A. and document case-level atom/positive alignment gaps.
