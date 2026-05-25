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
        "LLM rationale is not evidence; keep rationale_short short and separate from evidence_refs.",
        "Do not use speedup, timing, runtime performance, taxonomy tags, or checker exactness as evidence for atom implementation.",
        "semantic_guard_atom is not an operation coverage numerator.",
        "Return strict JSON only. Do not include Markdown, prose, or code fences.",
        "",
        "Allowed observed_status values: implemented, not_implemented, contradicted, unclear, not_applicable.",
        "Allowed confidence values: high, medium, low.",
        "",
        "Evidence reference contract for evidence_refs:",
        "- Use only these supported static ref forms:",
        "  - candidate_sql_span:<literal substring>",
        "  - source_sql_span:<literal substring>",
        "  - positive_sql_span:<literal substring>",
        "  - candidate_token_span:<normalized tokens>",
        "  - source_candidate_diff:changed",
        "- The literal substring must appear exactly in the named SQL text, except candidate_token_span which may use normalized whitespace and case-insensitive tokens.",
        "- Do not cite vague phrases such as \"the query uses GROUP BY\" unless encoded as a supported static ref.",
        "- Unsupported refs such as candidate_sql:, llm_rationale:, taxonomy:, speedup:, timing:, prose-only descriptions, or file paths will be rejected by Stage B.",
        "- If no supported static ref exists for an atom, use an empty evidence_refs list and mark uncertain atoms as unclear.",
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
        '      "evidence_refs": ["candidate_sql_span:<literal substring>"],',
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
