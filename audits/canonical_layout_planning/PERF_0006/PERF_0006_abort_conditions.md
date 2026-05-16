# PERF_0006 Future Actual Migration Abort Conditions

The future actual migration must stop if any condition below occurs:

- Release repo is dirty before migration starts.
- Legacy case directory `cases/PERF/PERF_0006` is missing.
- Any required legacy file is missing without an approved defer/reference-only mapping.
- Public hygiene scan finds an unexpected local path, temporary path, host trace, prompt/API/token trace, or sensitive log/debug trace in a file planned for public copy.
- A raw Spark plan text file with `file:/tmp` or `/tmp/` traces would be copied into public retained evidence.
- SHA256 copy validation fails for a copied legacy file.
- `manifest.yaml` and `evidence/runs_retention.yaml` contradict each other.
- Validator v0.3 `full-case` mode fails after migration.
- Validator v0.3 `canonical-case` mode fails after migration.
- Denominator, paper results, Common-core membership, or case admission would change.
- A new speedup, timing, performance ranking, or global leaderboard claim would be introduced.
- Raw legacy evidence would be mutated.
- `git add .` or another broad commit scope is attempted.
