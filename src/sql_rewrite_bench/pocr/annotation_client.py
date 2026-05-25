"""Stage A annotation client interfaces.

Fake/offline mode remains available for tests. OpenAI-compatible live mode is
guarded by explicit caller configuration and environment-only secrets.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, annotation_from_mapping


@dataclass(frozen=True)
class AnnotationClientConfig:
    mode: str
    provider_policy: str = "openai_compatible"
    model_policy: str = "gpt-5.4"
    allow_live: bool = False
    base_url: str = ""
    api_key: str = ""
    api_key_env_used: str = ""
    auth_header: str = "authorization_bearer"
    timeout_seconds: float = 60.0
    max_tokens: int = 4000


@dataclass(frozen=True)
class AnnotationCallResult:
    annotation: CandidateAnnotation
    provider_label: str
    model_label: str
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


class FakeAnnotationClient:
    """Offline fixture client that returns a pre-supplied annotation payload."""

    def __init__(self, fixture_response: CandidateAnnotation | Mapping[str, Any] | str):
        if isinstance(fixture_response, CandidateAnnotation):
            self._annotation = fixture_response
        elif isinstance(fixture_response, str):
            self._annotation = annotation_from_mapping(json.loads(fixture_response))
        else:
            self._annotation = annotation_from_mapping(fixture_response)

    def annotate(self, prompt: str) -> CandidateAnnotation:
        if not prompt.strip():
            raise ValueError("prompt is required")
        return self._annotation

    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult:
        annotation = self.annotate(prompt)
        return AnnotationCallResult(
            annotation=annotation,
            provider_label="fake",
            model_label="fixture",
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
        )


class OpenAICompatibleAnnotationClient:
    """Minimal OpenAI-compatible live client for bounded POCR smokes."""

    def __init__(self, config: AnnotationClientConfig):
        self.config = config
        if not config.allow_live:
            raise RuntimeError("live annotation mode is disabled; explicit allow_live is required")
        if config.provider_policy != "openai_compatible":
            raise RuntimeError("live annotation mode only supports provider_policy=openai_compatible")
        if not config.base_url:
            raise RuntimeError("live annotation mode requires an OpenAI-compatible base URL")
        if not config.api_key:
            raise RuntimeError("live annotation mode requires an API key from environment")
        if not config.model_policy:
            raise RuntimeError("live annotation mode requires a model label")
        if config.auth_header not in {"authorization_bearer", "x-api-key"}:
            raise RuntimeError("auth_header must be authorization_bearer or x-api-key")

    def annotate(self, prompt: str) -> CandidateAnnotation:
        return self.annotate_with_metadata(prompt).annotation

    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult:
        if not prompt.strip():
            raise ValueError("prompt is required")
        response = self._call_chat_completions(prompt)
        content = _response_content(response)
        if not content.strip():
            raise RuntimeError("provider response did not contain annotation content")
        annotation = annotation_from_mapping(json.loads(_strip_json_fence(content)))
        usage = response.get("usage") if isinstance(response, dict) else {}
        if not isinstance(usage, dict):
            usage = {}
        return AnnotationCallResult(
            annotation=annotation,
            provider_label=self.config.provider_policy,
            model_label=self.config.model_policy,
            prompt_tokens=_optional_int(usage.get("prompt_tokens")),
            completion_tokens=_optional_int(usage.get("completion_tokens")),
            total_tokens=_optional_int(usage.get("total_tokens")),
        )

    def _call_chat_completions(self, prompt: str) -> dict[str, Any]:
        body = {
            "model": self.config.model_policy,
            "messages": [
                {
                    "role": "system",
                    "content": "Return strict JSON only for the POCR Stage A annotation schema.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": self.config.max_tokens,
        }
        headers = {"Content-Type": "application/json", "User-Agent": "sql-rewritebench-pocr-live-smoke/0.1"}
        if self.config.auth_header == "x-api-key":
            headers["x-api-key"] = self.config.api_key
        else:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        request = urllib.request.Request(
            self.config.base_url.rstrip("/") + "/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"provider request failed: HTTP {exc.code}: {_redact(detail, self.config.api_key)[:300]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"provider request failed: {exc.reason}") from exc
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RuntimeError("provider response was not JSON") from exc
        if not isinstance(decoded, dict):
            raise RuntimeError("provider response JSON was not an object")
        return decoded


def build_annotation_client(
    config: AnnotationClientConfig,
    *,
    fixture_response: CandidateAnnotation | Mapping[str, Any] | str | None = None,
) -> FakeAnnotationClient | OpenAICompatibleAnnotationClient:
    """Build an annotation client for fake or future live mode."""

    if config.mode == "fake":
        if fixture_response is None:
            raise ValueError("fake annotation mode requires fixture_response")
        return FakeAnnotationClient(fixture_response)
    if config.mode == "live":
        return OpenAICompatibleAnnotationClient(config)
    raise ValueError(f"unsupported annotation client mode: {config.mode}")


def _response_content(response: Mapping[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, Mapping):
        return ""
    message = first.get("message")
    if isinstance(message, Mapping) and isinstance(message.get("content"), str):
        return message["content"]
    if isinstance(first.get("text"), str):
        return first["text"]
    return ""


def _strip_json_fence(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return stripped


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) else None


def _redact(value: str, secret: str) -> str:
    if secret:
        return value.replace(secret, "[REDACTED]")
    return value
