"""Semantic equivalence summary generation for verifier support outputs."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

from .pairs import boundary_flags_as_json
from .verdicts import ALLOWED_VERDICTS, validate_verdict_record


def generate_semantic_equivalence_summary(
    *,
    run_id: str,
    verdict_rows: Iterable[Mapping[str, Any]],
    verifier_tools_requested: Iterable[str] | None = None,
    pairs_planned: int | None = None,
    result_consistent_pairs: int | None = None,
) -> dict[str, Any]:
    """Generate ``semantic_equivalence_summary.json`` payload.

    This computes only a synthetic/local summary from verifier verdict rows. It
    does not use local result-checker exactness as verifier evidence.
    """

    validated = [validate_verdict_record(row) for row in verdict_rows]
    counts = Counter(row["normalized_verdict"] for row in validated)
    for verdict in ALLOWED_VERDICTS:
        counts.setdefault(verdict, 0)
    equivalent_count = counts["equivalent"]
    non_equivalent_count = counts["non_equivalent"]
    decidable_count = equivalent_count + non_equivalent_count
    attempted_count = len(validated) - counts["not_attempted"]
    requested = sorted(set(verifier_tools_requested or [row["tool"] for row in validated]))
    completed = sorted(
        {
            row["tool"]
            for row in validated
            if row["normalized_verdict"] != "not_attempted" and row.get("invocation_status") != "not_attempted"
        }
    )
    if decidable_count:
        semantic_equivalence_rate: float | None = equivalent_count / decidable_count
        na_reason = None
    else:
        semantic_equivalence_rate = None
        na_reason = "no_decidable_verifier_outcomes"
    if result_consistent_pairs and result_consistent_pairs > 0:
        verifier_decidability_rate: float | None = decidable_count / result_consistent_pairs
    else:
        verifier_decidability_rate = None
    summary = {
        "schema_version": "semantic_equivalence_summary_v0",
        "run_id": run_id,
        "verifier_tools_requested": requested,
        "verifier_tools_completed": completed,
        "pairs_planned": pairs_planned if pairs_planned is not None else len(validated),
        "pairs_attempted": attempted_count,
        "equivalent_count": equivalent_count,
        "non_equivalent_count": non_equivalent_count,
        "unknown_count": counts["unknown"],
        "timeout_count": counts["timeout"],
        "unsupported_count": counts["unsupported"],
        "syntax_error_count": counts["syntax_error"],
        "not_implemented_count": counts["not_implemented"],
        "out_of_memory_count": counts["out_of_memory"],
        "tool_error_count": counts["tool_error"],
        "not_attempted_count": counts["not_attempted"],
        "decidable_count": decidable_count,
        "semantic_equivalence_rate": semantic_equivalence_rate,
        "verifier_decidability_rate": verifier_decidability_rate,
        "na_reason": na_reason,
        "semantic_equivalence_rate_status": "computed" if semantic_equivalence_rate is not None else "not_applicable",
        "semantic_equivalence_source": "formal_verifier_evidence",
        "result_checker_exactness_used": False,
        **boundary_flags_as_json(),
    }
    return summary
