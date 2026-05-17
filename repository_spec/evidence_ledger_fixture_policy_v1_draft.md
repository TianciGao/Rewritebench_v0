# Evidence Ledger Fixture Policy v1 Draft

Status: draft fixture policy, not implementation-authorizing

Purpose: define how artificial ledger fixture rows should be used to test schema and validation rules before production retained-evidence adapters exist.

## Fixture Boundary

Fixture rows are artificial. They are not retained evidence, benchmark results, paper evidence, or user-run evidence.

Every fixture row must state:

- `fixture_only=true`
- `evidence_source=synthetic_fixture`
- `not_paper_evidence=true`

## Non-use As Paper Evidence

Fixture rows must not be copied into `reports/`, `results/`, paper tables, retained evidence directories, or case packages as evidence.

They must not be used to claim:

- correctness;
- semantic equivalence;
- execution coverage;
- speedup;
- attribution coverage;
- cross-engine execution or consistency;
- Speedup Retention.

## Purpose Of Fixtures

Fixture rows exist only to exercise:

- required fields;
- nullable fields;
- allowed status values;
- record-type-specific field rules;
- denominator usage;
- unsupported and N.A. handling;
- no-global-leaderboard boundaries;
- no-metric-computation boundaries.

## Valid And Invalid Fixtures

Fixture sets should include both expected-valid and intentionally invalid rows.

Invalid rows are required to test that future validators catch:

- missing candidate identity;
- forbidden timing fields on controls;
- forbidden timing fields on verifier support pairs;
- missing target engine on portability rows;
- metric-eligible retained summaries;
- missing denominator IDs where required.

## Future Validator Use

Future validators should load fixture rows before production data. A validator is not implementation-ready until it can:

- accept expected-valid fixture rows;
- reject expected-invalid fixture rows;
- explain validation failures using stable error names;
- avoid computing metrics from fixture rows.

## Output Boundary

Fixture outputs may live only under audit or test fixture directories until a future test/CI task promotes them. This policy does not authorize creating scripts, source package code, production ledgers, reports, results, or paper tables.
