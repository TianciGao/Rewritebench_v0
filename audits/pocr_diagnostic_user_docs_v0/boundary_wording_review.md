# Boundary Wording Review

The user docs and example README must contain the required POCR diagnostic boundary wording.

Required phrases:

- Positive Operation Coverage diagnostic support
- This is not official POCR.
- Stage A annotation alone is not counted.
- Stage B transformation-aware validation is diagnostic only.
- Semantic guard atoms are not part of operation coverage numerator.
- No route-level POCR score is emitted.
- No paper-facing metric is promoted.

Validation notes:

- `docs/pocr_diagnostic.md` contains all required phrases.
- `examples/pocr_diagnostic/README.md` contains all required phrases.
- The docs describe POCR as diagnostic support only, not official POCR and not paper-facing.
- The docs do not describe tag slices, Stage A rationale, speedup, runtime, taxonomy tags, source SQL shape, candidate SQL shape, or positive SQL alone as operation coverage evidence.
