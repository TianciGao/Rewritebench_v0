# Engine Metrics Review

Canonical per-engine metrics:

| engine | selected | generated | source executable | candidate executable | exact | mismatch | unsupported | timed | generation | execution coverage | result consistency | GM speedup |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| postgres | 40 | 40 | 40 | 40 | 39 | 1 | 0 | 34 | 1.0 | 1.0 | 0.975 | 1.0207730373187183 |
| mysql | 40 | 40 | 40 | 40 | 32 | 8 | 0 | 29 | 1.0 | 1.0 | 0.8 | 1.0022893818022647 |
| spark | 40 | 40 | 35 | 32 | 31 | 1 | 5 | 27 | 1.0 | 0.8 | 0.775 | 1.015498492165199 |

Note: canonical metrics output uses the generic user-adapter route id `adapter_c8e9bc8dc8ca`; adapter status metadata records the Direct LLM route/method as `direct_llm_original`.
