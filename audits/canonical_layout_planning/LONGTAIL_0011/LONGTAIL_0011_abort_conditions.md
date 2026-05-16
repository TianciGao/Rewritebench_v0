# LONGTAIL_0011 Actual Migration Abort Conditions

The future actual canonical-layout migration for `LONGTAIL_0011` must stop if any condition below is true.

- The release repo is dirty at preflight and the dirtiness is not part of the approved task.
- The legacy case directory `cases/LONGTAIL/LONGTAIL_0011/` is missing.
- Required legacy SQL, schema, witness, validation, or retained evidence files are missing.
- Any public hygiene scan fails after proposed sanitization/adaptation.
- Any unexpected local path appears in a public file, including `file:/home`, `file:/mnt`, `file:/tmp`, `/tmp/`, `C:\`, WSL-local wording, or maintainer-local absolute paths.
- Any API key, prompt, assistant, or token trace appears in a public file.
- A copied file hash does not match the legacy source for a copy-as-is or copy-and-rename artifact.
- A sanitized Spark plan does not remove local temporary paths.
- `manifest.yaml` and `evidence/runs_retention.yaml` contradict each other.
- The hard-negative expected rejection reason is missing, unclear, or not approved for public checker packaging.
- Validator v0.3 `full-case` mode fails.
- Validator v0.3 `canonical-case` mode fails.
- The migration would change denominator, paper results, Common-core membership, or case admission status.
- The migration would create a workload-frequency, production-frequency, global-leaderboard, or paper-result claim.
- The migration would modify raw legacy evidence.
- Raw `runs/` would be copied wholesale without public-safety review and retention mapping.
- `git add .` or another broad commit scope is attempted.
- Any command would run DB engines, validation scripts, timing workloads, LLM calls, or evidence regeneration.
