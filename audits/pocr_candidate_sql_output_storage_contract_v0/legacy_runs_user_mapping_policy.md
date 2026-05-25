# Legacy runs/user Mapping Policy

Existing `runs/user/**/candidate_sql` roots are legacy local/user-run assets.

They may be read as source maps for diagnostics and reconciliation. They must not be deleted, moved, overwritten, normalized, or copied without inventory and retention mapping.

These roots are not official retained evidence by default. They are not leaderboard inputs. They do not fill paper-facing POCR cells by themselves.

Future manifests should reference legacy roots with:

- `source_run_id`
- `source_candidate_root`
- `legacy_source_root`
- candidate SHA-256
- file size
- route and denominator metadata

The preferred migration policy is reference-first. If a future task needs to copy legacy candidates into D035-shaped `output/results/<run_id>/candidate_sql/`, that task must be separately authorized, must preserve hashes, and must record why copy is necessary.

No file deletion, copy, move, normalization, or rewrite occurred in this task. No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.
