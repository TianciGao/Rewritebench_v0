# Computability Gaps

Existing local replay artifacts are sufficient for a dry-run macro calculation for the two included routes because they contain one row per PG40 case with:

- planned row identity;
- candidate presence;
- annotation status;
- expected operation atom count;
- Stage-B transformation-supported operation atom count;
- presence-only, insufficient-evidence, rejected-noop, and schema-invalid atom counts;
- diagnostic boundary flags.

Committed audit packets alone are not equally sufficient for both routes. SQLGlot no-op has a committed row-level sanity-control CSV that can cross-check row counts, but Repair-1's committed closeout and targeted-retry audit packet primarily contain aggregate summaries plus mapping rows. The local `/tmp` replay artifact is the decisive per-row Repair-1 macro source.

No expected atom count gap was found for PG40. Read-only `skills.md` operation-atom counts total 107 and match the replay artifacts.

No Stage B row-count gap was found in the local replay artifacts.

A future reusable aggregator should require exported row-level diagnostic artifacts in a stable committed or retained diagnostic location if the values need to be reproducible without local `/tmp` state.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
