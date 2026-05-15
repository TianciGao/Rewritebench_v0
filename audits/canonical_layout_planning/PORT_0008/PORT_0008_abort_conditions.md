# PORT_0008 Future Actual Migration Abort Conditions

Stop the future actual migration if any of these occur:

- Release repo is dirty before starting.
- Release repo is behind `origin/main` and cannot be fast-forwarded cleanly.
- Legacy repo state cannot be inspected read-only.
- Any expected legacy `PORT_0008` file is missing.
- Existing release evidence-pilot files are missing or SHA256 does not match the formal mapping.
- Public hygiene scan finds raw local paths, host traces, prompt/API/token traces, or raw log paths in any public candidate file.
- Raw Spark plan files would be copied into public retained evidence.
- Copied file SHA256 does not match the corresponding legacy source, except for explicitly generated metadata or explicitly reused sanitized evidence.
- `manifest.yaml`, `evidence/runs_retention.yaml`, and `metadata/artifact_paths.yaml` disagree about a path or evidence role.
- Validator v0.2 full-case mode fails after the future migration.
- Any file claims denominator changed, paper results changed, Common-core membership changed, global leaderboard status, or case admission beyond the approved state.
- Any command would mutate the legacy repo.
- Any DB engine, validation script, timing workload, or LLM call would run.
- Raw legacy evidence would be deleted, moved, renamed, overwritten, or sanitized in place.
- `git add .` or another broad staging command is attempted.
- Commit scope includes files outside the explicit approved actual-migration path list.
