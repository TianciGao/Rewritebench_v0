import json
from pathlib import Path


CASE_ID = "PORT_0004"
CASE_DIR = Path(__file__).resolve().parent.parent
RUN_DIR = CASE_DIR / "runs"
PLAN_CHECK_PATH = RUN_DIR / "plan_check.json"
EXPECTED_PLAN_FILES = [
    "runs/mysql/plans/source.json",
    "runs/pg/plans/rewrite_pos_01.json",
    "runs/pg/plans/rewrite_neg_01.json",
    "runs/spark/plans/rewrite_pos_02_spark.txt",
    "runs/spark/plans/rewrite_neg_02_spark.txt",
]


def main() -> int:
    existing_plan_files = []
    missing_plan_files = []

    for relative_path in EXPECTED_PLAN_FILES:
        file_path = CASE_DIR / relative_path
        if file_path.is_file():
            existing_plan_files.append(relative_path)
        else:
            missing_plan_files.append(relative_path)

    payload = {
        "case_id": CASE_ID,
        "status": "complete" if not missing_plan_files else "incomplete",
        "draft_only": True,
        "expected_plan_files": EXPECTED_PLAN_FILES,
        "existing_plan_files": existing_plan_files,
        "missing_plan_files": missing_plan_files,
        "notes": [
            "Plan-artifact presence checking only.",
            "No plan semantics review is claimed.",
            "No admission, formal review completion, or release-grade claim is implied.",
        ],
    }
    PLAN_CHECK_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if not missing_plan_files else 1

if __name__ == "__main__":
    raise SystemExit(main())
