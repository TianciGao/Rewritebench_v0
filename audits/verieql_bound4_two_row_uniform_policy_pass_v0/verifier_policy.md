# Verifier Policy

Declared uniform policy:
- verifier tool: `verieql`
- verifier mode: `finite_bound`
- bound size: 4
- timeout seconds: 30
- cores: 1
- schema canonicalization: enabled
- result checker exactness used as verifier evidence: false

Policy identifier:
- `finite_bound_bound4_timeout30_cores1`

Boundary:
- The output is tied to this declared policy only.
- It does not imply equivalence under `bound_size=10`.
- It must not be mixed with earlier `bound_size=10` results inside one denominator.
- It is a local diagnostic verifier-support result, not official Semantic Equivalence Rate.

