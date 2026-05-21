# Protected Surface Check

## Intended Changed Files

- 9 PORT manifests:
  - `cases/PORT/PORT_0003/manifest.yaml`
  - `cases/PORT/PORT_0004/manifest.yaml`
  - `cases/PORT/PORT_0005/manifest.yaml`
  - `cases/PORT/PORT_0008/manifest.yaml`
  - `cases/PORT/PORT_0012/manifest.yaml`
  - `cases/PORT/PORT_0013/manifest.yaml`
  - `cases/PORT/PORT_0022/manifest.yaml`
  - `cases/PORT/PORT_0024/manifest.yaml`
  - `cases/PORT/PORT_0025/manifest.yaml`
- `audits/port_cross_dialect_manifest_metadata_patch_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

No intended changes to:

- source code under `src/`
- scripts
- tests
- docs
- examples
- SQL files
- schema files
- checker files
- validation files
- `case_sets/`
- inventory
- reports/results
- benchmark_spec
- repository_spec
- raw retained evidence
- `.github/workflows/`
- root metadata files
- release tags or branches

## Validation Result

- `git diff --check`: passed.
- YAML parse checks for all 9 patched manifests: passed.
- Static local-diagnostic semantic checks for all 9 patched manifests: passed.
- Static v2 case-package validator: 31/40 Common-core cases passed; the 9 patched PORT cases failed only because the current validator does not yet whitelist the new top-level `local_diagnostic` metadata (`local_diagnostic: unapproved top-level key`). Updating validator source is deferred to P3 because P2 does not authorize source/test changes.
- Legacy canonical-case validator: non-applicable to the current clean v2 layout; it still expects v1-era paths such as `sql/positives/`, case-local engine schema directories, and evidence files that are intentionally absent from clean v2 packages.
- Changed-file checks: exactly 9 PORT manifests changed; no SQL files changed; no non-PORT manifests changed; `case_sets/` unchanged; reports/results unchanged; denominator scaffolds unchanged.
- CSV and Markdown checks for audit files: passed.
- Protected-surface status check: passed.
- `runs/user/` output check: no run output was created for this metadata-only task.
