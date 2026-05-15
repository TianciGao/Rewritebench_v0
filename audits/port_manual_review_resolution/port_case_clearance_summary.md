# PORT manual-review resolution summary

Generated: 2026-05-15T18:32:58

Scope: read-only static inspection of seven Common-core PORT cases. No legacy files were modified.

## PORT_0004

- why it was flagged: Current legacy source tree has no high-risk traces for this case; prior flagged warehouse residue was not present in this checkout.
- inspected: 45 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0004` plus manifest/validation/report/prior-audit references.
- risks found: local_path=no; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: cleared_for_evidence_index_normalization
- physical migration pilot: cleared_for_physical_pilot
- human decision remains: no; Proceed to evidence-index normalization; physical pilot may proceed only copy-first with runs_retention mapping.

### Compact case tree

```text
PORT_0004/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_neg_02_spark.sql
  rewrite_pos_01.sql
  rewrite_pos_02_spark.sql
  runs/mysql/plans/source.json
  runs/mysql/source.tsv
  runs/pg/plans/rewrite_neg_01.json
  runs/pg/plans/rewrite_pos_01.json
  runs/pg/rewrite_neg_01.tsv
  runs/pg/rewrite_pos_01.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_02_spark.txt
  runs/spark/plans/rewrite_pos_02_spark.txt
  runs/spark/rewrite_neg_02_spark.tsv
  runs/spark/rewrite_pos_02_spark.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  source.sql
  taxonomy_trial_v0.3.yaml
  validation/PLAN_COLLECTION_README.md
  validation/README.md
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/checker.yaml
  validation/collect_mysql_plans.sh
  validation/collect_pg_plans.sh
  validation/collect_spark_plans.sh
  validation/load_witness_mysql.sql
  validation/load_witness_pg.sql
  validation/load_witness_spark.sql
  validation/mysql_witness_data.sql
  validation/run_mysql_validation.sh
  validation/run_pg_validation.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| none | retained evidence | mapped evidence | keep_as_legacy_retained_evidence_with_mapping | no high-risk highlight |

## PORT_0008

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 35 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0008` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0008/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_pos_01.sql
  runs/mysql/plans/rewrite_neg_01.json
  runs/mysql/plans/rewrite_pos_01.json
  runs/mysql/rewrite_neg_01.tsv
  runs/mysql/rewrite_pos_01.tsv
  runs/pg/plans/source.json
  runs/pg/source.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0008/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 16 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0008/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0008_spark_plan_collect...;line 31 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0008/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0008_spark_plan_collect... |
| cases/PORT/PORT_0008/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 16 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0008/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0008_spark_plan_collect...;line 31 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0008/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0008_spark_plan_collect... |

## PORT_0012

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 37 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0012` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0012/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_pos_01.sql
  runs/mysql/plans/rewrite_neg_01.json
  runs/mysql/plans/rewrite_pos_01.json
  runs/mysql/rewrite_neg_01.tsv
  runs/mysql/rewrite_pos_01.tsv
  runs/pg/plans/source.json
  runs/pg/source.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0012/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 15 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0012_spark_plan_collect... |
| cases/PORT/PORT_0012/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 15 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0012_spark_plan_collect... |

## PORT_0013

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 39 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0013` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0013/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_neg_02_spark.sql
  rewrite_pos_01.sql
  rewrite_pos_02_spark.sql
  runs/mysql/plans/source.json
  runs/mysql/source.tsv
  runs/pg/plans/rewrite_neg_01.json
  runs/pg/plans/rewrite_pos_01.json
  runs/pg/rewrite_neg_01.tsv
  runs/pg/rewrite_pos_01.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0013/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 19 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0013_spark_plan_collect...;line 38 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0013_spark_plan_collect... |
| cases/PORT/PORT_0013/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 19 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0013_spark_plan_collect...;line 38 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0013_spark_plan_collect... |

## PORT_0022

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 39 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0022` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0022/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_pos_01.sql
  runs/mysql/plans/source.json
  runs/mysql/result_check.json
  runs/mysql/source.tsv
  runs/pg/plans/rewrite_neg_01.json
  runs/pg/plans/rewrite_pos_01.json
  runs/pg/rewrite_neg_01.tsv
  runs/pg/rewrite_pos_01.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/result_check.json
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0022/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 20 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0022_spark_plan_collect...;line 35 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0022_spark_plan_collect... |
| cases/PORT/PORT_0022/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 20 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0022_spark_plan_collect...;line 35 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0022/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0022_spark_plan_collect... |

## PORT_0024

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 39 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0024` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=yes; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0024/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_pos_01.sql
  runs/mysql/plans/source.json
  runs/mysql/result_check.json
  runs/mysql/source.tsv
  runs/pg/plans/rewrite_neg_01.json
  runs/pg/plans/rewrite_pos_01.json
  runs/pg/rewrite_neg_01.tsv
  runs/pg/rewrite_pos_01.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/result_check.json
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0024/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 12 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0024/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0024_spark_plan_collect... |
| cases/PORT/PORT_0024/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 12 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0024/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0024_spark_plan_collect... |
| cases/PORT/PORT_0024/runs/spark/result_check.json | MySQL or Spark log/debug residue | control validation | move_to_external_archive_later | line 20 categories=log_debug snippet="stdout_log": "cases/PORT/PORT_0024/runs/spark/load_and_execute.log",;line 21 categories=log_debug snippet="stderr_log": "cases/PORT/PORT_0024/runs/spark/stderr.log" |

## PORT_0025

- why it was flagged: Local path/host/WSL/localhost traces appear in plan evidence; evidence index can record them, but physical/public migration needs sanitized copies or archive mapping.
- inspected: 39 files under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/cases/PORT/PORT_0025` plus manifest/validation/report/prior-audit references.
- risks found: local_path=yes; prompt_api_token=no; spark_warehouse=no; log_debug=no; evidence_unclear=no.
- evidence-index normalization: evidence_index_ok_but_physical_pilot_blocked
- physical migration pilot: blocked_pending_sanitization
- human decision remains: yes; Approve sanitized public copy plan for affected plan evidence files.

### Compact case tree

```text
PORT_0025/
  manifest.yaml
  provenance/parrot_source_record.json
  provenance/provenance_notes.txt
  rewrite_neg_01.sql
  rewrite_pos_01.sql
  runs/mysql/plans/source.json
  runs/mysql/result_check.json
  runs/mysql/source.tsv
  runs/pg/plans/rewrite_neg_01.json
  runs/pg/plans/rewrite_pos_01.json
  runs/pg/rewrite_neg_01.tsv
  runs/pg/rewrite_pos_01.tsv
  runs/plan_check.json
  runs/result_check.json
  runs/spark/plans/rewrite_neg_01.txt
  runs/spark/plans/rewrite_pos_01.txt
  runs/spark/result_check.json
  runs/spark/rewrite_neg_01.tsv
  runs/spark/rewrite_pos_01.tsv
  schema/ddl_mysql.sql
  schema/ddl_pg.sql
  schema/ddl_spark.sql
  schema_notes.md
  source.sql
  validation/check_plan_artifacts.py
  validation/check_results.py
  validation/mysql_witness_data.sql
  validation/pg_witness_data.sql
  validation/run_mysql_plan_collection.sh
  validation/run_mysql_validation.sh
  validation/run_pg_plan_collection.sh
  validation/run_pg_validation.sh
  validation/run_spark_plan_collection.sh
  validation/run_spark_validation.sh
  validation/spark_witness_data.sql
```

### Reviewed risk/decision highlights

| file/group | classification | evidence role | recommendation | notes |
|---|---|---|---|---|
| cases/PORT/PORT_0025/runs/spark/plans/rewrite_neg_01.txt | sanitizable evidence | hard-negative rejection evidence; plan/failure observability | keep_with_public_sanitized_copy_later | line 18 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0025_spark_plan_collect...;line 33 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0025_spark_plan_collect... |
| cases/PORT/PORT_0025/runs/spark/plans/rewrite_pos_01.txt | sanitizable evidence | plan/failure observability | keep_with_public_sanitized_copy_later | line 18 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0025_spark_plan_collect...;line 33 categories=local_path snippet=Location: InMemoryFileIndex [file:/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0025/runs/spark/plans/_tmp_spark_plan_collection/warehouse/port_0025_spark_plan_collect... |
