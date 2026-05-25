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

    @property
    def schema_status(self) -> str:
        return "schema_pending" if self.parsed is not None else "schema_invalid"


def guarded_json_loads(raw: str, *, allow_code_fence: bool = True, repair_mode: bool = False) -> GuardedJsonResult:
    """Parse strict JSON or one safe JSON code fence.

    This helper does not repair malformed JSON. `repair_mode` is accepted only
    to make accidental repair attempts fail explicitly.
    """

    if repair_mode:
        raise ValueError("JSON repair mode is not implemented or authorized")
    text = raw.strip()
    fence_stripped = False
    if allow_code_fence and text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            opener = lines[0].strip().lower()
            if opener in {"```", "```json"}:
                text = "\n".join(lines[1:-1]).strip()
                fence_stripped = True
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError as exc:
        return GuardedJsonResult(
            raw_status="malformed_json",
            parsed=None,
            repaired=False,
            fence_stripped=fence_stripped,
            error=str(exc),
        )
    if not isinstance(decoded, dict):
        return GuardedJsonResult(
            raw_status="not_json_object",
            parsed=None,
            repaired=False,
            fence_stripped=fence_stripped,
            error="parsed JSON is not an object",
        )
    return GuardedJsonResult(
        raw_status="parsed",
        parsed=decoded,
        repaired=False,
        fence_stripped=fence_stripped,
        error="",
    )
