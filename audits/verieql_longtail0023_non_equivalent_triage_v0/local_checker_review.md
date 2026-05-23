# Local Checker Review

Checker files inspected:

- `cases/LONGTAIL/LONGTAIL_0023/checker/checker.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/checker/normalization.yaml`
- `cases/LONGTAIL/LONGTAIL_0023/checker/compare_config.yaml`

Checker policy:

- Runtime oracle: source SQL result.
- Result comparison mode: semantic equivalence.
- Static evidence required: false.
- Outputs committed under the case package: not allowed.

Retained local run output inspected:

- `source_result.jsonl`: 5 rows
- `candidate_result.jsonl`: 5 rows
- Source and candidate retained witness rows are identical.

The first retained row in both files is:

```json
{"inbound_count": "3", "outbound_count": "2", "postid": "201", "title": "Disk cleanup tips", "total_links": "5"}
```

Interpretation:

- The local checker did not reveal result drift in the retained witness.
- The retained witness is not formal proof for all databases.
- However, because the source and candidate SQL files are byte-identical, the local checker is not the plausible cause of the observed source-candidate disagreement.

Classification impact:

- `possible_checker_false_accept` is not the primary classification for this row.
- The local checker remains a finite runtime diagnostic, not formal verifier evidence.
