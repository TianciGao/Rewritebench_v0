"""Text-level candidate SQL preflight for local user-entry diagnostics."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .user_run_schema import (
    CANDIDATE_PARSE_STATUS_NOT_CHECKED,
    CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE,
    CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
    CANDIDATE_PREFLIGHT_FAILURE_NONE,
    CANDIDATE_PREFLIGHT_FAILURE_PREFLIGHT_ERROR,
    CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL,
    CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE,
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
    CANDIDATE_SAFETY_STATUS_SAFE,
    CANDIDATE_SAFETY_STATUS_UNSAFE,
    SOURCE_LIKE_STATUS_CHANGED,
    SOURCE_LIKE_STATUS_NOT_CHECKED,
    SOURCE_LIKE_STATUS_SOURCE_LIKE,
)


QUERY_KEYWORDS = {"SELECT", "WITH"}
UNSAFE_KEYWORDS = {
    "ALTER",
    "CALL",
    "COPY",
    "CREATE",
    "DELETE",
    "DROP",
    "EXEC",
    "GRANT",
    "INSERT",
    "MERGE",
    "REVOKE",
    "TRUNCATE",
    "UPDATE",
}


@dataclass(frozen=True)
class CandidatePreflightResult:
    """Candidate readiness result before optional DB/checker diagnostics."""

    candidate_preflight_status: str
    candidate_preflight_passed: str
    candidate_preflight_failure_class: str
    candidate_safety_status: str
    candidate_parse_status: str
    source_like_status: str
    notes: str


def preflight_error_result(message: str) -> CandidatePreflightResult:
    """Return a fail-closed result for unexpected preflight errors."""

    return CandidatePreflightResult(
        candidate_preflight_status=CANDIDATE_PREFLIGHT_STATUS_FAILED,
        candidate_preflight_passed="false",
        candidate_preflight_failure_class=CANDIDATE_PREFLIGHT_FAILURE_PREFLIGHT_ERROR,
        candidate_safety_status=CANDIDATE_SAFETY_STATUS_UNSAFE,
        candidate_parse_status=CANDIDATE_PARSE_STATUS_NOT_CHECKED,
        source_like_status=SOURCE_LIKE_STATUS_NOT_CHECKED,
        notes=f"candidate preflight error: {message}",
    )


def run_candidate_preflight(
    *,
    source_sql_text: str,
    candidate_sql_text: str,
    dialect: str | None = None,
) -> CandidatePreflightResult:
    """Run conservative text-level SQL readiness checks.

    This is not SQL semantic-equivalence checking, execution, checker logic, or
    a formal SQL security verifier. It only gates obvious non-query or unsafe
    candidate text before optional local DB execution.
    """

    del dialect  # Reserved for future parser/dialect-aware checks.

    stripped_candidate = candidate_sql_text.strip()
    if not stripped_candidate:
        return _failed(
            CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE,
            CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
            "candidate SQL is empty or whitespace-only",
        )

    if _has_multiple_statements(candidate_sql_text):
        return _failed(
            CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
            CANDIDATE_SAFETY_STATUS_UNSAFE,
            "candidate SQL appears to contain multiple statements",
        )

    first_keyword = _first_statement_keyword(candidate_sql_text)
    if first_keyword in UNSAFE_KEYWORDS:
        return _failed(
            CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL,
            CANDIDATE_SAFETY_STATUS_UNSAFE,
            f"candidate SQL begins with unsafe statement type {first_keyword}",
        )
    if first_keyword not in QUERY_KEYWORDS:
        return _failed(
            CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE,
            CANDIDATE_SAFETY_STATUS_UNSAFE,
            "candidate SQL is not a SELECT or WITH query",
        )

    return CandidatePreflightResult(
        candidate_preflight_status=CANDIDATE_PREFLIGHT_STATUS_PASSED,
        candidate_preflight_passed="true",
        candidate_preflight_failure_class=CANDIDATE_PREFLIGHT_FAILURE_NONE,
        candidate_safety_status=CANDIDATE_SAFETY_STATUS_SAFE,
        candidate_parse_status=CANDIDATE_PARSE_STATUS_NOT_CHECKED,
        source_like_status=_source_like_status(source_sql_text, candidate_sql_text),
        notes="candidate preflight passed; parse status not checked",
    )


def _failed(
    failure_class: str,
    safety_status: str,
    notes: str,
) -> CandidatePreflightResult:
    return CandidatePreflightResult(
        candidate_preflight_status=CANDIDATE_PREFLIGHT_STATUS_FAILED,
        candidate_preflight_passed="false",
        candidate_preflight_failure_class=failure_class,
        candidate_safety_status=safety_status,
        candidate_parse_status=CANDIDATE_PARSE_STATUS_NOT_CHECKED,
        source_like_status=SOURCE_LIKE_STATUS_NOT_CHECKED,
        notes=notes,
    )


def _first_statement_keyword(sql: str) -> str:
    text = _strip_leading_comments(sql)
    match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)", text)
    return match.group(1).upper() if match else ""


def _has_multiple_statements(sql: str) -> bool:
    for semicolon_index in _semicolon_positions(sql):
        remainder = _strip_leading_comments(sql[semicolon_index + 1 :]).strip()
        if remainder:
            return True
    return False


def _semicolon_positions(sql: str) -> list[int]:
    positions: list[int] = []
    quote: str | None = None
    line_comment = False
    block_comment = False
    index = 0
    while index < len(sql):
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < len(sql) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote is not None:
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue

        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if char == ";":
            positions.append(index)
        index += 1
    return positions


def _strip_leading_comments(sql: str) -> str:
    text = sql.lstrip()
    while True:
        if text.startswith("--"):
            newline = text.find("\n")
            if newline == -1:
                return ""
            text = text[newline + 1 :].lstrip()
            continue
        if text.startswith("/*"):
            end = text.find("*/")
            if end == -1:
                return ""
            text = text[end + 2 :].lstrip()
            continue
        return text


def _source_like_status(source_sql_text: str, candidate_sql_text: str) -> str:
    if _normalize_for_source_like(source_sql_text) == _normalize_for_source_like(
        candidate_sql_text
    ):
        return SOURCE_LIKE_STATUS_SOURCE_LIKE
    return SOURCE_LIKE_STATUS_CHANGED


def _normalize_for_source_like(sql: str) -> str:
    text = sql.strip()
    if text.endswith(";"):
        text = text[:-1].strip()
    return " ".join(text.split())
