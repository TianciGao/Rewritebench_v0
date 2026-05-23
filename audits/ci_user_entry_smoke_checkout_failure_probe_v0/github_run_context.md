# GitHub Run Context

Observed failed run:
- Workflow: `user-entry-smoke`
- Run number: `453`
- Run id: `26329489901`
- Event: `push`
- Commit: `0c53cc7d492bc14cf4bf9d97506ce86e002b4976`
- Created: `2026-05-23T09:40:41Z`
- Conclusion: `failure`
- Failed step: `Checkout repository`
- Later steps: skipped
- Reported checkout symptom: `/usr/bin/git` exited with code `128`; `could not read Username for 'https://github.com': terminal prompts disabled`

Same-commit user-entry rerun/sibling run:
- Workflow: `user-entry-smoke`
- Run number: `454`
- Run id: `26329490534`
- Event: `pull_request`
- Commit: `0c53cc7d492bc14cf4bf9d97506ce86e002b4976`
- Created: `2026-05-23T09:40:44Z`
- Conclusion: `success`
- Checkout: success
- Python setup and all smoke steps: success

Same-commit ledger comparison:
- Workflow: `Ledger fixture smoke`
- Run number: `551`
- Run id: `26329489902`
- Event: `push`
- Commit: `0c53cc7d492bc14cf4bf9d97506ce86e002b4976`
- Created: `2026-05-23T09:40:41Z`
- Conclusion: `success`
- Checkout: success

Interpretation:
- The failure was isolated to one `actions/checkout` attempt on the push-triggered `user-entry-smoke` run.
- The same commit was checkable by the ledger push workflow and by the user-entry pull-request workflow.
- This points to a transient GitHub checkout/token/remote credential issue or event-specific run context issue, not a repository code failure.

