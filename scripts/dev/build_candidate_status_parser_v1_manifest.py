#!/usr/bin/env python3
"""Build the approved input manifest for candidate_status_parser_v1.

The builder reads only release-repo approval artifacts and materializes the
five maintainer-approved non-timing parser inputs. It also records every other
proposal row as rejected, deferred, or reference-only so parser v1 cannot
silently expand its input surface.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_OUT_DIR = Path("audits/candidate_status_parser_v1")
APPROVED_PROPOSALS = {"P001", "P002", "P003", "P011", "P012"}
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
APPROVED_FIELDS_BY_PROPOSAL = {
    "P001": "generated|ready|failure_stage|failure_type|result_status|evidence_source",
    "P002": "generated|ready|executed|exact|result_status|failure_stage|failure_type|evidence_source",
    "P003": "failure_stage|failure_type|result_status|evidence_source",
    "P011": "result_status|failure_stage|failure_type|retained_artifact_path|evidence_source",
    "P012": "executed|exact|result_status|failure_stage|failure_type|checker_status|retained_artifact_path|evidence_source",
}

DECISION_SHEET = Path(
    "audits/candidate_status_whitelist_triage/candidate_status_manual_decision_sheet.csv"
)
MANIFEST_PREVIEW = Path(
    "audits/candidate_status_whitelist_triage/candidate_status_parser_v1_input_manifest_preview.csv"
)
PROPOSAL_FILE = Path("audits/candidate_status_whitelist_triage/candidate_status_whitelist_proposal.csv")

MANIFEST_FILENAME = "candidate_status_parser_v1_input_manifest.csv"
REJECTION_LOG_FILENAME = "candidate_status_parser_v1_input_rejection_log.csv"

MANIFEST_COLUMNS = [
    "manifest_id",
    "proposal_id",
    "source_repo",
    "source_path",
    "relative_path",
    "candidate_method",
    "expected_row_grain",
    "approved_fields",
    "disallowed_fields",
    "parser_mode",
    "approved_for_parser",
    "approval_status",
    "required_conditions",
    "source_file_type",
    "source_exists",
    "notes",
]

REJECTION_COLUMNS = [
    "proposal_id",
    "source_path",
    "rejection_reason",
    "future_action",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build candidate_status_parser_v1 approved input manifest."
    )
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def release_path(path: Path) -> Path:
    root = repo_root()
    resolved = path if path.is_absolute() else root / path
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"release approval artifact cannot be in legacy repo: {path}")
    return resolved


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def relative_path(source_path: str) -> str:
    if source_path.startswith("legacy:"):
        return source_path.removeprefix("legacy:")
    if str(LEGACY_REPO_ROOT) in source_path:
        return source_path.replace(str(LEGACY_REPO_ROOT) + "/", "")
    return source_path


def source_repo(source_path: str) -> str:
    if source_path.startswith("legacy:") or str(LEGACY_REPO_ROOT) in source_path:
        return "legacy_repo"
    return "release_repo"


def source_exists(source_path: str) -> bool:
    if source_repo(source_path) == "legacy_repo":
        return (LEGACY_REPO_ROOT / relative_path(source_path)).exists()
    return release_path(Path(relative_path(source_path))).exists()


def proposal_by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["proposal_id"]: row for row in rows if row.get("proposal_id")}


def preview_proposal_id(row: dict[str, str]) -> str:
    notes = row.get("notes", "")
    if "Approved from " not in notes:
        return ""
    tail = notes.split("Approved from ", 1)[1]
    return tail.split(" ", 1)[0].strip()


def build_manifest_rows(
    decisions: list[dict[str, str]],
    preview_rows: list[dict[str, str]],
    proposals: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    decision_by_id = {row["proposal_id"]: row for row in decisions if row.get("proposal_id")}
    rows: list[dict[str, str]] = []
    for preview in preview_rows:
        proposal_id = preview_proposal_id(preview)
        if proposal_id not in APPROVED_PROPOSALS:
            continue
        decision = decision_by_id.get(proposal_id, {})
        proposal = proposals.get(proposal_id, {})
        if decision.get("maintainer_decision") != "approved_for_candidate_status_parser_v1":
            raise ValueError(f"{proposal_id} is not approved in decision sheet")
        source_path = preview["source_path"]
        rows.append(
            {
                "manifest_id": preview["manifest_id"],
                "proposal_id": proposal_id,
                "source_repo": preview["source_repo"],
                "source_path": source_path,
                "relative_path": relative_path(source_path),
                "candidate_method": preview["candidate_method"],
                "expected_row_grain": preview["expected_row_grain"],
                "approved_fields": APPROVED_FIELDS_BY_PROPOSAL[proposal_id],
                "disallowed_fields": decision.get("rejected_fields") or preview.get("disallowed_fields", ""),
                "parser_mode": preview["parser_mode"],
                "approved_for_parser": "true",
                "approval_status": "approved_by_maintainer",
                "required_conditions": decision.get("required_conditions", ""),
                "source_file_type": proposal.get("file_type", "csv"),
                "source_exists": str(source_exists(source_path)).lower(),
                "notes": preview.get("notes", ""),
            }
        )
    found = {row["proposal_id"] for row in rows}
    if found != APPROVED_PROPOSALS:
        raise ValueError(f"approved proposal mismatch: found={sorted(found)}")
    return rows


def build_rejection_rows(
    decisions: list[dict[str, str]],
    proposals: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for decision in decisions:
        proposal_id = decision.get("proposal_id", "")
        if not proposal_id or proposal_id in APPROVED_PROPOSALS:
            continue
        proposal = proposals.get(proposal_id, {})
        maintainer_decision = decision.get("maintainer_decision") or decision.get("recommended_decision")
        if maintainer_decision == "defer_manual_review":
            future_action = "manual review before any parser use"
        elif maintainer_decision == "retain_reference_only":
            future_action = "retain as locator/reference metadata only"
        elif maintainer_decision == "not_approved_for_candidate_status_parser_v1":
            future_action = "requires separate maintainer approval before parser use"
        else:
            future_action = "do not use in candidate_status_parser_v1"
        rows.append(
            {
                "proposal_id": proposal_id,
                "source_path": proposal.get("source_path", ""),
                "rejection_reason": maintainer_decision,
                "future_action": future_action,
                "notes": decision.get("required_conditions") or decision.get("notes", ""),
            }
        )
    return rows


def main() -> int:
    args = parse_args()
    out_dir = release_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    decisions = read_csv(release_path(DECISION_SHEET))
    preview_rows = read_csv(release_path(MANIFEST_PREVIEW))
    proposals = proposal_by_id(read_csv(release_path(PROPOSAL_FILE)))

    manifest_rows = build_manifest_rows(decisions, preview_rows, proposals)
    rejection_rows = build_rejection_rows(decisions, proposals)

    write_csv(out_dir / MANIFEST_FILENAME, manifest_rows, MANIFEST_COLUMNS)
    write_csv(out_dir / REJECTION_LOG_FILENAME, rejection_rows, REJECTION_COLUMNS)

    print(f"approved_manifest_inputs: {len(manifest_rows)}")
    print(f"rejected_or_deferred_inputs: {len(rejection_rows)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
