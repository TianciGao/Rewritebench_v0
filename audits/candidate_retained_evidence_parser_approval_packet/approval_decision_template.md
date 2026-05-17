# Candidate Retained-evidence Parser Approval Decision Template

Task under review:

Bounded non-timing candidate retained-evidence parser for Track-A same-engine `rewrite_candidate_cell` rows.

## Decision Options

Select exactly one option.

### Option A - Approve Non-timing Candidate Status Parser Design Only

Decision:

- [ ] Approved

Meaning:

Design work may continue. No implementation, production retained-evidence parsing, row-status filling, timing parsing, metric input authorization, metrics computation, or paper rendering is authorized.

Required next artifact:

Input manifest and parser design spec.

### Option B - Approve Implementation Of Bounded Non-timing Parser

Decision:

- [ ] Approved

Meaning:

Implementation may proceed only for approved non-timing `rewrite_candidate_cell` status fields and only over the explicit input manifest attached to the approval.

Required restrictions:

- No timing fields.
- No metric computation.
- `metric_input_authorized=false`.
- No reports/results mutation.
- No denominator change.
- No paper-result change.
- No raw legacy evidence mutation.
- Fail closed on row-grain ambiguity.

Approved input manifest:

```text
TBD by maintainer
```

### Option C - Defer Pending Metric/team Review

Decision:

- [ ] Deferred

Reason:

```text
TBD by maintainer
```

Meaning:

No parser implementation is authorized. Existing scaffold and unresolved overlay remain the current state.

### Option D - Reject Due To Evidence Ambiguity

Decision:

- [ ] Rejected

Reason:

```text
TBD by maintainer
```

Meaning:

Do not implement a candidate retained-evidence parser from the current evidence surfaces. Revisit only after retained evidence is curated or row-grain evidence improves.

## Required Maintainer Notes

Scope clarifications:

```text
TBD
```

Explicit exclusions:

```text
TBD
```

Approval date:

```text
TBD
```

Approver:

```text
TBD
```
