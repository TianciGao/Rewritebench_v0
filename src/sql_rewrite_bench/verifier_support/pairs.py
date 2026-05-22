"""Verifier pair schema helpers for local diagnostic outputs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

BOUNDARY_FLAGS = {
    "local_diagnostic_only": True,
    "official_metric_input": False,
    "paper_result_input": False,
    "retained_evidence_promoted": False,
    "leaderboard_input": False,
}

PAIR_TYPES = {
    "source_vs_candidate",
    "source_vs_positive",
    "source_vs_hard_negative",
    "source_vs_candidate_port_target",
    "support_pair_smoke",
}

ALLOWED_TOOLS = {"verieql", "sqlsolver"}

PAIR_FIELDS = [
    "pair_id",
    "run_id",
    "tool",
    "case_id",
    "pool",
    "engine",
    "route_id",
    "method_id",
    "pair_type",
    "source_sql_path",
    "candidate_sql_path",
    "positive_sql_path",
    "negative_sql_path",
    "schema_context_path",
    "checker_context_path",
    "denominator_id",
    "local_diagnostic_only",
    "official_metric_input",
    "paper_result_input",
    "retained_evidence_promoted",
    "leaderboard_input",
]


def validate_pair_record(record: Mapping[str, Any]) -> dict[str, str]:
    """Validate and normalize one ``verifier_pairs.csv`` row.

    The validator intentionally enforces only the shared output contract. It
    does not inspect SQL text, infer PORT roles, or check verifier availability.
    """

    missing = [field for field in PAIR_FIELDS if field not in record]
    if missing:
        raise ValueError(f"verifier pair record missing required fields: {', '.join(missing)}")

    normalized = {field: _stringify(record.get(field)) for field in PAIR_FIELDS}
    if not normalized["pair_id"]:
        raise ValueError("verifier pair record requires non-empty pair_id")
    if not normalized["run_id"]:
        raise ValueError("verifier pair record requires non-empty run_id")
    if normalized["tool"] not in ALLOWED_TOOLS:
        raise ValueError(f"unsupported verifier tool: {normalized['tool']}")
    if normalized["pair_type"] not in PAIR_TYPES:
        raise ValueError(f"unsupported verifier pair_type: {normalized['pair_type']}")
    if not normalized["case_id"]:
        raise ValueError("verifier pair record requires non-empty case_id")
    if not normalized["source_sql_path"]:
        raise ValueError("verifier pair record requires source_sql_path")
    if normalized["pair_type"] in {"source_vs_candidate", "source_vs_candidate_port_target", "support_pair_smoke"}:
        if not normalized["candidate_sql_path"]:
            raise ValueError(f"{normalized['pair_type']} requires candidate_sql_path")
    if normalized["pair_type"] == "source_vs_positive" and not normalized["positive_sql_path"]:
        raise ValueError("source_vs_positive requires positive_sql_path")
    if normalized["pair_type"] == "source_vs_hard_negative" and not normalized["negative_sql_path"]:
        raise ValueError("source_vs_hard_negative requires negative_sql_path")

    _validate_boundary_flags(normalized)
    return normalized


def boundary_flags_as_csv() -> dict[str, str]:
    """Return boundary flags in CSV string form."""

    return {key: "true" if value else "false" for key, value in BOUNDARY_FLAGS.items()}


def boundary_flags_as_json() -> dict[str, bool]:
    """Return boundary flags in JSON boolean form."""

    return dict(BOUNDARY_FLAGS)


def _validate_boundary_flags(record: Mapping[str, Any]) -> None:
    for key, expected in BOUNDARY_FLAGS.items():
        actual = _parse_bool(record.get(key))
        if actual is not expected:
            raise ValueError(f"verifier pair boundary flag {key} must be {str(expected).lower()}")


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    text = _stringify(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
