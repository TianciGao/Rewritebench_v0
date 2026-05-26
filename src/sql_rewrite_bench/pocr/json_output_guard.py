"""Fail-closed JSON guard for Stage A annotation provider output."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GuardedJsonResult:
    raw_status: str
    parsed: dict[str, Any] | None
    repaired: bool
    fence_stripped: bool
    error: str
    repair_strategy: str = ""
    original_status: str = ""
    final_status: str = ""

    @property
    def schema_status(self) -> str:
        return "schema_pending" if self.parsed is not None else "schema_invalid"


def guarded_json_loads(
    raw: str | None,
    *,
    allow_code_fence: bool = True,
    allow_surrounding_text: bool = False,
    repair_mode: bool = False,
    timed_out: bool = False,
) -> GuardedJsonResult:
    """Parse strict JSON or explicitly allowed deterministic wrappers.

    This helper does not repair malformed JSON. `repair_mode` is accepted only
    to make accidental repair attempts fail explicitly.
    """

    if repair_mode:
        raise ValueError("JSON repair mode is not implemented or authorized")
    if timed_out:
        return _invalid("timeout", "provider call timed out or returned no response")
    if raw is None:
        return _invalid("no_response", "provider response was missing")
    text = raw.strip()
    if not text:
        return _invalid("empty_response", "provider response was empty")
    fence_stripped = False
    original_status = "valid_json_object"
    repair_strategy = ""
    if allow_code_fence and text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            opener = lines[0].strip().lower()
            if opener in {"```", "```json"}:
                text = "\n".join(lines[1:-1]).strip()
                fence_stripped = True
                original_status = "fenced_json_object"
                repair_strategy = "strip_json_code_fence"
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError as exc:
        if _looks_truncated(text):
            return _invalid("truncated_json", str(exc), fence_stripped=fence_stripped)
        multi_status = _multi_object_status(text)
        if multi_status:
            return _invalid(multi_status, str(exc), fence_stripped=fence_stripped)
        if _looks_like_surrounding_text(text):
            if allow_surrounding_text:
                extracted = _extract_single_json_object(text)
                if extracted is not None:
                    try:
                        decoded = json.loads(extracted)
                    except json.JSONDecodeError as inner_exc:
                        return _invalid(
                            "malformed_json",
                            str(inner_exc),
                            fence_stripped=fence_stripped,
                            original_status="provider_text_around_json",
                        )
                    if isinstance(decoded, dict):
                        return GuardedJsonResult(
                            raw_status="parsed",
                            parsed=decoded,
                            repaired=True,
                            fence_stripped=fence_stripped,
                            error="",
                            repair_strategy="extract_single_json_object",
                            original_status="provider_text_around_json",
                            final_status="parsed",
                        )
            return _invalid(
                "provider_text_around_json",
                "provider response contained text outside JSON object",
                fence_stripped=fence_stripped,
            )
        return GuardedJsonResult(
            raw_status="malformed_json",
            parsed=None,
            repaired=False,
            fence_stripped=fence_stripped,
            error=str(exc),
            original_status="malformed_json",
            final_status="schema_invalid",
        )
    if not isinstance(decoded, dict):
        return GuardedJsonResult(
            raw_status="not_json_object",
            parsed=None,
            repaired=False,
            fence_stripped=fence_stripped,
            error="parsed JSON is not an object",
            original_status="non_object_json",
            final_status="schema_invalid",
        )
    return GuardedJsonResult(
        raw_status="parsed",
        parsed=decoded,
        repaired=bool(repair_strategy),
        fence_stripped=fence_stripped,
        error="",
        repair_strategy=repair_strategy,
        original_status=original_status,
        final_status="parsed",
    )


def _invalid(
    status: str,
    error: str,
    *,
    fence_stripped: bool = False,
    original_status: str | None = None,
) -> GuardedJsonResult:
    return GuardedJsonResult(
        raw_status=status,
        parsed=None,
        repaired=False,
        fence_stripped=fence_stripped,
        error=error,
        original_status=original_status or status,
        final_status="schema_invalid",
    )


def _multi_object_status(text: str) -> str:
    decoder = json.JSONDecoder()
    try:
        first, index = decoder.raw_decode(text)
    except json.JSONDecodeError:
        return ""
    remainder = text[index:].strip()
    if not remainder:
        return ""
    try:
        second, second_index = decoder.raw_decode(remainder)
    except json.JSONDecodeError:
        return "provider_text_around_json"
    if isinstance(first, dict) and isinstance(second, dict) and not remainder[second_index:].strip():
        return "multi_object_response"
    return "provider_text_around_json"


def _looks_like_surrounding_text(text: str) -> bool:
    return "{" in text and "}" in text and not text.lstrip().startswith("{") or (
        text.lstrip().startswith("{") and not text.rstrip().endswith("}")
    )


def _looks_truncated(text: str) -> bool:
    stripped = text.rstrip()
    if stripped.endswith(("{", "[", ":", ",")):
        return True
    return (text.count("{") > text.count("}") or text.count("[") > text.count("]")) and not stripped.endswith("}")


def _extract_single_json_object(text: str) -> str | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            decoded, end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, dict):
            return text[index : index + end]
    return None
