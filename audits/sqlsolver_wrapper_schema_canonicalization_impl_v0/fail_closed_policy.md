# Fail-Closed Policy

Unsafe canonicalization fails closed before SQLSolver invocation.

Unsupported features are reported as verifier-support limitations through guard categories and `unsupported` / not-attempted style outcomes where applicable. They must not be counted as rewrite-method failures.

Canonicalization must not fabricate verifier evidence. Passing a canary only means the wrapper/tool input path can parse and decide that synthetic identity shape; it does not prove benchmark semantic equivalence.

Canonicalization must not convert local checker exactness into SER. Local checker exactness remains Result Consistency evidence only.

Canonicalized SQLSolver inputs are temporary verifier inputs. The implementation does not mutate benchmark SQL, schema files, retained evidence, or paper artifacts.
