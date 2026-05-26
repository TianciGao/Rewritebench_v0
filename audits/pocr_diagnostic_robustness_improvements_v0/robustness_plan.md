# Robustness Plan

The robustness work is intentionally offline and diagnostic-only.

1. Add retry planning as a separate review artifact, not as automatic retry execution.
2. Classify provider JSON output failures more precisely without silently accepting ambiguous outputs.
3. Lint Stage A evidence refs before Stage B interpretation and report quality feedback without changing diagnostics.
4. Build a manual-review queue for transformation-supported atoms, possible under-accept rows, fail-closed retry candidates, and linter warnings/errors.
5. Preserve D036/D037/D038 boundaries: skills.md is the atom source, Stage B is transformation-aware, and annotation JSONL remains diagnostic evidence only.
