# Dependency and Environment Review

## SQLGlot

SQLGlot was available and used by the existing SQLGlot adapter.

- SQLGlot version: `30.2.1`

## Java / Calcite

Java was available:

- Java command: `/usr/bin/java`
- Java version: `openjdk version "17.0.18" 2026-01-20`

The Calcite adapter requires one of the configured external runtime paths/commands. In this shell, none of the following were configured:

- `SQLRB_CALCITE_HEP_CMD`
- `SQLRB_CALCITE_HEP_JAR`
- `SQLRB_CALCITE_HEP_ROOT`
- `SQLRB_CALCITE_HEP_JAVA`
- `SQLRB_CALCITE_HEP_MODE`
- `SQLRB_CALCITE_HEP_TIMEOUT`

As a result, Calcite HEP fail-closed planned all 120 rows and failed closed with `preflight_blocked` / `calcite_runtime_unavailable`.

## Secret Boundary

No live API was called and no API key was read. No secret values are recorded in this packet.
