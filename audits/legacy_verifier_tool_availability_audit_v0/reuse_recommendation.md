# Reuse Recommendation

## Recommendation

Recommended reuse mode: `external_local_path_only_when_available`.

Current state:

- VeriEQL: unavailable as a reusable local command.
- SQLSolver: unavailable as a reusable local command.

## Do Not Reuse By Copying

Do not copy into the release repo:

- third-party source checkouts,
- jars or native libraries,
- Docker images,
- virtual environments,
- `/tmp` build outputs,
- legacy verifier output artifacts,
- retained report artifacts.

## Safe Future Paths

Safe future options:

1. Provide a local VeriEQL command path through `sqlrb user verify --tool verieql --tool-cmd <path>` after separately staging the tool.
2. Provide a local SQLSolver command path through `sqlrb user verify --tool sqlsolver --tool-cmd <path>` after separately staging the tool.
3. Add small wrapper scripts only in a separately authorized task if they wrap external installations without vendoring third-party tool code or binaries.
4. Keep historical verifier outputs as historical support evidence until a retained-evidence mapping task authorizes and constrains any reuse.

## License And Vendor Risk

Copying third-party tools into the release repository is not recommended. SQLSolver historical notes mention Apache-2.0 upstream visibility, but that does not authorize vendoring binaries/source in this release task. VeriEQL historical staged-code provenance is not present in the inspected checkout and would require a separate license/source review before any vendoring decision.

## Current Wrapper Action

Keep the current new-repo wrappers fail-closed:

- `SQLRB_VERIEQL_CMD`: not set.
- `SQLRB_SQLSOLVER_CMD`: not set.
- `semantic_equivalence_rate`: remains `null` / `N.A.` without real verifier evidence.
