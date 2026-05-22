"""Shared verifier-support helpers for local diagnostic outputs.

This package contains only common synthetic fixture, schema validation, verdict
normalization, and summary generation logic. It does not invoke VeriEQL,
SQLSolver, or any other verifier tool.
"""

from .fixtures import SyntheticVerifierFixture, write_synthetic_verifier_fixture
from .pairs import PAIR_FIELDS, PAIR_TYPES, validate_pair_record
from .summary import generate_semantic_equivalence_summary
from .verdicts import (
    ALLOWED_VERDICTS,
    DECIDABLE_VERDICTS,
    VERDICT_FIELDS,
    normalize_verdict,
    validate_verdict_record,
)

__all__ = [
    "ALLOWED_VERDICTS",
    "DECIDABLE_VERDICTS",
    "PAIR_FIELDS",
    "PAIR_TYPES",
    "SyntheticVerifierFixture",
    "VERDICT_FIELDS",
    "generate_semantic_equivalence_summary",
    "normalize_verdict",
    "validate_pair_record",
    "validate_verdict_record",
    "write_synthetic_verifier_fixture",
]
