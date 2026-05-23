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
from .sqlsolver import (
    SQLSolverAvailability,
    SQLSolverSmokeOutput,
    detect_sqlsolver,
    normalize_sqlsolver_output,
    write_sqlsolver_smoke,
)
from .verieql import (
    VeriEQLAvailability,
    VeriEQLCanaryOutput,
    detect_verieql,
    normalize_verieql_output,
    write_verieql_canary,
)

__all__ = [
    "ALLOWED_VERDICTS",
    "DECIDABLE_VERDICTS",
    "PAIR_FIELDS",
    "PAIR_TYPES",
    "SQLSolverAvailability",
    "SQLSolverSmokeOutput",
    "SyntheticVerifierFixture",
    "VeriEQLAvailability",
    "VeriEQLCanaryOutput",
    "VERDICT_FIELDS",
    "detect_sqlsolver",
    "detect_verieql",
    "generate_semantic_equivalence_summary",
    "normalize_sqlsolver_output",
    "normalize_verdict",
    "normalize_verieql_output",
    "validate_pair_record",
    "validate_verdict_record",
    "write_sqlsolver_smoke",
    "write_verieql_canary",
    "write_synthetic_verifier_fixture",
]
