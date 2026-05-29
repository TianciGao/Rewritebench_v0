# Verifier Rerun Readiness

SQLSolver:

- External setup and wrapper are ready.
- PG SQLGlot noop exact-row identity-guard pass produced 24 corrected decidable rows out of 35 exact rows.
- Stronger than VeriEQL on the PG noop exact subset.
- Blocker: `sqlrb user verify --pair-scope run-candidates` is not implemented.

VeriEQL:

- Integrated and locally usable.
- PG SQLGlot noop support closeout found only 4 corrected decidable rows out of 35 exact rows after identity guard.
- Coverage/identity limitations block paper-facing SER promotion.
- Blocker: user-facing exact-candidate verifier rerun facade is not implemented.

Required before final SER work:

- exact/result-consistency gate from a candidate run
- source-vs-source identity guard
- candidate-vs-candidate identity guard
- source-vs-candidate verifier verdict
- corrected denominator over identity-passing decidable rows only
- D035 verifier outputs under `output/results|logs|reports/<run_id>/`

Semantic Equivalence Rate remains N.A. for future Track A reruns unless a
separately authorized verifier rerun produces corrected decidable evidence.
