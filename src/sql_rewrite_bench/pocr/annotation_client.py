"""Stage A annotation client interfaces.

Only fake/offline mode is executable in this scaffold. The future
OpenAI-compatible live mode fails closed and intentionally does not read API
keys or perform network calls in this task.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, annotation_from_mapping


@dataclass(frozen=True)
class AnnotationClientConfig:
    mode: str
    provider_policy: str = "openai_compatible"
    model_policy: str = "gpt-5.4"
    allow_live: bool = False


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


class OpenAICompatibleAnnotationClient:
    """Future live client placeholder that currently fails closed."""

    def __init__(self, config: AnnotationClientConfig):
        self.config = config
        if not config.allow_live:
            raise RuntimeError("live annotation mode is disabled; explicit allow_live is required")
        raise RuntimeError("live annotation mode is not implemented in this scaffold")

    def annotate(self, prompt: str) -> CandidateAnnotation:  # pragma: no cover - constructor always fails.
        raise RuntimeError("live annotation mode is not implemented in this scaffold")


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
