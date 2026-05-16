# CONS_0005 Future Migration Abort Conditions

The actual future `CONS_0005` canonical-layout migration must stop if any condition below is true.

- Release repo is dirty before migration begins.
- Legacy `cases/CONS/CONS_0005` is missing or has unexpected required-file gaps.
- Any mutating command is attempted in the legacy repository.
- Public hygiene scan fails on a file intended for public release.
- Raw `file:/tmp`, `/tmp/`, `/home/tianci_gao`, WSL, prompt, API key, token, or similar traces remain in public-facing files.
- Copied file SHA256 does not match the corresponding legacy source unless the file is explicitly generated or sanitized.
- Manifest and `evidence/runs_retention.yaml` contradict each other.
- Checker expected-rejection reason is unknown and has not been approved.
- Spark plan sanitization cannot preserve plan evidence while removing local paths.
- Validator v0.3 `full-case` mode fails.
- Validator v0.3 `canonical-case` mode fails.
- Any denominator, paper-result, or case-membership field changes.
- Raw legacy evidence is modified, deleted, renamed, moved, or sanitized in place.
- Raw `runs/` is copied wholesale into the public case.
- `git add .` or any broad commit scope is attempted.
- The task begins to look like Common-core 40 migration rather than a single-case pilot.
