# Legacy Evidence Boundary

Old R-Bot results are legacy facts only.

They may guide:

- wrapper design;
- output-contract expectations;
- denominator-aware boundary wording;
- failure bucket planning;
- future live smoke selection.

They must not be used as:

- new canonical local metrics;
- `local_metrics.py` outputs;
- paper results;
- retained evidence promotion;
- leaderboard input;
- evidence that the adapted GPT-5.4 route reproduces the original paper stack.

Any future canonical local diagnostic must run through `python -m cli.main user evaluate` and, if metrics are authorized, `python -m cli.main user compute-local-metrics`.
