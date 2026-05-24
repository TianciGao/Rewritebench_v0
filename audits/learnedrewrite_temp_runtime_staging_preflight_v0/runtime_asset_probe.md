# Runtime Asset Probe

External runtime candidate:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

## Candidate JAR

- Exists: yes
- File size: 45101062 bytes
- SHA-256: `07faf6ba08b381225f9c547235c45d4c37dfc2fe838be3276fd264f71e3a4d87`
- Copied into release repo: no

## Java

Java is available:

```text
openjdk version "17.0.18" 2026-01-20
OpenJDK Runtime Environment (build 17.0.18+8-Ubuntu-124.04.1)
OpenJDK 64-Bit Server VM (build 17.0.18+8-Ubuntu-124.04.1, mixed mode, sharing)
```

## Relative Runtime Assets

`rules_for_selected/standard.txt` exists under the external source tree:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rules_for_selected/standard.txt
```

Observed asset details:

| asset | exists | size_bytes | sha256 |
| --- | --- | ---: | --- |
| `rules_for_selected/standard.txt` | yes | 1389 | `364dcbfffd1b5b1e1297f9ec20d98fed94fc83c13deef521c1d6c929e4e7f0b2` |
| `rules_for_selected/user_selected_rules.txt` | yes | 1305 | `fa4ce73ee1af2705089d7f23928e1a31bb262ce56ce351f84e74c17c3b09808d` |

Other external runtime assets observed read-only:

- `calcite_core_main_jar/`
- `META-INF/`
- `src/main/schema.json`

## Workdir Decision

The runtime source writes `request.txt` in its working directory. Starting the
JAR directly from `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/` would risk
modifying the external source root. Therefore this task did not start the
runtime from that directory. Temp-only staging was used instead.

No asset was copied into this release repo.
