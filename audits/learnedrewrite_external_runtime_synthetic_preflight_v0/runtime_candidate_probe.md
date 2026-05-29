# Runtime Candidate Probe

External runtime candidate:

```text
/tmp/sqlrb_prior_methods_sources/LearnedRewrite/rewriter_java.jar
```

## Candidate File

- Exists: yes
- File size: 45101062 bytes
- SHA-256: `07faf6ba08b381225f9c547235c45d4c37dfc2fe838be3276fd264f71e3a4d87`
- Copied into release repo: no

## Java

Java is available:

```text
openjdk version "17.0.18" 2026-01-20
```

## Manifest / Help

Safe manifest inspection succeeded:

```text
Manifest-Version: 1.0
Main-Class: server
```

`jar tf` shows the JAR carries `calcite_core_main_jar/`, `server.class`, `main/schema.json`, and `rules_for_selected/` entries.

A bounded `--help` probe was attempted from `/tmp` with `timeout 8s`. It printed no help/version text and exited by timeout. This indicates the JAR behaves as a server entrypoint rather than a CLI help tool.

## Server Mode

The server starts and listens on port `6336` when run without arguments. A first diagnostic startup with `--server.port=26336` did not bind `26336`; a default startup bound `6336`. This suggests the recovered official default port is the only verified mode in this task.

## Dependencies / Working Directory

The synthetic preflight request showed a working-directory dependency:

```text
java.io.FileNotFoundException: rules_for_selected/standard.txt (No such file or directory)
```

The server was intentionally started from a temporary working directory under `/tmp` to avoid modifying the external upstream checkout. Starting it from `/tmp/sqlrb_prior_methods_sources/LearnedRewrite/` might satisfy the relative `rules_for_selected/standard.txt` dependency, but the runtime writes `request.txt` in the working directory. Running it from the upstream source directory would therefore modify external files, which is not authorized in this task.

## Runtime Mode Verdict

- Command mode: not established. No row-scoped command API was found.
- HTTP mode: partially available. The JAR starts a local `/rewriter` server on port `6336`, but the synthetic request failed before producing candidate SQL because relative runtime assets were missing from the temp working directory.
- Ready for user-facade external runtime smoke: no.
