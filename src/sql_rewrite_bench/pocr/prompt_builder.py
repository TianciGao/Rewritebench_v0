"""Deterministic Stage A annotation prompt builder."""

from __future__ import annotations

from dataclasses import dataclass

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION
from sql_rewrite_bench.pocr.models import SkillContract


@dataclass(frozen=True)
class AnnotationPromptInputs:
    """Inputs needed to build one candidate-level annotation prompt."""

    contract: SkillContract
    source_sql: str
    candidate_sql: str
    engine: str
    method_id: str
    route_id: str
    candidate_id: str | None = None
    candidate_path: str | None = None
    positive_sql: str | None = None
    negative_sql: str | None = None


def build_annotation_prompt(inputs: AnnotationPromptInputs) -> str:
    """Build a deterministic prompt for strict JSON Stage A annotation."""

    if not inputs.contract.case_id or not inputs.contract.pool:
        raise ValueError("SkillContract must include case_id and pool")
    if not inputs.contract.atoms:
        raise ValueError("SkillContract must include Atom Protocol atoms")
    if not (inputs.candidate_id or inputs.candidate_path):
        raise ValueError("candidate_id or candidate_path is required")

    atom_lines = []
    for atom in inputs.contract.atoms:
        atom_lines.append(
            "\n".join(
                [
                    f"- atom_id: {atom.atom_id}",
                    f"  atom_type: {atom.category}",
                    f"  type: {atom.atom_type}",
                    f"  requirement: {atom.requirement}",
                ]
            )
        )

    parts = [
        "You are annotating one SQL rewrite candidate for a parse-only POCR Stage A fixture.",
        "Judge only the atoms explicitly defined in the case-local skills.md Atom Protocol.",
        "Do not invent atoms, rename atoms, merge atoms, split atoms, or infer atoms from taxonomy, SQL text, runtime, speedup, or retained evidence.",
        "Separate operation_atom and semantic_guard_atom exactly as provided.",
        "If the candidate is uncertain for an atom, mark observed_status as unclear rather than guessing.",
        "Do not use speedup, timing, or runtime performance as evidence for atom implementation.",
        "Return strict JSON only. Do not include Markdown, prose, or code fences.",
        "",
        "Allowed observed_status values: implemented, not_implemented, contradicted, unclear, not_applicable.",
        "Allowed confidence values: high, medium, low.",
        "",
        "Required JSON shape:",
        "{",
        '  "case_id": "...",',
        '  "pool": "...",',
        '  "engine": "...",',
        '  "method_id": "...",',
        '  "route_id": "...",',
        '  "candidate_id": "..." OR "candidate_path": "...",',
        f'  "annotation_schema_version": "{ANNOTATION_SCHEMA_VERSION}",',
        '  "atoms": [',
        "    {",
        '      "atom_id": "...",',
        '      "atom_type": "operation_atom | semantic_guard_atom",',
        '      "expected": true,',
        '      "observed_status": "implemented | not_implemented | contradicted | unclear | not_applicable",',
        '      "rationale_short": "...",',
        '      "evidence_refs": [],',
        '      "confidence": "high | medium | low"',
        "    }",
        "  ]",
        "}",
        "",
        "Row metadata:",
        f"- case_id: {inputs.contract.case_id}",
        f"- pool: {inputs.contract.pool}",
        f"- engine: {inputs.engine}",
        f"- method_id: {inputs.method_id}",
        f"- route_id: {inputs.route_id}",
        f"- candidate_id: {inputs.candidate_id or ''}",
        f"- candidate_path: {inputs.candidate_path or ''}",
        "",
        "Atoms from skills.md:",
        "\n".join(atom_lines),
        "",
        "Source SQL:",
        _fenced_sql(inputs.source_sql),
        "",
        "Candidate SQL:",
        _fenced_sql(inputs.candidate_sql),
    ]
    if inputs.positive_sql is not None:
        parts.extend(["", "Optional positive SQL context:", _fenced_sql(inputs.positive_sql)])
    if inputs.negative_sql is not None:
        parts.extend(["", "Optional negative SQL context:", _fenced_sql(inputs.negative_sql)])
    return "\n".join(parts)


def _fenced_sql(sql: str) -> str:
    return "```sql\n" + sql.strip() + "\n```"
