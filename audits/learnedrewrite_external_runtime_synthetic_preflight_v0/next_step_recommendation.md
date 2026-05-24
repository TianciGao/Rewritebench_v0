# Next Step Recommendation

Synthetic preflight result: failed.

The runtime starts and accepts a POST, but it fails before producing candidate SQL because a relative runtime asset is missing from the temporary working directory:

```text
rules_for_selected/standard.txt
```

Recommended next step:

1. Authorize a temp-only LearnedRewrite runtime staging task.
2. Stage the minimal required runtime asset directory into `/tmp`, not into the release repo.
3. Start `rewriter_java.jar` from that staged temp working directory.
4. Send exactly one synthetic non-benchmark request again.
5. If successful, implement real adapter HTTP mode and authorize a 1-2 row PostgreSQL-only D035 user-facade smoke without DB/checker/timing.

Do not run Common-core SQL, Track A 120, DB/checker/timing, metrics, or verifier until the synthetic runtime response yields one extractable SQL candidate and adapter real-runtime mode is implemented.
