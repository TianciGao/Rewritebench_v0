# Built-In Examples Review

## README Examples

The VeriEQL README documents:

- direct toy execution with `python -m __main__`,
- timeout batch execution with `parallel.cli_within_timeout`,
- bound batch execution with `parallel.cli_within_bound`.

The direct toy path uses the internal `Environment` API and a fixed finite row bound. It is useful as a tool-behavior clue but is not the same surface as the JSONL timeout runner used by the release wrapper.

## Test Examples

VeriEQL's test files include direct API examples that assert equivalent pairs under a finite row bound. These are evidence that a clean finite-bound equivalent path exists in the tool's internal API.

They do not prove that `parallel.cli_within_timeout` will emit a clean final `EQU` row, because timeout mode intentionally keeps increasing bounds after each `EQU`.

## Historical Output Files

Historical `.out` files under VeriEQL's `experiments/` directory contain many `EQU...TMO` records and clean `NEQ` records. A read-only scan did not find clean all-`EQU` timeout-mode output rows in the inspected experiment files.

This supports the interpretation that timeout-mode equivalence often appears as finite-bound `EQU` progress followed by timeout at a larger bound.

## Clean Equivalent Path Status

A clean equivalent toy/example path likely exists through one of these surfaces:

- direct finite-bound API,
- `parallel.cli_within_bound`,
- or a future wrapper mode that explicitly records finite-bound equivalence as local bounded evidence.

No clean equivalent path was confirmed through the current timeout-mode wrapper in this task.

## Evidence Boundary

Built-in examples and historical output are tool-behavior clues only. They are not SQL-RewriteBench Common-core evidence, not official Semantic Equivalence Rate inputs, and not retained evidence.
