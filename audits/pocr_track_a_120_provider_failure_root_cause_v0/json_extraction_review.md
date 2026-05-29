# JSON Extraction Review

The current live client reads OpenAI-compatible `choices[0].message.content`, rejects empty content, strips a full Markdown code fence, and then calls `json.loads`. This handles raw JSON objects and simple fenced JSON blocks.

Safe cases currently handled:
- raw JSON object
- markdown fenced JSON when the whole response is fenced

Cases not broadly handled:
- leading/trailing prose around JSON
- stringified JSON nested inside another JSON string
- partial/truncated JSON
- multiple JSON objects

Improving extraction could help earlier malformed JSON rows only if the provider returns recoverable fenced/prose-wrapped JSON. It would not fix the 150-row retry failure because those calls failed before usable annotation content was available. Any extraction expansion should be narrow and tested to avoid over-accepting prose or partial objects.

Proposed tests if implemented later: fenced JSON with `json` language tag, leading/trailing prose containing one object, empty response fail-closed, and truncated JSON fail-closed.

Further blind retry is not recommended until the provider configuration failure is fixed.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
