# Recommendation

Recommended next order:

1. If a local VeriEQL command path becomes available, run one bounded VeriEQL canary.
2. If a local SQLSolver command path becomes available, run the two-pair SQLSolver synthetic smoke.
3. If neither tool is available, optionally implement a user-facing `sqlrb user verify` facade that remains fail-closed and local-only.

Do not proceed directly to broader Common-core verifier runs. The real-tool canaries should first confirm:

- command/version detection,
- raw artifact retention,
- normalized verdict mapping,
- summary generation,
- local-only boundary flags,
- no top-level reports/results writes.

Semantic Equivalence Rate should remain `N.A.` in local metrics until real verifier summary artifacts exist.
