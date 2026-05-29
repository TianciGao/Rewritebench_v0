# Config Change Summary

Changed file:

- `cases/CONS/CONS_0011/checker/normalization.yaml`

Change made:

```yaml
sort_rows: true
```

The setting was added at top level so the current local checker applies repository-supported row sorting during result normalization for `CONS_0011`.

Preserved settings:

- `normalization_version: canonical_case_package_layout_v2`
- `case_id: CONS_0011`
- `pool: CONS`
- `sql_paths`
- `rules.ignore_whitespace: true`
- `rules.ignore_case_for_keywords: true`
- `rules.normalize_numeric_literals: false`
- `rules.preserve_semantic_operators: true`
- `evidence_policy`

Files intentionally not changed:

- SQL files: no.
- Manifest files: no.
- `compare_config.yaml`: no, because current checker does not consume row-order policy from that file.
- `checker.yaml`: no.
- Global checker/source code: no.
- Other case checker configs: no.
- `case_sets/`: no.
- `reports/` or `results/`: no.

Boundary:

- Official metrics computed: no.
- Timing or speedup computed: no.
- Global leaderboard created: no.
- Denominator, paper result, case membership, and raw retained evidence changed: no.
