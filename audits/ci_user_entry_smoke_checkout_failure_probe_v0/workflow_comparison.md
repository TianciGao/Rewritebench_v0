# Workflow Comparison

Compared files:
- `.github/workflows/user_entry_smoke.yml`
- `.github/workflows/ledger-fixture-smoke.yml`

Checkout configuration:
- `user_entry_smoke.yml`: `uses: actions/checkout@v4`
- `ledger-fixture-smoke.yml`: `uses: actions/checkout@v4`
- Neither workflow sets checkout `with:` options.
- Neither workflow enables submodules or LFS through checkout options.
- Both workflows use `permissions: contents: read`.

Other repository checks:
- No `.gitmodules` file was found.
- No local `submodule.*` git config was found.
- No `.gitattributes` file was found in the shallow inspected tree, so no repository LFS attribute rule was detected.

Difference assessment:
- The meaningful workflow differences are after checkout: Python setup, smoke commands, diff checks, and artifact upload.
- The failed `user-entry-smoke` run stopped at checkout, before any of those later differences could execute.
- Commit `0c53cc7d492bc14cf4bf9d97506ce86e002b4976` did not modify `.github/workflows/`.

Conclusion:
- No malformed checkout option, submodule behavior, LFS behavior, permissions difference, or workflow-specific checkout configuration difference was found.
- No workflow file change is justified by the evidence from this probe.

