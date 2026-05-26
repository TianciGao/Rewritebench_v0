# Default-Off Live Annotation Policy

POCR live annotation remains default-off.

Existing `sqlrb user pocr-diagnostic` modes:

- Annotation-missing mode: no annotation JSONL is supplied; no API key is read; no API call occurs.
- Replay mode: an existing annotation JSONL file is supplied; no API key is read; no API call occurs.

Future live annotation must require:

- `--enable-pocr-diagnostic`
- `--enable-pocr-live-annotation`
- explicit LLM provider configuration
- an API key environment variable name
- an explicit live LLM gate

Generated annotation JSONL must follow `docs/pocr_annotation_artifacts.md` and remain diagnostic evidence unless a separate task promotes it.

Stage A annotation alone is not counted. Stage B transformation-aware validation is diagnostic only. No official POCR is computed. No route-level POCR score is emitted. No paper-facing metric is promoted. No global leaderboard is produced.
