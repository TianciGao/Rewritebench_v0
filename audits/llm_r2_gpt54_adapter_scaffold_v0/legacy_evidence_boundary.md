# Legacy Evidence Boundary

Old LLM-R2 results are legacy facts only.

They may guide:

- wrapper design;
- fixture shape;
- failure bucket planning;
- route-boundary wording;
- extraction-risk tests.

They must not be:

- imported as new canonical metrics;
- copied into `runs/user/` or top-level `reports/` / `results/`;
- mixed into `local_metrics.py` outputs;
- promoted to retained evidence in this task;
- treated as Track A 120 evidence.

Any future new LLM-R2 result requires a fresh D035 user-facade run followed by
`compute-local-metrics` only if that run is explicitly authorized.
