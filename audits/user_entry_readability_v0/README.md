# User-Entry Readability Commands v0

## Purpose

This packet records U6 user-readability enhancements for the user-entry path.

The implementation adds command-only helpers so users can inspect Common-core
case-set membership, explain a case-engine selection, and inspect local output
schemas before running an adapter.

## Commands Added

- `--list-cases`
- `--explain-selection`
- `--show-output-schema`

## Boundary

- U6 adds user readability commands only.
- The commands do not invoke adapters when used alone.
- The commands do not create `runs/user/...` output directories when used alone.
- Timing/speedup computed: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Retained evidence parsed or promoted: no.
- Global leaderboard created: no.
- Denominator changed: no.
- Case membership changed: no.

## Verdict

U6 readability commands are complete for the current user-entry local diagnostic
path.

## Next Safe Action

Human review of the readability command output, then authorize U7 engine
execution router and MySQL/Spark fail-closed interface design if accepted.
