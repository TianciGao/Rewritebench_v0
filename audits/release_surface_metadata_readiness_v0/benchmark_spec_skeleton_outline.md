# Benchmark Spec Skeleton Outline

Future `benchmark_spec/` files should preserve the locked public v0 facts and avoid introducing new scientific claims.

## `benchmark_spec/README.md`

- Explain that this directory governs public benchmark scope.
- Link scope, case package contract, denominator policy, and reporting policy.
- State that it does not compute metrics or render paper tables.

## `benchmark_spec/scope.md`

Must state:

- Common-core v0 = 40 cases.
- Pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Track A same-engine denominator = 120 planned rows.
- Case package is the benchmark unit.
- Common-core v0 is a controlled coverage set, not a production frequency sample.

## `benchmark_spec/case_package_contract.md`

Must describe:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql` when declared
- `schema/schema_profile.yaml`
- `checker/`
- `validation/`
- external schema linkage through manifest/schema profile metadata

## `benchmark_spec/denominator_policy.md`

Must state:

- Membership and denominator rows are governed by `case_sets/common_core_v0/`.
- Track A same-engine planned rows remain 120.
- Denominator changes require separate authorization.
- User-entry local outputs do not change denominator membership.

## `benchmark_spec/reporting_policy.md`

Must state:

- Results must be role-aware and denominator-aware.
- No global leaderboard.
- Hard negatives are checker controls, not method-generated candidates.
- Performance is interpreted only on exact + timed rows.
- PORT bounded evidence must not be described as full PORT9 closure.
- SpeedupTransferRate is not computed for current evidence.
- Verifier support is not a rewrite-generation baseline.
- Official metrics and paper table rendering require separate authorization.
