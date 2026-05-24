# Runtime Staging Review

External runtime JAR:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

Required external asset:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rules_for_selected/
```

Observed hashes:

| asset | sha256 |
| --- | --- |
| `rewriter_java.jar` | `07faf6ba08b381225f9c547235c45d4c37dfc2fe838be3276fd264f71e3a4d87` |
| `rules_for_selected/standard.txt` | `364dcbfffd1b5b1e1297f9ec20d98fed94fc83c13deef521c1d6c929e4e7f0b2` |

Temp staging path used outside the release repo:

```text
/tmp/sqlrb_learnedrewrite_pg40_bounded_local_diagnostic_v0/runtime_staging/
```

Runtime port: `6336`.

Startup status: started and accepted HTTP requests.

Shutdown status: stopped after the diagnostic; no `rewriter_java.jar` process or port `6336` listener remained.

Release-repo vendor boundary: no JAR, source, rules asset, generated runtime output, request log, dependency JAR, or upstream asset was copied into this repository.
