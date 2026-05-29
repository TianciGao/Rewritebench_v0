"""Parser for root-level Common-core skills.md contracts.

This module is parse-only. It does not call APIs, inspect candidate SQL, infer
atoms from taxonomy/SQL files, or compute Positive Operation Coverage Rate.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from sql_rewrite_bench.pocr.models import SkillAtom, SkillContract, SkillParseResult, SkillValidationIssue
from sql_rewrite_bench.pocr.validation import validate_skill_contract

_SCOPE_FIELD_RE = re.compile(r"^-\s*(?P<key>case_id|pool)\s*:\s*`?(?P<value>[^`\s]+)`?\s*$")
_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")


def parse_skills_file(path: Path, *, expected_case_id: str | None = None, expected_pool: str | None = None) -> SkillParseResult:
    """Read a skills.md file as utf-8-sig and parse it."""

    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        issue = SkillValidationIssue(
            case_id=expected_case_id,
            pool=expected_pool,
            skills_path=path,
            code="read_failed",
            message=str(exc),
        )
        return SkillParseResult(contract=None, issues=(issue,))
    except UnicodeDecodeError as exc:
        issue = SkillValidationIssue(
            case_id=expected_case_id,
            pool=expected_pool,
            skills_path=path,
            code="utf8_sig_decode_failed",
            message=str(exc),
        )
        return SkillParseResult(contract=None, issues=(issue,))

    return parse_skills_text(
        text,
        skills_path=path,
        expected_case_id=expected_case_id,
        expected_pool=expected_pool,
    )


def parse_skills_text(
    text: str,
    *,
    skills_path: Path | None = None,
    expected_case_id: str | None = None,
    expected_pool: str | None = None,
) -> SkillParseResult:
    """Parse skills.md text into a structured contract plus validation issues."""

    case_id, pool = _parse_scope_fields(text.splitlines())
    atoms = tuple(_parse_atom_table(text.splitlines()))
    contract = SkillContract(
        skills_path=skills_path,
        case_id=case_id,
        pool=pool,
        atoms=atoms,
        has_atom_protocol=_has_heading(text, "Atom Protocol"),
        has_required_candidate_annotation_shape=_has_heading(text, "Required Candidate Annotation Shape"),
        has_review_boundaries=_has_heading(text, "Review Boundaries"),
        raw_text=text,
    )
    issues = tuple(
        validate_skill_contract(
            contract,
            expected_case_id=expected_case_id,
            expected_pool=expected_pool,
        )
    )
    return SkillParseResult(contract=contract, issues=issues)


def _parse_scope_fields(lines: Iterable[str]) -> tuple[str | None, str | None]:
    case_id: str | None = None
    pool: str | None = None
    for line in lines:
        match = _SCOPE_FIELD_RE.match(line.strip())
        if not match:
            continue
        key = match.group("key")
        value = match.group("value")
        if key == "case_id":
            case_id = value
        elif key == "pool":
            pool = value
    return case_id, pool


def _has_heading(text: str, title: str) -> bool:
    wanted = title.casefold()
    for line in text.splitlines():
        match = _HEADING_RE.match(line.strip())
        if match and match.group("title").strip().casefold() == wanted:
            return True
    return False


def _parse_atom_table(lines: list[str]) -> list[SkillAtom]:
    atom_heading_index = _find_heading(lines, "Atom Protocol")
    if atom_heading_index is None:
        return []

    end_index = len(lines)
    for index in range(atom_heading_index + 1, len(lines)):
        match = _HEADING_RE.match(lines[index].strip())
        if match and len(match.group("marks")) <= 2:
            end_index = index
            break

    section = lines[atom_heading_index + 1 : end_index]
    for relative_index, line in enumerate(section):
        if not _is_table_line(line):
            continue
        headers = _split_markdown_row(line)
        normalized_headers = [_normalize_header(header) for header in headers]
        if {"atom", "category", "type", "risk", "weight", "requirement"}.issubset(set(normalized_headers)):
            absolute_header_index = atom_heading_index + 1 + relative_index
            return _parse_table_rows(lines, absolute_header_index, normalized_headers)
    return []


def _find_heading(lines: list[str], title: str) -> int | None:
    wanted = title.casefold()
    for index, line in enumerate(lines):
        match = _HEADING_RE.match(line.strip())
        if match and match.group("title").strip().casefold() == wanted:
            return index
    return None


def _parse_table_rows(lines: list[str], header_index: int, headers: list[str]) -> list[SkillAtom]:
    separator_index = header_index + 1
    if separator_index >= len(lines) or not _is_separator_row(lines[separator_index]):
        return []

    atoms: list[SkillAtom] = []
    for row_index in range(separator_index + 1, len(lines)):
        line = lines[row_index]
        if not _is_table_line(line):
            break
        values = _split_markdown_row(line)
        if len(values) < len(headers):
            values = values + [""] * (len(headers) - len(values))
        raw_fields = dict(zip(headers, values, strict=False))
        category = _normalize_cell(raw_fields.get("category", ""))
        if category not in {"operation_atom", "semantic_guard_atom"}:
            normalized_category = "unknown"
        else:
            normalized_category = category
        weight_raw = _strip_code(raw_fields.get("weight", ""))
        atoms.append(
            SkillAtom(
                atom_id=_strip_code(raw_fields.get("atom", "")),
                category=normalized_category,  # type: ignore[arg-type]
                atom_type=_strip_code(raw_fields.get("type", "")),
                risk=_strip_code(raw_fields.get("risk", "")),
                weight_raw=weight_raw,
                weight=_parse_float(weight_raw),
                requirement=_strip_code(raw_fields.get("requirement", "")),
                source_row_number=row_index + 1,
                raw_fields={key: _strip_code(value) for key, value in raw_fields.items()},
            )
        )
    return atoms


def _is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def _is_separator_row(line: str) -> bool:
    if not _is_table_line(line):
        return False
    cells = _split_markdown_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def _split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _normalize_header(value: str) -> str:
    return _strip_code(value).strip().lower().replace(" ", "_")


def _normalize_cell(value: str) -> str:
    return _strip_code(value).strip().lower()


def _strip_code(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1].strip()
    return stripped


def _parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None
