# MySQL Same-Engine Source Failure Triage v0

Verdict: `legacy_mapping_gap`.

This audit triages the four `source_execution_failed` rows from the Common-core MySQL local diagnostic trial: `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`. A targeted rerun selected exactly those four rows and reproduced `mysql_source_execution_failed` for all four before candidate execution or checker handoff.

The failures are not schema setup, load, candidate execution, checker, output conversion, or permission failures. Each case has current MySQL schema/load assets and the run reached source query execution. The failing query is the current `sql/source.sql`, which is PostgreSQL-like in all four cases and is rejected by MySQL syntax.

Legacy reference use was read-only. The legacy branch `artifact/case-package-contract-alignment-clean` contains retained MySQL artifacts for `runs/mysql/rewrite_pos_01.tsv`, plus PostgreSQL `runs/pg/source.tsv`; it does not show a retained `runs/mysql/source.tsv` artifact for these cases. Legacy validation therefore appears to have compared a PostgreSQL source reference against a MySQL positive target rewrite, not direct MySQL execution of `source.sql`.

## Case Summary

| Case | New failure | Root cause classification | Legacy evidence |
|---|---|---|---|
| `PORT_0003` | MySQL rejects PostgreSQL-style `source.sql` with double quotes and `NULLS LAST`. | `legacy_mapping_gap` | MySQL `rewrite_pos_01.tsv`, no MySQL source artifact found. |
| `PORT_0005` | MySQL rejects PostgreSQL-style `source.sql` with double quotes and `NULLS FIRST`. | `legacy_mapping_gap` | MySQL `rewrite_pos_01.tsv`, no MySQL source artifact found. |
| `PORT_0008` | MySQL rejects PostgreSQL-style quoted identifiers and PostgreSQL expression syntax. | `legacy_mapping_gap` | MySQL `rewrite_pos_01.tsv`, no MySQL source artifact found. |
| `PORT_0012` | MySQL rejects PostgreSQL-style quoted identifiers and `TO_CHAR`/cast syntax. | `legacy_mapping_gap` | MySQL `rewrite_pos_01.tsv`, no MySQL source artifact found. |

## Boundary

This is local diagnostic triage only. It computes no official metrics, no timing/speedup, no reports/results updates, no denominator changes, no paper-result changes, no raw retained-evidence changes, and no leaderboard output. The targeted rerun output remains local under `runs/user/mysql_source_failure_triage/` and is not committed.

## Recommended Next Safe Action

Run a narrow role-mapping design/fix task for the four PostgreSQL-source to MySQL-target PORT cases. The task should decide whether these rows need explicit reverse cross-dialect local-diagnostic metadata and runner routing, or whether `--engine mysql` should continue failing closed for them. Do not edit SQL or schema files as the first step.
