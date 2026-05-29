# Blocker Backlog

## SQLGlot Noop

- PORT source-role / dialect frontiers remain fail-visible.
- MySQL has label-only policy caveats from prior diagnostics.
- Spark has PORT unsupported/fail-closed roles and PORT real-adapter frontier.
- Current MySQL/Spark D035 route cards are not refreshed.

## SQLGlot Optimize

- Context-free optimize can emit invalid correlated-subquery qualification, seen on `CONS_0005`.
- No current D035 route-card refresh.
- Schema-aware route would change semantics and needs a separate route name and authorization.

## Calcite HEP

- MySQL/Spark external runtime behavior not validated.
- No-candidate rows remain.
- DATETIME/TIMESTAMP handling remains unresolved.
- PORT source-role handling remains unresolved.
- Schema-fallback candidates are excluded by policy.
- Mismatches remain in PostgreSQL route card.

## Direct LLM Original

- No D035 adapter under `baselines/`.
- No prompt/model/provider/extraction metadata contract.
- No output reproducibility policy for new user-facing rerun.

## Direct LLM Repair-1

- Depends on Direct LLM original.
- Needs repair-stage metadata.
- Needs execution-feedback and extraction boundary.

## SQLSolver

- Needs `sqlrb user verify --pair-scope run-candidates`.
- Needs D035 exact-candidate verifier output ledger.

## VeriEQL

- Coverage/identity limitations remain.
- Needs user-facing exact-candidate verifier output if used at all.
- Paper-facing VeriEQL SER should remain blocked.
