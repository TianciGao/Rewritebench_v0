"""Verifier verdict normalization and schema validation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .pairs import boundary_flags_as_json

ALLOWED_VERDICTS = {
    "equivalent",
    "non_equivalent",
    "unknown",
    "timeout",
    "unsupported",
    "syntax_error",
    "not_implemented",
    "out_of_memory",
    "tool_error",
    "not_attempted",
}

DECIDABLE_VERDICTS = {"equivalent", "non_equivalent"}

VERDICT_FIELDS = [
    "pair_id",
    "tool",
    "tool_version",
    "invocation_status",
    "verdict",
    "raw_stdout_path",
    "raw_stderr_path",
    "runtime_ms",
    "timeout_seconds",
    "normalized_verdict",
    "verdict_reason",
    "artifact_paths",
    "local_diagnostic_only",
    "official_metric_input",
    "paper_result_input",
    "retained_evidence_promoted",
    "leaderboard_input",
]

_NORMALIZATION_ALIASES = {
    "equivalent": {
        "equivalent",
        "eq",
        "valid",
        "proved",
        "verified",
        "same",
        "semantically_equivalent",
        "semantic_equivalent",
        "true",
    },
    "non_equivalent": {
        "non_equivalent",
        "non-equivalent",
        "not_equivalent",
        "not equivalent",
        "counterexample",
        "counter_example",
        "different",
        "invalid",
        "refute",
        "refuted",
        "refutation",
        "false",
    },
    "unknown": {"unknown", "inconclusive", "undecidable", "unknown_or_undecidable"},
    "timeout": {"timeout", "timed_out", "time_limit", "time_limit_exceeded", "time limit exceeded"},
    "unsupported": {"unsupported", "unsupported_sql", "unsupported_syntax", "not_supported", "not supported"},
    "syntax_error": {"syntax_error", "syntax error", "syn"},
    "not_implemented": {"not_implemented", "not implemented", "nie", "implementation_missing"},
    "out_of_memory": {"out_of_memory", "out of memory", "oom", "memory_limit"},
    "tool_error": {"tool_error", "error", "exception", "crash", "parse_error", "failed", "failure"},
    "not_attempted": {"not_attempted", "not attempted", "not_run", "not run", "skipped"},
}

_STATUS_ALIASES = {
    "timeout": {"timeout", "timed_out"},
    "unsupported": {"unsupported", "not_supported"},
    "syntax_error": {"syntax_error"},
    "not_implemented": {"not_implemented"},
    "out_of_memory": {"out_of_memory"},
    "tool_error": {"tool_error", "error", "failed", "failure", "crash"},
    "not_attempted": {"not_attempted", "not_run", "skipped"},
}


def normalize_verdict(raw_verdict: Any, *, invocation_status: Any = None) -> str:
    """Normalize a synthetic/tool-native verdict to the shared vocabulary.

    Unknown raw strings fail visible as ``tool_error``. The literal raw verdict
    ``unknown`` and common inconclusive forms map to ``unknown``.
    """

    raw_text = _canonical_text(raw_verdict)
    status_text = _canonical_text(invocation_status)
    for normalized, aliases in _STATUS_ALIASES.items():
        if status_text in aliases:
            return normalized
    for normalized, aliases in _NORMALIZATION_ALIASES.items():
        if raw_text in aliases:
            return normalized
    if not raw_text:
        if status_text in {"completed", "success", "ok"}:
            return "unknown"
        return "not_attempted"
    return "tool_error"


def verdict_reason(raw_verdict: Any, normalized_verdict: str, *, invocation_status: Any = None) -> str:
    """Produce a short diagnostic reason for a normalized verdict."""

    raw_text = _canonical_text(raw_verdict)
    status_text = _canonical_text(invocation_status)
    if normalized_verdict == "tool_error" and raw_text and raw_text not in _NORMALIZATION_ALIASES["tool_error"]:
        return f"unrecognized_raw_verdict:{raw_text}"
    if status_text:
        return f"normalized_from_status:{status_text}"
    if raw_text:
        return f"normalized_from_raw:{raw_text}"
    return "no_raw_verdict"


def build_verdict_record(
    *,
    pair_id: str,
    tool: str,
    raw_verdict: Any,
    invocation_status: str = "completed",
    tool_version: str = "synthetic",
    raw_stdout_path: str = "",
    raw_stderr_path: str = "",
    runtime_ms: float | int | None = None,
    timeout_seconds: float | int | None = None,
    artifact_paths: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a contract-shaped synthetic verifier verdict record."""

    normalized = normalize_verdict(raw_verdict, invocation_status=invocation_status)
    record: dict[str, Any] = {
        "pair_id": pair_id,
        "tool": tool,
        "tool_version": tool_version,
        "invocation_status": invocation_status,
        "verdict": normalized,
        "raw_stdout_path": raw_stdout_path,
        "raw_stderr_path": raw_stderr_path,
        "runtime_ms": runtime_ms,
        "timeout_seconds": timeout_seconds,
        "normalized_verdict": normalized,
        "verdict_reason": verdict_reason(raw_verdict, normalized, invocation_status=invocation_status),
        "artifact_paths": dict(artifact_paths or {}),
        **boundary_flags_as_json(),
    }
    return validate_verdict_record(record)


def validate_verdict_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one ``verifier_verdicts.jsonl`` object."""

    missing = [field for field in VERDICT_FIELDS if field not in record]
    if missing:
        raise ValueError(f"verifier verdict record missing required fields: {', '.join(missing)}")
    normalized = dict(record)
    if not _stringify(normalized["pair_id"]):
        raise ValueError("verifier verdict record requires non-empty pair_id")
    if _stringify(normalized["tool"]) not in {"verieql", "sqlsolver"}:
        raise ValueError(f"unsupported verifier tool: {normalized['tool']}")
    if normalized["verdict"] not in ALLOWED_VERDICTS:
        raise ValueError(f"unsupported verifier verdict: {normalized['verdict']}")
    if normalized["normalized_verdict"] not in ALLOWED_VERDICTS:
        raise ValueError(f"unsupported normalized verifier verdict: {normalized['normalized_verdict']}")
    if normalized["verdict"] != normalized["normalized_verdict"]:
        raise ValueError("synthetic verifier verdict records must keep verdict and normalized_verdict aligned")
    if not isinstance(normalized["artifact_paths"], Mapping):
        raise ValueError("verifier verdict artifact_paths must be an object")
    _validate_json_boundary_flags(normalized)
    return normalized


def _validate_json_boundary_flags(record: Mapping[str, Any]) -> None:
    expected = boundary_flags_as_json()
    for key, value in expected.items():
        if record.get(key) is not value:
            raise ValueError(f"verifier verdict boundary flag {key} must be {str(value).lower()}")


def _canonical_text(value: Any) -> str:
    return _stringify(value).strip().lower().replace(" ", "_")


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
