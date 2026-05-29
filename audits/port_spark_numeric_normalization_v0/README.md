# PORT Spark Numeric Normalization Audit

Verdict: `completed`

This packet records the narrow local-diagnostic checker fix for the MySQL-source to Spark-target numeric representation gap exposed by the PORT Spark controlled diagnostic for `PORT_0004` and `PORT_0013`.

Root cause confirmed: yes. The prior diagnostic artifacts showed both sides executed successfully and produced one row/one column. MySQL source-reference JSONL serialized the numeric aggregate as a string, while Spark target-candidate JSONL serialized the decimal-equivalent value as a JSON number. The checker already allowed cross-dialect positional comparison and string-vs-string decimal equivalence, but did not allow string-vs-number decimal equivalence.

Change summary:
- Added safe mixed string/number numeric equivalence in `local_result_checker.py`.
- Enabled that equivalence only when resolved manifest metadata declares `source_reference.engine == mysql` and `target_candidate.engine == spark`.
- Excluded booleans, nulls, nonnumeric strings, dates, identifiers, NaN, and infinities from numeric coercion.
- Kept same-engine PERF/CONS/LONGTAIL and same-engine PORT comparisons strict.
- Kept PostgreSQL/MySQL cross-dialect routes unchanged except for continuing their existing passing behavior.

Before/after:
- Before controlled Spark target run: selected/source/candidate/checker/exact/mismatch rows `4/4/4/4/2/2`.
- After controlled Spark target run: selected/source/candidate/checker/exact/mismatch rows `4/4/4/4/4/0`.
- Fixed cases: `PORT_0004` and `PORT_0013`.

Boundary:
- Local diagnostic checker fix only.
- No SQL changes.
- No manifest changes.
- No schema/checker YAML/validation/case set changes.
- No reports/results updates.
- No denominator, paper result, case membership, or raw retained evidence changes.
- No official metrics, timing/speedup, or leaderboard output.

Next safe action: rerun a broader Common-core Spark local diagnostic only if desired, treating PORT controlled rows and unsupported rows as local diagnostic evidence only; keep official metrics, timing, reports/results, retained-evidence promotion, and leaderboard work out of scope.
