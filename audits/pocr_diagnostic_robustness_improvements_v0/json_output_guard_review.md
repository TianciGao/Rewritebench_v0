# JSON Output Guard Review

The JSON guard now classifies valid JSON objects, fenced JSON objects, surrounding whitespace, provider text around JSON, truncated JSON, empty responses, non-object JSON, multi-object responses, and timeout/no-response conditions.

Fenced JSON is accepted only through deterministic fence stripping and records `repaired=true` with `repair_strategy=strip_json_code_fence`. Provider text before/after JSON fails closed by default; deterministic extraction is available only behind an explicit option and records `repair_strategy=extract_single_json_object`.

No malformed row may become schema-valid without deterministic parse plus downstream schema validation.
