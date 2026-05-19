from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from sql_rewrite_bench.case_package_v2_resolver import resolve_case_package_v2


class CasePackageV2ResolverTests(unittest.TestCase):
    def make_repo(self, manifest: str, include_witness: bool = True) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        case_dir = root / "cases" / "PERF" / "PERF_9999"
        for path in (
            case_dir / "sql",
            case_dir / "checker",
            case_dir / "validation",
            case_dir / "witness",
            root / "schemas" / "demo_schema" / "postgres",
            root / "schemas" / "demo_schema" / "mysql",
            root / "schemas" / "demo_schema" / "spark",
        ):
            path.mkdir(parents=True, exist_ok=True)
        for rel in (
            "sql/source.sql",
            "sql/pos_01.sql",
            "sql/neg_01.sql",
            "checker/checker.yaml",
            "checker/normalization.yaml",
            "checker/compare_config.yaml",
            "checker/expected_rejections.yaml",
            "validation/run_validation.sh",
            "validation/run_plan_collection.sh",
        ):
            (case_dir / rel).write_text("-- test\n", encoding="utf-8")
        for engine in ("postgres", "mysql", "spark"):
            (root / "schemas" / "demo_schema" / engine / "ddl.sql").write_text("-- ddl\n", encoding="utf-8")
            (root / "schemas" / "demo_schema" / engine / "load.sql").write_text("-- load\n", encoding="utf-8")
        if include_witness:
            (case_dir / "witness" / "data_profile.yaml").write_text("status: generated\n", encoding="utf-8")
            (case_dir / "witness" / "correct_result.csv").write_text("a\n1\n", encoding="utf-8")
        (case_dir / "README.md").write_text(
            textwrap.dedent(
                """\
                # PERF_9999

                ## Purpose
                Test.

                ## Release Scope
                Test.

                ## Package Contents
                Test.

                ## Evidence Boundary
                Test.

                ## Benchmark Boundary
                Test.

                ## Notes / Future Review Status
                Test.
                """
            ),
            encoding="utf-8",
        )
        (case_dir / "manifest.yaml").write_text(textwrap.dedent(manifest), encoding="utf-8")
        return tmp, root

    def valid_manifest(self) -> str:
        return """\
        case_id: PERF_9999
        pool: PERF
        case_package_standard: v2
        source_family: demo
        sql:
          source: sql/source.sql
          positives:
            - sql/pos_01.sql
          negatives:
            - sql/neg_01.sql
        schema_ref:
          schema_id: demo_schema
          engines:
            postgres:
              ddl: schemas/demo_schema/postgres/ddl.sql
              load: schemas/demo_schema/postgres/load.sql
            mysql:
              ddl: schemas/demo_schema/mysql/ddl.sql
              load: schemas/demo_schema/mysql/load.sql
            spark:
              ddl: schemas/demo_schema/spark/ddl.sql
              load: schemas/demo_schema/spark/load.sql
        checker:
          config: checker/checker.yaml
          normalization: checker/normalization.yaml
          compare_config: checker/compare_config.yaml
          expected_rejections: checker/expected_rejections.yaml
        witness:
          mode: source_as_oracle
          data_profile_status: generated
          correct_result_status: optional
          data_profile: witness/data_profile.yaml
          correct_result: witness/correct_result.csv
        validation:
          run_validation: validation/run_validation.sh
          run_plan_collection: validation/run_plan_collection.sh
        """

    def test_synthetic_v2_manifest_with_valid_schema_ref_passes(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            self.assertFalse(result.errors)

    def test_missing_schema_ref_path_fails(self) -> None:
        manifest = self.valid_manifest().replace(
            "schemas/demo_schema/postgres/ddl.sql",
            "schemas/demo_schema/postgres/missing.sql",
        )
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("schema_ref.engines.postgres.ddl" in error for error in result.errors))

    def test_missing_optional_witness_files_warns_only(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest(), include_witness=False)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            witness_refs = [ref for ref in result.references if ref.field.startswith("witness.")]
            self.assertTrue(any(ref.status == "warn" for ref in witness_refs))

    def test_absolute_paths_fail(self) -> None:
        manifest = self.valid_manifest().replace("sql/source.sql", "/tmp/source.sql")
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("absolute path" in error for error in result.errors))

    def test_perf0006_v2_ref_validation_runs_read_only(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = resolve_case_package_v2(
            repo_root=repo_root,
            case_path=Path("cases/PERF/PERF_0006"),
        )
        self.assertEqual(result.case_id, "PERF_0006")
        self.assertEqual(result.overall_status, "pass")
        self.assertTrue(result.findings)


if __name__ == "__main__":
    unittest.main()
