# Timing Review

Copied from `local_metrics.py` outputs only.

- exact rows: 111
- timed exact rows: 98
- timing eligible rows: 98
- timing partial failures: 0
- speedup denominator: 98
- timing-ineligible exact rows: 13
- timing-ineligible exact reason: `timing_scope_not_supported` for 13 PORT rows.

Speedup distribution:

```text
gm_speedup_ratio=0.9978498743494606
p10=0.9350245899377606
p25=0.9941671005127753
p50=1.0037084775530145
p75=1.0119714589375732
p90=1.0704591883635644
```

Timing NA reason counts from the route ledger:

```text
{'': 98, 'checker_not_success': 4, 'timing_scope_not_supported': 13, 'unsupported_fail_closed': 5}
```
