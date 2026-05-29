# Recommendation

Current D035 compliance verdict:

- User-facing CLI location: compliant.
- Internal implementation location: compliant.
- Baseline adapter location: compliant.
- User-facing output exporter: compliant.
- Examples surface: present, but could use a D035 runnable sample refresh.
- Docs surface: partial; needs a separate docs organization and wording cleanup.
- Dev scripts: intentionally deferred.
- Benchmark data physical layout: intentionally deferred.

Recommended follow-up:

Authorize a narrow audit/docs cleanup task, not a physical migration task.

Suggested scope for the follow-up:

1. Update user docs and baseline READMEs to distinguish internal `runs/user/<run_id>/` staging from exported D035 user output.
2. Add `docs/guide/`, `docs/spec/`, and `docs/templates/` skeletons or move only documentation when references are safe.
3. Add a minimal D035 user-output example under `examples/` if useful.
4. Leave `cases/`, `case_sets/`, `schemas/`, `inventory/`, and `scripts/dev/` in place.

No source move is recommended from this inventory.
