from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "examples" / "user" / "port_mysql_target_reference_adapter.py"


def _run_adapter(
    case_dir: Path,
    workspace: Path,
    *,
    engine: str = "mysql",
) -> subprocess.CompletedProcess[str]:
    candidate = workspace / "candidate.sql"
    env = os.environ.copy()
    env.update(
        {
            "SQLRB_CASE_DIR": str(case_dir),
            "SQLRB_WORKSPACE_DIR": str(workspace),
            "SQLRB_CANDIDATE_SQL_PATH": str(candidate),
            "SQLRB_ENGINE": engine,
        }
    )
    return subprocess.run(
        [sys.executable, str(ADAPTER)],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class PortMySQLTargetReferenceAdapterTest(unittest.TestCase):
    def test_copies_manifest_declared_mysql_target_reference_for_real_port_case(self) -> None:
        case_dir = REPO_ROOT / "cases" / "PORT" / "PORT_0003"
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            workspace.mkdir()
            completed = _run_adapter(case_dir, workspace)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                (workspace / "candidate.sql").read_text(encoding="utf-8"),
                (case_dir / "sql" / "pos_01.sql").read_text(encoding="utf-8"),
            )

    def test_fails_closed_when_selected_engine_is_not_mysql(self) -> None:
        case_dir = REPO_ROOT / "cases" / "PORT" / "PORT_0003"
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            workspace.mkdir()
            completed = _run_adapter(case_dir, workspace, engine="postgres")

            self.assertEqual(completed.returncode, 2)
            self.assertIn("SQLRB_ENGINE", completed.stderr)
            self.assertFalse((workspace / "candidate.sql").exists())

    def test_uses_declared_query_path_instead_of_guessing_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = Path(temp_dir) / "case"
            target_dir = case_dir / "sql" / "mysql_refs"
            target_dir.mkdir(parents=True)
            (target_dir / "declared_mysql_target.sql").write_text(
                "select 1 as ok;\n",
                encoding="utf-8",
            )
            (case_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "local_diagnostic:",
                        "  schema_version: port_target_engine_diagnostic_v0",
                        "  engine_roles:",
                        "    mysql:",
                        "      diagnostic_mode: cross_dialect_reference",
                        "      target_candidate:",
                        "        role: adapter_output",
                        "        engine: mysql",
                        "      target_reference:",
                        "        role: positive_reference",
                        "        engine: mysql",
                        "        query: sql/mysql_refs/declared_mysql_target.sql",
                        "        use_for_checker_oracle: false",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            workspace = Path(temp_dir) / "workspace"
            workspace.mkdir()

            completed = _run_adapter(case_dir, workspace)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                (workspace / "candidate.sql").read_text(encoding="utf-8"),
                "select 1 as ok;\n",
            )

    def test_fails_closed_when_target_reference_can_be_checker_oracle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_dir = Path(temp_dir) / "case"
            sql_dir = case_dir / "sql"
            sql_dir.mkdir(parents=True)
            (sql_dir / "target.sql").write_text("select 1;\n", encoding="utf-8")
            (case_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "local_diagnostic:",
                        "  schema_version: port_target_engine_diagnostic_v0",
                        "  engine_roles:",
                        "    mysql:",
                        "      diagnostic_mode: cross_dialect_reference",
                        "      target_candidate:",
                        "        role: adapter_output",
                        "        engine: mysql",
                        "      target_reference:",
                        "        role: positive_reference",
                        "        engine: mysql",
                        "        query: sql/target.sql",
                        "        use_for_checker_oracle: true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            workspace = Path(temp_dir) / "workspace"
            workspace.mkdir()

            completed = _run_adapter(case_dir, workspace)

            self.assertEqual(completed.returncode, 2)
            self.assertIn("use_for_checker_oracle", completed.stderr)
            self.assertFalse((workspace / "candidate.sql").exists())


if __name__ == "__main__":
    unittest.main()
