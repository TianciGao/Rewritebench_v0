"""Lightweight SQL text normalization for POCR transformation diagnostics."""

from __future__ import annotations

import re

_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"--[^\n\r]*")
_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|<>|!=|<=|>=|[<>=]+|[(),.*+-/]")


def normalize_sql_for_pocr_diff(sql_text: str) -> str:
    """Normalize SQL text for conservative source/candidate diff checks.

    This is not a parser and does not claim semantic equivalence. It strips
    simple comments, lowercases tokens, and normalizes whitespace only.
    """

    without_comments = strip_sql_comments_for_pocr(sql_text)
    return " ".join(_TOKEN_RE.findall(without_comments.lower()))


def strip_sql_comments_for_pocr(sql_text: str) -> str:
    """Strip simple SQL comments for diagnostic text-diff checks."""

    no_block = _BLOCK_COMMENT_RE.sub(" ", sql_text)
    return _LINE_COMMENT_RE.sub(" ", no_block)


def is_source_like_noop(source_sql: str, candidate_sql: str) -> bool:
    """Return true when source and candidate normalize to identical text."""

    return normalize_sql_for_pocr_diff(source_sql) == normalize_sql_for_pocr_diff(candidate_sql)


def span_present_in_candidate_but_absent_or_different_from_source(
    span: str,
    *,
    source_sql: str,
    candidate_sql: str,
) -> bool:
    """Check whether a cited candidate span is candidate-specific.

    The check is deliberately conservative: the span must be present in the
    candidate and absent from the normalized source text. If the source also
    contains the normalized span, the helper returns false rather than
    inferring that a transformation occurred.
    """

    normalized_span = normalize_sql_for_pocr_diff(span)
    if not normalized_span:
        return False
    candidate_normalized = normalize_sql_for_pocr_diff(candidate_sql)
    source_normalized = normalize_sql_for_pocr_diff(source_sql)
    return normalized_span in candidate_normalized and normalized_span not in source_normalized


def candidate_aligns_with_positive_span(
    span: str,
    *,
    candidate_sql: str,
    positive_sql: str | None,
) -> bool:
    """Check whether a span appears in both candidate and positive-control SQL."""

    if positive_sql is None:
        return False
    normalized_span = normalize_sql_for_pocr_diff(span)
    if not normalized_span:
        return False
    return (
        normalized_span in normalize_sql_for_pocr_diff(candidate_sql)
        and normalized_span in normalize_sql_for_pocr_diff(positive_sql)
    )


def source_candidate_changed(source_sql: str, candidate_sql: str) -> bool:
    """Return true when the normalized source and candidate texts differ."""

    return not is_source_like_noop(source_sql, candidate_sql)
