# Source Review

## README

The VeriEQL README documents two batch modes:

- timeout mode: `python -m parallel.cli_within_timeout -f XX.jsonlines -t 600 -o XX.out`
- finite-bound mode: `python -m parallel.cli_within_bound -f XX.jsonlines -s 10 -o XX.out`

This task used finite-bound mode.

## Finite-Bound Runner

`parallel/cli_within_bound.py` accepts:

- `-f/--file`
- `-s/--bound_size`
- `-t/--timeout`
- `-c/--cores`
- `-i/--integrity_constraint`
- `-o/--out_file`

The runner loads each JSONL record, reads `index`, `schema`, `constraint`, and `pair`, then calls `process_ends_with_max_bound_size(...)`.

For each pair, it loops from bound size 1 through the requested `--bound_size`. It appends a state for each bound and stops when a state is not `EQU`. Therefore:

- an equivalent pair can emit all `EQU` states up to the requested finite bound;
- a non-equivalent pair can emit `NEQ` at the first bound where a counterexample is found;
- timeout, unsupported, syntax, implementation, OOM, unknown, or other errors remain visible in the state list.

## Timeout Runner Contrast

`parallel/cli_within_timeout.py` keeps increasing finite bounds after each `EQU` until timeout or a non-`EQU` state. That explains prior `EQU...TMO` histories for equivalent-looking pairs. Finite-bound mode gives the caller an explicit stopping bound and can avoid appending `TMO` after the last requested successful bound.

## State Constants

`constants.py` defines:

- `EQU`
- `NEQ`
- `UNK`
- `TMO`
- `SYN`
- `NIE`
- `NSE`
- `OOM`
- `OTE`

`errors.py` maps `NotEquivalenceError` to non-equivalence and `NotSupportedError` to unsupported feature.

## Input Shape

Bundled benchmark JSONL examples use uppercase schema table/column identifiers such as `PERSON`, `PERSONID`, `EMP`, and `EMPNO`. The parser appears to uppercase SQL identifiers internally. This matters for wrapper schema generation.
