# Open Gaps Before Final Rerun

Implementation gaps:

- `sqlrb user verify --pair-scope run-candidates` is not implemented.
- `sqlrb user evaluate --verifier` still fails closed.
- No user-facing verifier command currently imports exact candidate rows from a previous candidate run.
- No user-facing verifier command currently emits a canonical per-candidate identity ledger.
- No CLI flag set exists for SQLSolver identity reruns beyond synthetic smoke.
- No CLI flag set exists for VeriEQL finite-bound exact-candidate reruns through the user-facing facade.

Policy gaps:

- Paper-facing SQLSolver support row needs separate authorization.
- Paper-facing VeriEQL SER remains blocked due coverage/identity limitations.
- Coverage and identity pass rates must be reported alongside any future local or paper-facing rate.
- Non-equivalent rows require investigation before promotion.

The next implementation task should be narrow: add a local-only exact-candidate verifier rerun facade that reads a candidate run, applies the exact/result-consistency gate, runs identity guard, and writes only D035 verifier outputs.
