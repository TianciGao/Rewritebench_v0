# R-Bot GPT-5.4 Adapter Scaffold v0

This packet records a fixture-only scaffold for an adapted R-Bot local diagnostic route.

## Summary

- Added `baselines/rbot/adapter.py`.
- Added fake/no-live fixture tests under `tests/user_entry/test_rbot_adapter.py`.
- Route id: `rbot_gpt54_adapted`.
- Method id: `rbot`.
- Future provider policy: OpenAI-compatible / GPTSAPI-compatible, `gpt-5.4`, live gate `SQLRB_LLM_ALLOW_LIVE=1`.
- Current task mode: fake runtime only.

This is not an original R-Bot paper reproduction. It does not invoke the official LLM4Rewrite stack, RAG/Chroma, CalciteRewrite, DB execution, checker, timing, local metrics, verifier, paper rendering, or Track A 120.

## Smoke Result

A tiny fake-runtime user-facade smoke was run over `PERF_0006/postgres` and `CONS_0036/postgres` with no DB/checker/timing flags. It selected 2 rows and generated 2 fake candidate SQL files. Runtime outputs under `/tmp` and `runs/user/` were removed before commit.

## Next Safe Action

If this scaffold is accepted, authorize a tiny bounded live GPT-5.4 R-Bot-adapted generation smoke over 1-2 PostgreSQL rows. Do not run DB/checker/timing or Track A 120 until live generation is stable.
