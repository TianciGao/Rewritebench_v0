# LONGTAIL_0011 Positive SQL Correction

Task: `fix_longtail_0011_positive_sql_contract_v0`

This audit records a narrow case-local correction to:

- `cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql`

The previous positive SQL used an ascending `WorstRank` shortcut. The corrected positive SQL now matches the source query surface expected by `skills.md`: descending `DENSE_RANK()` as `PostRank`, a grouped `MaxRank` relation, and `rp.PostRank = mr.MaxPostRank`.

No source SQL, negative SQL, skills contract, manifest, checker configuration, case membership, denominator, paper-facing result, baseline output, POCR annotation, user output, or retained evidence was updated.

Validation status: static contract checks passed; DB/checker validation was deferred because this task did not authorize broad DB/checker/timing execution.
