# Regression Tests

## Focused Checker Tests

Command:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py -q
```

Result:

```text
26 passed in 0.09s
```

Coverage added or confirmed:

- strict exact records `value_exact=true`, `label_exact=true`, `label_only_mismatch=false`
- strict label mismatch remains mismatch and records `label_only_mismatch=true`
- value mismatch is not label-only
- row count mismatch is not label-only
- column count mismatch is not label-only
- duplicate/multiplicity mismatch is not label-only
- explicit alias mismatch remains strict
- generated-expression label mismatch is diagnostic-only, not exact
- controlled cross-dialect paths remain unchanged
- MySQL-source to Spark-target numeric normalization role gate remains unchanged
- representative PERF/CONS/LONGTAIL/same-engine PORT strict behavior remains unchanged

## Focused Quality Report Tests

Command:

```bash
PYTHONPATH=src pytest tests/user_entry/test_quality_report.py -q
```

Result:

```text
4 passed in 0.12s
```

Coverage added or confirmed:

- quality summary includes `diagnostic_counts.label_only_mismatch_rows`
- quality report includes a diagnostic classifications section
- local diagnostic boundary remains unchanged
- timing/speedup fields are still absent

## Full User-Entry Tests

Command:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result:

```text
146 passed, 1 skipped, 12 subtests passed in 3.67s
```
