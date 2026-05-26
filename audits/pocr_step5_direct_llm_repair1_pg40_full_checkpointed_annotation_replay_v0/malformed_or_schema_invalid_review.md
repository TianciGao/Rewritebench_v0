# Malformed Or Schema Invalid Review

Fail-closed annotation rows: 5.

- `LONGTAIL_0012`: annotation_status=`malformed_json`, call_status=`malformed_json`, error_type=`JSONDecodeError`.
- `PERF_0013`: annotation_status=`malformed_json`, call_status=`malformed_json`, error_type=`JSONDecodeError`.
- `PERF_0017`: annotation_status=`timeout`, call_status=`timeout`, error_type=`TimeoutError`.
- `PERF_0033`: annotation_status=`malformed_json`, call_status=`malformed_json`, error_type=`JSONDecodeError`.
- `PERF_0052`: annotation_status=`timeout`, call_status=`timeout`, error_type=`TimeoutError`.

These rows remain diagnostic fail-closed rows and are not repaired or promoted in this task.
