# Paper Naming Alignment

Use "Positive Operation Coverage Rate (POCR)" as the preferred metric name.

The numerator and denominator are based on `operation_atom` entries, not arbitrary positive-target coverage. The POCR name therefore matches the case-local `skills.md` atom contract and the Stage B operation-evidence boundary.

Older or adjacent drafts may use "Positive Target Coverage Rate (PTCR)" for a similar concept. If the paper keeps PTCR wording, it must explicitly define PTCR as equivalent to POCR or rename consistently throughout the interpretability layer.

Recommended paper wording:

```text
Positive Operation Coverage Rate (POCR) measures the macro-averaged coverage of expected rewrite operation atoms with Stage-B-supported transformation evidence.
```

Stage A annotation alone is not counted. Stage B transformation-aware validation is required.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
