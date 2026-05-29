# Preservation Risk Review

Existing `runs/user/` candidate SQL roots are local/user-run assets. They are not official retained evidence by default.

They are nevertheless valuable for POCR diagnostic replay because they preserve route-labeled candidate SQL that can be paired with `skills.md` and annotation JSONL later.

Preservation policy recorded by this task:

- Do not delete existing `runs/user/**/candidate_sql` roots until they are mapped.
- Do not move candidate SQL without a separate retention/export decision.
- Do not overwrite candidate SQL without an explicit rerun or output-contract authorization.
- Do not copy candidate SQL into retained evidence or paper-facing results without separate promotion authorization.

This task did not move, copy, delete, normalize, regenerate, or rewrite any candidate SQL file.

The SHA-256 manifest records current file identity for later preservation review:

- `candidate_sha256_manifest.csv`

Risk notes:

- Many candidate roots are unit-test or smoke artifacts. They should not be treated as route evidence without human review.
- Some canonical route roots are incomplete as candidate SQL file roots because fail-closed/no-candidate rows have no candidate SQL file.
- Complete candidate SQL roots are useful for replay, but annotation JSONL remains route-bound and must match `case_id`, `engine`, `method_id`, `route_id`, and candidate identity.
- Official POCR, route-level aggregation, retained-evidence promotion, paper metric promotion, and leaderboard output remain separately gated.
