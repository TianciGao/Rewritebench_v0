# PORT runs retention preview summary

Generated: 2026-05-15

This summary applies the approved policy decision. No legacy evidence was sanitized, moved, deleted, rewritten, or copied.

## Policy decision applied

- Public release should keep sanitized public copies for sanitizable Spark plan evidence.
- Original legacy plan artifacts must be retained through mapping and may stay in private/external archive.
- Raw local path traces must not appear in public retained evidence.
- PORT_0024 Spark result-check stdout/stderr log references should be summarized or archived, not exposed raw by default.

## Case preview table

| case_id | evidence-index preview | sanitizable evidence | private/archive mapping needed | physical pilot blocked | human approval needed | notes |
|---|---:|---:|---:|---:|---:|---|
| PORT_0004 | yes | 0 | 0 | no | no | clean preview; no current local-path or log-reference risk |
| PORT_0008 | yes | 2 | 2 | yes | yes | Spark plan local-path traces require sanitized public copies |
| PORT_0012 | yes | 2 | 2 | yes | yes | Spark plan local-path traces require sanitized public copies |
| PORT_0013 | yes | 2 | 2 | yes | yes | Spark plan local-path traces require sanitized public copies |
| PORT_0022 | yes | 2 | 2 | yes | yes | Spark plan local-path traces require sanitized public copies |
| PORT_0024 | yes | 2 | 3 | yes | yes | Spark plan local-path traces require sanitized public copies; Spark result_check has stdout/stderr log references |
| PORT_0025 | yes | 2 | 2 | yes | yes | Spark plan local-path traces require sanitized public copies |

## Clean evidence-index previews

All seven PORT cases now have proposed `runs_retention.yaml` preview mappings. These previews can feed later case-local `evidence/runs_retention.yaml` files after migration approval.

## Cases needing sanitized public copies

PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, and PORT_0025 each have Spark plan artifacts with local-path traces. Their previews propose sanitized public plan copies and private/original archive mappings.

## Private/external archive mapping

The original raw Spark plan artifacts remain do-not-delete evidence. PORT_0024 also needs archive or summary handling for the Spark `result_check.json` stdout/stderr log references.

## Why PORT_0004 is different

PORT_0004 has no current high-risk trace in this checkout and is cleared for evidence-index normalization and copy-first physical pilot, subject to normal runs-retention mapping.

## Why six cases remain physical-pilot blocked

The six blocked cases need sanitized public copies or archive mappings implemented before physical migration. The previews record the mapping shape, but no sanitized files exist yet.

## How previews feed real case files

A later approved migration can copy each preview into the migrated case as `evidence/runs_retention.yaml`, then replace proposed placeholders with actual sanitized public paths, archive paths, and approval metadata.
