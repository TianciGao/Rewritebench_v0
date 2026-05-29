# Real-Tool Readiness Gates

## VeriEQL

Before a real VeriEQL canary:

- Provide an explicit command path or one of the supported environment variables.
- Detect and record tool version.
- Use one bounded pair only at first, preferably a `CONS_0005` source/positive pair or a synthetic support pair.
- Write raw stdout and stderr under `output/results/<run_id>/verifier/tools/verieql/`.
- Confirm normalized verdict and summary fields.
- Keep the run local-only and non-official.

## SQLSolver

Before a real SQLSolver smoke:

- Provide an explicit command path or `SQLRB_SQLSOLVER_CMD`.
- Detect and record tool version.
- Use the two-pair synthetic smoke first:
  - `SELECT 1` vs `SELECT 1`
  - `SELECT 1` vs `SELECT 2`
- If the tool requires schema/context, use a minimal temporary schema fixture.
- Write raw stdout and stderr under `output/results/<run_id>/verifier/tools/sqlsolver/`.
- Confirm normalized verdict and summary fields.
- Keep the run local-only and non-official.

## Shared Gates

- Do not merge VeriEQL and SQLSolver into an official score.
- Do not use verifier outputs as rewrite baselines.
- Do not rank verifier tools against rewrite routes.
- Do not update top-level `reports/` or `results/`.
- Do not promote retained evidence without a separate task.
