# Next Canary Plan Recommendation

## Recommended Next Safe Action

Authorize a narrow VeriEQL adapter compatibility task before running any real VeriEQL canary.

The compatibility task should:

- add `SQLRB_VERIEQL_ROOT` support
- generate VeriEQL JSONL pair input
- invoke `python -m parallel.cli_within_timeout` from the VeriEQL root
- retain raw stdout/stderr and output JSONL under D035 local verifier paths
- parse VeriEQL output into the shared verifier-support verdict vocabulary
- keep missing dependencies and tool failures fail-closed
- avoid official metrics, retained evidence, reports/results, and leaderboard output

## First Candidate

Use `CONS_0007` first for adapter wiring and fail-closed behavior. It is the old readiness scaffold's only `support_candidate`, but historical VeriEQL output shows `EXISTS` may be unsupported, so the expected outcome should be compatibility information, not proof.

## Secondary Candidate

Use `CONS_0035` only after `CONS_0007` wiring is clean. It has richer historical VeriEQL and SQLSolver clues, but the positive pair is constraint-sensitive.

## SQLSolver Follow-up

If a SQLSolver command or jar path is provided, run a bounded synthetic smoke first, then optionally `CONS_0007` positive/negative pairs. Do not copy or vendor the tool into the release repo.

## Stop Conditions

Stop and report if:

- the tool command is unavailable
- dependencies are missing
- the tool requires installation or vendoring
- output cannot be placed under `output/results|logs|reports/<run_id>/`
- verifier output cannot be normalized without guesswork
