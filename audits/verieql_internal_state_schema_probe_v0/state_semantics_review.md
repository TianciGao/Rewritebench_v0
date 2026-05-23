# State Semantics Review

## Source Locations

Inspected VeriEQL root:

`/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL`

Key files inspected:

- `constants.py`
- `parallel/cli_within_timeout.py`
- `parallel/cli_within_bound.py`
- `errors.py`
- `environment.py`

## State Meanings

`constants.py` defines the state abbreviations:

- `EQU`: finite-bound equivalence result for the current bound.
- `NEQ`: non-equivalence found, usually with a counterexample.
- `TMO`: timeout.
- `NSE`: not-supported feature.
- `UNK`: unknown.
- `SYN`: syntax error.
- `NIE`: not-implemented error.
- `OOM`: out of memory.
- `OTE`: other error.

`errors.py` confirms the exception mapping used by the runner:

- `NotEquivalenceError`: non-equivalent.
- `NotSupportedError`: unsupported feature, with messages such as `Not supported feature: ...`.
- `UnknownError`: symbolic reasoning unknown.

## Multiple States Per Pair

A single JSONL pair can produce multiple states in `parallel/cli_within_timeout.py`.

The timeout runner starts at a finite `bound_size`, verifies the pair, and appends the resulting state. If the state is `EQU`, it increments the bound and starts another verification process for the same pair. It stops only when a non-`EQU` state appears or when the timeout loop expires.

Therefore:

- `["NEQ"]` means a counterexample was found at the first checked bound.
- `["EQU", "NEQ"]` means the first finite bound had no counterexample, but a larger bound did.
- `["EQU", "EQU", "TMO"]` means smaller finite bounds returned equivalence and the next attempted bound timed out.
- `["NSE"]` means VeriEQL rejected the pair due an unsupported feature before producing equivalence evidence.

## TMO After EQU

For SQL-RewriteBench local verifier-support policy, a `TMO` anywhere in the state list keeps the normalized verdict as `timeout`. Earlier `EQU` states remain useful tool-behavior signals, but they are not clean formal equivalence evidence for the pair.

This aligns with the previous timeout-policy probe: partial `EQU+TMO` must not be promoted to official Semantic Equivalence Rate evidence.

## Upstream Summary Difference

The upstream timeout runner includes summary logic that can count `EQU...TMO` histories as successful for its own benchmark reporting. That is upstream tooling behavior, not the SQL-RewriteBench local verifier-support policy. The release wrapper should keep the stricter classification unless a separate durable decision changes the evidence policy.
