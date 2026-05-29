# Verdict Normalization Policy

Allowed normalized verdicts:

- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `unsupported`
- `tool_error`
- `not_attempted`

Policy:

- Tool-native equivalent/proved/valid forms map to `equivalent`.
- Counterexample/not-equivalent forms map to `non_equivalent`.
- Inconclusive/undecidable forms map to `unknown`.
- Timeout status or timeout raw verdict maps to `timeout`.
- Unsupported syntax or unsupported tool status maps to `unsupported`.
- Invocation failure, parser failure, crash, and unrecognized raw verdict strings map to `tool_error`.
- Skipped/not-run forms map to `not_attempted`.

Fail-visible rule:

- Unknown raw strings do not become equivalence evidence. They normalize to `tool_error`.
- The literal raw verdict `unknown` remains `unknown`.

Decidable outcomes:

- Only `equivalent` and `non_equivalent` enter the Semantic Equivalence Rate denominator.
- `unknown`, `timeout`, `unsupported`, `tool_error`, and `not_attempted` remain separately counted.
