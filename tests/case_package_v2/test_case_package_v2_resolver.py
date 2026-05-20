from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

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
        (case_dir / "validation" / "run_engine_queries.py").write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env python3
                from pathlib import Path

                from sql_rewrite_bench.validation.engine_query_runner import main


                if __name__ == "__main__":
                    raise SystemExit(main(default_case_dir=Path(__file__).resolve().parents[1]))
                """
            ),
            encoding="utf-8",
        )
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
            (case_dir / "witness" / "witness_profile.yaml").write_text("mode: source_as_oracle\n", encoding="utf-8")
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
        primary_pool: PERF
        package_path: cases/PERF/PERF_9999
        source_family: demo
        source_workload:
          source_name: demo
          source_id: SRC_DEMO
          source_seed: DEMO_QUERY
        based_benchmark: demo
        source_query_identity:
          source_id: SRC_DEMO
          source_name: demo
          source_seed: DEMO_QUERY
        source_path: datasets/raw/demo/query.sql
        draft_origin:
          recovery_method: synthetic_test_fixture
        taxonomy:
          sql_feature:
            primary: []
            secondary: []
          rewrite_opportunity:
            primary:
              - predicate_pushdown
            secondary: []
          portability:
            confirmed: []
            suspected: []
          performance_focus:
            primary:
              - synthetic_fixture
            secondary: []
        sql:
          source: sql/source.sql
          positive_rewrites:
            - id: pos_01
              path: sql/pos_01.sql
              status: recovered
          hard_negatives:
            - id: neg_01
              path: sql/neg_01.sql
              status: recovered
        schema:
          profile: schema/schema_profile.yaml
          external_profile: schemas/demo_schema/schema_profile.yaml
        witness:
          mode: source_as_oracle
          data_profile_status: external_or_generated
          correct_result_status: not_required_for_runtime_checker
          witness_profile: witness/witness_profile.yaml
          data_profile: witness/data_profile.yaml
          correct_result: witness/correct_result.csv
        checker:
          checker: checker/checker.yaml
          normalization: checker/normalization.yaml
          compare_config: checker/compare_config.yaml
          expected_rejections: checker/expected_rejections.yaml
        validation:
          run_validation: validation/run_validation.sh
          run_plan_collection: validation/run_plan_collection.sh
          run_engine_queries: validation/run_engine_queries.py
        evidence_policy:
          static_case_evidence: not_required
          regeneration_policy: regenerable_by_validation_and_report_scripts
          retained_static_artifacts: none
        status: repaired_v2_manifest_contract
        known_caveats: []
        artifact_warning:
          no_denominator_change: true
          no_paper_result_change: true
          no_official_metrics_computed: true
          no_db_checker_execution_run: true
          no_global_leaderboard_created: true
        """

    def test_synthetic_v2_manifest_with_valid_semantic_contract_passes(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            self.assertFalse(result.errors)

    def test_schema_external_profile_resolves_engine_paths(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            self.assertFalse(result.errors)
            resolved = {
                ref.field: ref
                for ref in result.references
                if ref.field in ("schema.external_profile", "schema.external_profile.engines.postgres.ddl")
            }
            self.assertEqual(resolved["schema.external_profile"].status, "pass")
            self.assertEqual(resolved["schema.external_profile.engines.postgres.ddl"].status, "pass")

    def test_evidence_policy_required_and_evidence_ref_absent(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
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

    def test_missing_evidence_policy_fails(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data.pop("evidence_policy")
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("evidence_policy" in error for error in result.errors))

    def test_missing_run_engine_queries_manifest_field_fails(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data["validation"].pop("run_engine_queries")
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("validation.run_engine_queries" in error for error in result.errors))

    def test_missing_run_engine_queries_file_fails(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            (root / "cases" / "PERF" / "PERF_9999" / "validation" / "run_engine_queries.py").unlink()
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("validation.run_engine_queries" in error for error in result.errors))

    def test_run_engine_queries_copied_implementation_marker_fails(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            (root / "cases" / "PERF" / "PERF_9999" / "validation" / "run_engine_queries.py").write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    from pathlib import Path
                    from sql_rewrite_bench.validation.engine_query_runner import main
                    import psycopg2

                    if __name__ == "__main__":
                        raise SystemExit(main(default_case_dir=Path(__file__).resolve().parents[1]))
                    """
                ),
                encoding="utf-8",
            )
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("validation.run_engine_queries.thin_shim" in error for error in result.errors))

    def test_static_validator_does_not_execute_run_engine_queries(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            (root / "cases" / "PERF" / "PERF_9999" / "validation" / "run_engine_queries.py").write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    from pathlib import Path
                    from sql_rewrite_bench.validation.engine_query_runner import main

                    if False:
                        raise RuntimeError("validator executed the shim")

                    if __name__ == "__main__":
                        raise SystemExit(main(default_case_dir=Path(__file__).resolve().parents[1]))
                    """
                ),
                encoding="utf-8",
            )
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass", result.errors)

    def test_evidence_ref_top_level_fails(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data["evidence_ref"] = {"path": "evidence/cases/PERF/PERF_9999"}
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("evidence_ref" in error or "evidence/cases" in error for error in result.errors))

    def test_schema_ref_engines_top_level_fails(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data["schema_ref"] = {
            "schema_id": "demo_schema",
            "engines": {
                "postgres": {
                    "ddl": "schemas/demo_schema/postgres/ddl.sql",
                    "load": "schemas/demo_schema/postgres/load.sql",
                }
            },
        }
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("schema_ref" in error for error in result.errors))

    def test_invalid_evidence_policy_value_fails(self) -> None:
        manifest = self.valid_manifest().replace("static_case_evidence: not_required", "static_case_evidence: required")
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("evidence_policy.static_case_evidence" in error for error in result.errors))

    def test_missing_engine_path_in_external_profile_fails(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
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
            self.assertTrue(any("schema.external_profile.engines.postgres.ddl" in error for error in result.errors))

    def test_missing_external_schema_profile_fails(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest())
        with tmp:
            (root / "schemas" / "demo_schema" / "schema_profile.yaml").unlink()
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("schema.external_profile" in error for error in result.errors))

    def test_missing_optional_witness_files_warns_only(self) -> None:
        tmp, root = self.make_repo(self.valid_manifest(), include_witness=False)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "pass")
            witness_refs = [ref for ref in result.references if ref.field.startswith("witness.")]
            self.assertTrue(any(ref.status == "warn" for ref in witness_refs))

    def test_missing_taxonomy_fails(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data.pop("taxonomy")
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("taxonomy" in error for error in result.errors))

    def test_malformed_sql_entries_fail(self) -> None:
        manifest_data = yaml.safe_load(textwrap.dedent(self.valid_manifest()))
        manifest_data["sql"]["positive_rewrites"] = ["sql/pos_01.sql"]
        manifest = yaml.safe_dump(manifest_data, sort_keys=False)
        tmp, root = self.make_repo(manifest)
        with tmp:
            result = resolve_case_package_v2(repo_root=root, case_path=Path("cases/PERF/PERF_9999"))
            self.assertEqual(result.overall_status, "fail")
            self.assertTrue(any("sql.positive_rewrites" in error for error in result.errors))

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
        self.assertFalse(result.errors)

    def test_five_pilot_cases_validate_semantic_manifest_contract(self) -> None:
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
                self.assertTrue(
                    any(ref.field == "schema.external_profile" and ref.status == "pass" for ref in result.references)
                )


if __name__ == "__main__":
    unittest.main()
