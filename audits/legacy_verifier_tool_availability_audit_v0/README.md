# legacy_verifier_tool_availability_audit_v0

## Verdict

Audit verdict: `completed_no_reusable_local_tool_path_found`.

The release repository already has fail-closed VeriEQL and SQLSolver wrappers plus the `sqlrb user verify` facade, but the legacy/local artifact repository does not currently contain a reusable VeriEQL or SQLSolver command path that can be assigned to `SQLRB_VERIEQL_CMD` or `SQLRB_SQLSOLVER_CMD`.

## Scope

Inspected surfaces:

- Release repo: `/home/tianci_gao/code/Rewritebench_v0`
- Legacy artifact repo: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- Windows-visible WSL equivalent: `\\wsl.localhost\Ubuntu\home\tianci_gao\code\sql-rewrite-bench-artifact-clean`
- GitHub reference branch: `https://github.com/TianciGao/sql-rewrite-bench/tree/artifact/case-package-contract-alignment-clean`

The legacy checkout is on `artifact/case-package-contract-alignment-clean` at commit `428e74514b87956edd3289d40a6ebf15113f119c`, matching the remote branch reported by `git ls-remote`.

## Findings

- VeriEQL: historical notes and provenance artifacts exist, but no usable local staged VeriEQL tree or command path exists in the inspected legacy checkout.
- SQLSolver: historical acquisition/build/smoke notes exist, but no reusable local SQLSolver source checkout, jar, wrapper, or command path exists in the inspected legacy checkout.
- No `.jar` files were found in the legacy checkout.
- No `verieql`, `VeriEQL`, `sqlsolver`, or `SQLSolver` command was found on the release repo PATH.
- No relevant `VERIEQL`, `SQLSOLVER`, `JAVA_HOME`, `LD_LIBRARY_PATH`, or `Z3` environment variable was visible.
- Existing report/provenance artifacts are historical support evidence only. They are not executable tool installations and are not authorized as new-repo official Semantic Equivalence Rate inputs.

## Reuse Status

Recommended mode:

- `SQLRB_VERIEQL_CMD`: unavailable for now.
- `SQLRB_SQLSOLVER_CMD`: unavailable for now.
- Reuse should prefer external local command paths if tools are reinstalled later.
- Do not copy third-party tool source, jars, or historical outputs into the release repo.

## Boundary

This audit did not install tools, copy tools, vendor third-party repositories, run real verifier experiments, compute Semantic Equivalence Rate, compute official metrics, update top-level `reports/` or `results/`, promote retained evidence, or create leaderboard output.
