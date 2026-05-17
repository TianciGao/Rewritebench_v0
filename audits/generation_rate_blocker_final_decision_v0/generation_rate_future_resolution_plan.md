# Generation Rate Future Resolution Plan

## Recommended Path

Keep Generation Rate blocked for public v0. Resolve it later only through observed evidence improvement or a separately authorized policy decision.

## Evidence Work

1. Collect or project source-observed generated evidence for SQLGlot routes using only approved sanitized non-timing sources.
2. Confirm row grain at `case_id x engine x rewrite_method` before any parser or overlay step.
3. Preserve unresolved and unauthorized rows as denominator-visible partitions.
4. Keep observed generated evidence separate from inferred generated evidence.

## Policy Work

1. Define whether `ready=true` means emitted candidate SQL or only downstream readiness.
2. Decide whether inferred generated can ever support official Generation Rate.
3. If inference is authorized, require separate observed and inferred numerator columns.
4. Require explicit caveats for any diagnostic Generation/Readiness table.

## Validation Work

1. Rerun a readiness gate if Generation Rate policy or SQLGlot evidence changes.
2. Confirm denominator preservation against `denominator_same_engine_120.csv`.
3. Confirm no global leaderboard output.
4. Confirm no paper rendering or reports/results writes unless separately authorized.

## Timing Boundary

Timing, latency, speedup, and performance metrics remain separate. Generation Rate resolution must not parse timing arrays or use timing artifacts as candidate-generation evidence.

## Next Safe Action

Run `non_status_metric_na_backlog_closure_bundle_v0` before final renderer input packaging. Treat a Generation/Readiness diagnostic table as optional future work requiring separate authorization.
