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
            case_dir / "schema",
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
        (root / "schemas" / "demo_schema" / "schema_profile.yaml").write_text(
            textwrap.dedent(
                """\
                schema_id: demo_schema
                source_family: demo
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
                """
            ),
            encoding="utf-8",
        )
        (case_dir / "schema" / "schema_profile.yaml").write_text(
            textwrap.dedent(
                """\
                schema_id: demo_schema
                external_schema_profile: schemas/demo_schema/schema_profile.yaml
                source_family: demo
                relevant_tables: []
                columns: {}
                column_types: {}
                primary_keys: {}
                foreign_keys: {}
                dialect_differences: {}
                engine_support: {}
                fixture_notes: synthetic fixture
                """
            ),
            encoding="utf-8",
        )
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

    def profile_first_manifest(self) -> str:
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
          profile: schemas/demo_schema/schema_profile.yaml
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

    def test_profile_first_schema_ref_resolves_through_external_profile_passes(self) -> None:
        tmp, root = self.make_repo(self.profile_first_manifest())
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            self.assertFalse(result.errors)
            resolved = {
                ref.field: ref
                for ref in result.references
                if ref.field in ("schema_ref.profile", "schema_ref.engines.postgres.ddl")
            }
            self.assertEqual(resolved["schema_ref.profile"].status, "pass")
            self.assertEqual(resolved["schema_ref.engines.postgres.ddl"].status, "pass")

    def test_evidence_policy_not_required_passes_without_evidence_ref(self) -> None:
        manifest = (
            self.profile_first_manifest()
            + """
        evidence_policy:
          static_case_evidence: not_required
          regeneration_policy: regenerable_by_validation_and_report_scripts
          retained_static_artifacts: none
        """
        )
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            self.assertFalse(result.errors)
            self.assertTrue(
                any(
                    check.field == "evidence_policy.static_case_evidence"
                    and check.status == "pass"
                    for check in result.internal_checks
                )
            )

    def test_invalid_evidence_policy_value_fails(self) -> None:
        manifest = (
            self.profile_first_manifest()
            + """
        evidence_policy:
          static_case_evidence: required_static_paths
          regeneration_policy: unavailable
          retained_static_artifacts: none
        """
        )
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("evidence_policy.static_case_evidence" in error for error in result.errors))

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

    def test_missing_external_schema_profile_fails(self) -> None:
        tmp, root = self.make_repo(self.profile_first_manifest())
        with tmp:
            (root / "schemas" / "demo_schema" / "schema_profile.yaml").unlink()
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("schema_ref.profile" in error for error in result.errors))

    def test_missing_engine_path_in_external_profile_fails(self) -> None:
        tmp, root = self.make_repo(self.profile_first_manifest())
        with tmp:
            (root / "schemas" / "demo_schema" / "schema_profile.yaml").write_text(
                textwrap.dedent(
                    """\
                    schema_id: demo_schema
                    engines:
                      postgres:
                        ddl: schemas/demo_schema/postgres/missing.sql
                        load: schemas/demo_schema/postgres/load.sql
                      mysql:
                        ddl: schemas/demo_schema/mysql/ddl.sql
                        load: schemas/demo_schema/mysql/load.sql
                      spark:
                        ddl: schemas/demo_schema/spark/ddl.sql
                        load: schemas/demo_schema/spark/load.sql
                    """
                ),
                encoding="utf-8",
            )
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("schema_ref.engines.postgres.ddl" in error for error in result.errors))

    def test_missing_optional_witness_files_warns_only(self) -> None:
        tmp, root = self.make_repo(self.profile_first_manifest(), include_witness=False)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            witness_refs = [ref for ref in result.references if ref.field.startswith("witness.")]
            self.assertTrue(any(ref.status == "warn" for ref in witness_refs))

    def test_absolute_paths_fail(self) -> None:
        manifest = self.profile_first_manifest().replace("sql/source.sql", "/tmp/source.sql")
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
        self.assertFalse(result.errors)

    def test_five_pilot_cases_validate_profile_first_schema_ref(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        for case_path in (
            "cases/PERF/PERF_0006",
            "cases/PERF/PERF_0007",
            "cases/CONS/CONS_0005",
            "cases/PORT/PORT_0003",
            "cases/LONGTAIL/LONGTAIL_0011",
        ):
            with self.subTest(case_path=case_path):
                result = resolve_case_package_v2(repo_root=repo_root, case_path=Path(case_path))
                self.assertEqual(result.overall_status, "pass", result.errors)
                self.assertFalse(result.errors)
                self.assertTrue(any(ref.field == "schema_ref.profile" and ref.status == "pass" for ref in result.references))


if __name__ == "__main__":
    unittest.main()
