# PORT public release risk table

No immediate deletion is recommended. Risks are grouped for later sanitization/archive decisions.

## local path / host / WSL / localhost

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| PORT_0008 | cases/PORT/PORT_0008/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0008 | cases/PORT/PORT_0008/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0012 | cases/PORT/PORT_0012/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0012 | cases/PORT/PORT_0012/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0013 | cases/PORT/PORT_0013/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0013 | cases/PORT/PORT_0013/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0022 | cases/PORT/PORT_0022/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0022 | cases/PORT/PORT_0022/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0024 | cases/PORT/PORT_0024/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0024 | cases/PORT/PORT_0024/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0025 | cases/PORT/PORT_0025/runs/spark/plans/rewrite_neg_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |
| PORT_0025 | cases/PORT/PORT_0025/runs/spark/plans/rewrite_pos_01.txt | medium | local host/path trace can leak maintainer environment or make evidence non-portable | keep_with_public_sanitized_copy_later |

## prompt / API / token / assistant / model trace

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| none | none | low | no matching risk found | none |

## Spark warehouse / parquet / crc / _SUCCESS

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| none | none | low | no matching risk found | none |

## logs / stderr / debug residue

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| PORT_0024 | cases/PORT/PORT_0024/runs/spark/result_check.json | medium | logs/debug output can include environment traces and should not be public by default | move_to_external_archive_later |

## evidence role unclear

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| none | none | low | no matching risk found | none |

## large/binary files

| case | file or file group | severity | why it matters for public release | recommended action |
|---|---|---|---|---|
| none | none | low | no matching risk found | none |
