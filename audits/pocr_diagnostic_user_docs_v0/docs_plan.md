# Docs Plan

Preferred docs location was inspected before editing.

Result:

- No `docs/user/` directory exists.
- The fallback location `docs/pocr_diagnostic.md` was used.
- The existing `examples/` layout supports subdirectories, so `examples/pocr_diagnostic/README.md` was added.
- `docs/README.md` and `examples/README.md` were updated as indexes only.

The documentation is concise user-facing guidance. It does not add route-alias policy, compute POCR, aggregate route-level POCR, promote paper metrics, or alter CLI behavior.

Documentation topics:

- what `sqlrb user pocr-diagnostic` is;
- what it is not;
- required and optional arguments;
- annotation-missing example;
- matching-route replay example;
- route-mismatch fail-closed example;
- D035 output tree;
- D036/D037 POCR evidence boundaries.
