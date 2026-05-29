# Temp Staging Plan

Temporary staging directory:

```text
/tmp/sqlrb_learnedrewrite_runtime_staging_v0/
```

Staged support assets:

| staged asset | source path | reason | copied into release repo |
| --- | --- | --- | --- |
| `rules_for_selected/standard.txt` | `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rules_for_selected/standard.txt` | Required by `HepOpt` relative lookup | no |
| `rules_for_selected/user_selected_rules.txt` | `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rules_for_selected/user_selected_rules.txt` | Adjacent runtime rule-selection support file | no |

The external JAR was not copied. It was invoked by absolute path from the temp
workdir.

The runtime was started from the temp workdir so its `request.txt`, stdout, and
stderr stayed under `/tmp/sqlrb_learnedrewrite_runtime_staging_v0/` and were not
staged into the release repo.

Cleanup policy:

- shut down the Java server after the preflight;
- leave temp files under `/tmp` for local inspection only;
- commit only safe summaries in this audit packet.

No source, JAR, dependency JAR, dataset, checkpoint, generated output, request
log, or old result was copied into the release repo.
