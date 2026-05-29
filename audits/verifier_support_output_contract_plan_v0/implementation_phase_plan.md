# Implementation Phase Plan

Phase V0: output contract only.

- This task.
- No implementation and no verifier run.

Phase V1: synthetic verifier fixture and verdict normalization tests.

- Create fixture pairs and synthetic verdicts.
- Validate schemas and summary computation.
- No external tool dependency.

Phase V2: bounded VeriEQL canary integration.

- Add controlled canary invocation.
- Fail closed for unavailable tool, unsupported SQL, or missing context.
- Keep outputs local-only.

Phase V3: bounded SQLSolver smoke integration.

- Add controlled support-pair invocation.
- Normalize verdicts to shared schema.
- Keep outputs local-only.

Phase V4: local metrics reads `semantic_equivalence_summary.json`.

- Populate Semantic Equivalence Rate only when formal verifier evidence exists.
- Preserve `N.A.` when verifier evidence is absent.

Phase V5: optional official promotion.

- Separate authorization required.
- Validate provenance, denominator identity, route identity, verifier versions, environment, and artifact paths before any official use.
