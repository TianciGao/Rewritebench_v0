import csv
import json
import shutil
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import resolve_common_core_selection
from sql_rewrite_bench.tag_slices import (
    TAG_SLICE_FIELDS,
    load_retained_tags,
    load_retained_tags_from_taxonomy,
)
from sql_rewrite_bench.user_run import run_user_benchmark


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _args(
    out: Path,
    case_list: Path,
    adapter: Path,
    *,
    dry_run: bool = False,
    smoke: bool = False,
) -> Namespace:
    return Namespace(
        case_set="common_core_v0",
        pool="all" if smoke else "PERF",
        engine="postgres",
        case_list=None if smoke else case_list,
        smoke=smoke,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=30,
        dry_run=dry_run,
        enable_db_execution=False,
        enable_checker=False,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


def _read_tag_slices(out_dir: Path) -> list[dict[str, str]]:
    with (out_dir / "tag_slices.csv").open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert reader.fieldnames == TAG_SLICE_FIELDS
    return rows


class TagSliceTests(unittest.TestCase):
    def test_tag_slices_are_written_for_dry_run_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u5_tags_dry_run")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(
                _args(out, case_list, adapter, dry_run=True, smoke=True),
                REPO_ROOT,
            )

        out_dir = REPO_ROOT / out
        rows = _read_tag_slices(out_dir)
        self.assertEqual(summary["selected_rows"], 2)
        self.assertGreaterEqual(len(rows), 4)
        self.assertIn(("sql_feature", "date_time_function"), _axis_tag_set(rows))
        self.assertIn(("rewrite_opportunity", "subquery_decorrelation"), _axis_tag_set(rows))
        for row in rows:
            self.assertEqual(row["local_diagnostic_only"], "true")
            self.assertEqual(row["official_metric"], "false")
            self.assertEqual(row["leaderboard_input"], "false")
            self.assertNotIn("score", row)
            self.assertNotIn("ranking", row)
        perf_feature = _find(rows, "sql_feature", "date_time_function")
        self.assertEqual(perf_feature["selected_rows"], "1")
        self.assertEqual(perf_feature["candidate_generated_rows"], "0")

    def test_tag_slices_are_written_for_adapter_capture_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u5_tags_adapter_capture")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter, smoke=True), REPO_ROOT)

        out_dir = REPO_ROOT / out
        rows = _read_tag_slices(out_dir)
        self.assertEqual(summary["candidate_generated_rows"], 2)
        perf_feature = _find(rows, "sql_feature", "date_time_function")
        self.assertEqual(perf_feature["candidate_generated_rows"], "1")
        self.assertEqual(perf_feature["candidate_preflight_passed_rows"], "1")
        self.assertEqual(perf_feature["source_like_rows"], "1")
        self.assertEqual(perf_feature["timed_rows"], "0")
        self.assertIn("not a score", perf_feature["claim_boundary"])
        self.assertFalse(any("speedup" in field for field in TAG_SLICE_FIELDS))
        self.assertFalse(any(field in TAG_SLICE_FIELDS for field in ["tag_score", "rank"]))
        quality = json.loads((out_dir / "quality_summary.json").read_text(encoding="utf-8"))
        self.assertIs(quality["interpretation_boundary"]["tag_slices_included"], True)
        report = (out_dir / "quality_report.md").read_text(encoding="utf-8")
        self.assertIn("Tag-aware slices are available as local diagnostics", report)

    def test_tag_loader_uses_manifest_taxonomy_not_sql_text(self) -> None:
        row = resolve_common_core_selection(
            repo_root=REPO_ROOT,
            case_set="common_core_v0",
            engine="postgres",
            smoke=True,
        )[0]
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        tags = {(tag.axis, tag.tag) for tag in load_retained_tags(resolved)}
        source_sql = resolved.source_sql_path.read_text(encoding="utf-8")
        self.assertIn(("sql_feature", "date_time_function"), tags)
        self.assertNotIn("date_time_function", source_sql)

    def test_taxonomy_loader_maps_only_supported_axes(self) -> None:
        tags = load_retained_tags_from_taxonomy(
            {
                "sql_feature": {"primary": ["cte"], "secondary": ["join"]},
                "rewrite_opportunity": {"primary": ["predicate_pushdown"]},
                "plan_operator": {"primary": ["hash_join"]},
                "workload_realism": {"primary": ["synthetic_boundary"]},
                "portability": {"confirmed": ["identifier_quoting"]},
                "consistency_focus": {"primary": ["null_semantics"]},
            }
        )
        axis_tags = {(tag.axis, tag.tag) for tag in tags}
        self.assertIn(("sql_feature", "cte"), axis_tags)
        self.assertIn(("plan_operator", "hash_join"), axis_tags)
        self.assertIn(("workload_realism", "synthetic_boundary"), axis_tags)
        self.assertIn(("portability_risk", "identifier_quoting"), axis_tags)
        self.assertNotIn(("consistency_focus", "null_semantics"), axis_tags)


def _axis_tag_set(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {(row["axis"], row["tag"]) for row in rows}


def _find(rows: list[dict[str, str]], axis: str, tag: str) -> dict[str, str]:
    for row in rows:
        if row["axis"] == axis and row["tag"] == tag:
            return row
    raise AssertionError(f"missing tag slice: {axis}/{tag}")


if __name__ == "__main__":
    unittest.main()
