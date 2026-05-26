import csv
import json
from json import JSONDecodeError
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_client import AnnotationCallResult
from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.checkpointed_annotation_runner import (
    CheckpointedAnnotationConfig,
    output_paths,
    run_checkpointed_annotation,
)
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file


REPO_ROOT = Path(__file__).resolve().parents[2]
METHOD_ID = "direct_llm_repair_1"
ROUTE_ID = "direct_llm_repair_1_pg40_pocr_diagnostic"


class SequenceProvider:
    def __init__(self, *items: object):
        self.items = list(items)
        self.calls = 0

    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult:
        assert prompt.strip()
        self.calls += 1
        item = self.items.pop(0)
        if isinstance(item, BaseException):
            raise item
        return AnnotationCallResult(
            annotation=item,  # type: ignore[arg-type]
            provider_label="fake",
            model_label="fixture",
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
        )


class PendingInspectingProvider:
    def __init__(self, manifest_path: Path, annotation: object):
        self.manifest_path = manifest_path
        self.annotation = annotation
        self.saw_pending = False

    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult:
        rows = _read_csv(self.manifest_path)
        assert rows[0]["call_status"] == "pending"
        assert rows[0]["annotation_status"] == "pending"
        self.saw_pending = True
        return AnnotationCallResult(
            annotation=self.annotation,  # type: ignore[arg-type]
            provider_label="fake",
            model_label="fixture",
            prompt_tokens=1,
            completion_tokens=1,
            total_tokens=2,
        )


class ExplodingProvider:
    calls = 0

    def annotate_with_metadata(self, prompt: str) -> AnnotationCallResult:
        self.calls += 1
        raise AssertionError("provider should not be called")


def _case_pool(case_id: str) -> str:
    inventory = build_common_core_inventory(REPO_ROOT)
    return next(member.pool for member in inventory.members if member.case_id == case_id)


def _skills_path(case_id: str) -> Path:
    inventory = build_common_core_inventory(REPO_ROOT)
    return REPO_ROOT / next(member.skills_path for member in inventory.members if member.case_id == case_id)


def _valid_annotation(case_id: str):
    pool = _case_pool(case_id)
    result = parse_skills_file(_skills_path(case_id), expected_case_id=case_id, expected_pool=pool)
    assert result.contract is not None
    return annotation_from_mapping(
        {
            "case_id": case_id,
            "pool": pool,
            "engine": "postgres",
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "candidate_id": "fixture-candidate",
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "atoms": [
                {
                    "atom_id": atom.atom_id,
                    "atom_type": atom.category,
                    "expected": True,
                    "observed_status": "unclear",
                    "rationale_short": "fixture annotation",
                    "evidence_refs": [],
                    "confidence": "low",
                }
                for atom in result.contract.atoms
            ],
        }
    )


def _invalid_annotation(case_id: str):
    pool = _case_pool(case_id)
    return annotation_from_mapping(
        {
            "case_id": case_id,
            "pool": pool,
            "engine": "postgres",
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "candidate_id": "fixture-candidate",
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "atoms": [],
        }
    )


def _candidate_root(tmp_path: Path, case_ids: tuple[str, ...]) -> Path:
    root = tmp_path / "candidate_sql"
    root.mkdir(parents=True, exist_ok=True)
    for case_id in case_ids:
        (root / f"{case_id}__postgres.sql").write_text(f"select '{case_id}' as case_id;\n", encoding="utf-8")
    return root


def _config(tmp_path: Path, case_ids: tuple[str, ...] = ("PERF_0006",), **overrides: object) -> CheckpointedAnnotationConfig:
    values = {
        "repo_root": REPO_ROOT,
        "output_root": tmp_path / "output",
        "candidate_root": _candidate_root(tmp_path, case_ids),
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "engine": "postgres",
        "case_ids": case_ids,
        "live_enabled": True,
        "max_live_calls": len(case_ids),
        "provider_label": "fake",
        "model_label": "fixture",
        "api_key_env_name": "SQLRB_LLM_API_KEY",
    }
    values.update(overrides)
    return CheckpointedAnnotationConfig(**values)  # type: ignore[arg-type]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _all_output_text(root: Path) -> str:
    chunks: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def test_manifest_row_is_pending_before_provider_call(tmp_path: Path) -> None:
    config = _config(tmp_path)
    paths = output_paths(config)
    provider = PendingInspectingProvider(paths.annotation_manifest_csv, _valid_annotation("PERF_0006"))

    run_checkpointed_annotation(config, client=provider)

    assert provider.saw_pending is True
    rows = _read_csv(paths.annotation_manifest_csv)
    assert rows[0]["annotation_status"] == "schema_valid"


def test_successful_provider_call_writes_schema_valid_checkpoint_and_jsonl(tmp_path: Path) -> None:
    config = _config(tmp_path)
    provider = SequenceProvider(_valid_annotation("PERF_0006"))

    result = run_checkpointed_annotation(config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert provider.calls == 1
    assert rows[0]["annotation_status"] == "schema_valid"
    assert rows[0]["schema_valid"] == "true"
    assert rows[0]["diagnostic_only"] == "true"
    assert rows[0]["official_pocr_computed"] == "false"
    assert rows[0]["route_level_pocr_aggregated"] == "false"
    assert len(jsonl_rows) == 1
    assert jsonl_rows[0]["annotation_status"] == "schema_valid"


def test_malformed_provider_output_writes_fail_closed_jsonl(tmp_path: Path) -> None:
    config = _config(tmp_path)
    provider = SequenceProvider(JSONDecodeError("bad json", "{", 0))

    result = run_checkpointed_annotation(config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert rows[0]["annotation_status"] == "malformed_json"
    assert rows[0]["schema_valid"] == "false"
    assert rows[0]["fail_closed"] == "true"
    assert jsonl_rows[0]["annotation_status"] == "malformed_json"
    assert jsonl_rows[0]["error"]["fail_closed"] is True  # type: ignore[index]


def test_provider_exception_preserves_previous_rows(tmp_path: Path) -> None:
    config = _config(tmp_path, ("PERF_0006", "CONS_0005"))
    provider = SequenceProvider(_valid_annotation("PERF_0006"), RuntimeError("provider down"))

    result = run_checkpointed_annotation(config, client=provider)

    rows = {row["case_id"]: row for row in _read_csv(result.paths.annotation_manifest_csv)}
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert rows["PERF_0006"]["annotation_status"] == "schema_valid"
    assert rows["CONS_0005"]["annotation_status"] == "provider_call_failed"
    assert provider.calls == 2
    assert len(jsonl_rows) == 2


def test_resume_skips_schema_valid_rows_and_does_not_duplicate_jsonl(tmp_path: Path) -> None:
    config = _config(tmp_path)
    run_checkpointed_annotation(config, client=SequenceProvider(_valid_annotation("PERF_0006")))

    provider = ExplodingProvider()
    result = run_checkpointed_annotation(config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert provider.calls == 0
    assert rows[0]["annotation_status"] == "schema_valid"
    assert rows[0]["call_status"] == "skipped_existing"
    assert len(jsonl_rows) == 1


def test_retry_failed_requires_explicit_flag(tmp_path: Path) -> None:
    config = _config(tmp_path)
    run_checkpointed_annotation(config, client=SequenceProvider(RuntimeError("provider down")))

    skipped_provider = SequenceProvider(_valid_annotation("PERF_0006"))
    skipped_result = run_checkpointed_annotation(config, client=skipped_provider)
    assert skipped_provider.calls == 0
    assert _read_csv(skipped_result.paths.annotation_manifest_csv)[0]["annotation_status"] == "provider_call_failed"

    retry_config = CheckpointedAnnotationConfig(**{**config.__dict__, "retry_failed": True})
    retry_provider = SequenceProvider(_valid_annotation("PERF_0006"))
    retry_result = run_checkpointed_annotation(retry_config, client=retry_provider)
    assert retry_provider.calls == 1
    assert _read_csv(retry_result.paths.annotation_manifest_csv)[0]["annotation_status"] == "schema_valid"
    assert len(_read_jsonl(retry_result.paths.safe_annotation_outputs_jsonl)) == 1


def test_schema_invalid_checkpoint_is_not_retried_by_retry_failed(tmp_path: Path) -> None:
    config = _config(tmp_path)
    run_checkpointed_annotation(config, client=SequenceProvider(_invalid_annotation("PERF_0006")))

    retry_config = CheckpointedAnnotationConfig(**{**config.__dict__, "retry_failed": True})
    provider = ExplodingProvider()
    result = run_checkpointed_annotation(retry_config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    assert provider.calls == 0
    assert rows[0]["annotation_status"] == "schema_invalid"


def test_no_live_flag_means_no_provider_call_and_no_fake_jsonl(tmp_path: Path) -> None:
    config = _config(tmp_path, live_enabled=False)
    provider = ExplodingProvider()

    result = run_checkpointed_annotation(config, client=provider)

    assert provider.calls == 0
    assert result.not_run_reason
    assert result.paths.live_smoke_not_run_md.is_file()
    assert result.paths.safe_annotation_outputs_jsonl.is_file()
    assert _read_jsonl(result.paths.safe_annotation_outputs_jsonl) == []
    assert _read_csv(result.paths.annotation_manifest_csv)[0]["annotation_status"] == "not_run"


def test_api_key_value_is_never_serialized(tmp_path: Path, monkeypatch) -> None:
    secret = "sk-test-secret-value"
    monkeypatch.setenv("SQLRB_LLM_API_KEY", secret)
    config = _config(tmp_path, api_key_env_name="SQLRB_LLM_API_KEY")

    result = run_checkpointed_annotation(config, client=SequenceProvider(_valid_annotation("PERF_0006")))

    all_output = _all_output_text(result.paths.annotation_dir.parent.parent.parent.parent.parent)
    assert secret not in all_output
    assert "SQLRB_LLM_API_KEY" in all_output
    assert "api_key_value_recorded" in all_output


def test_candidate_sha_mismatch_fails_closed_without_provider_retry(tmp_path: Path) -> None:
    case_ids = ("PERF_0006",)
    config = _config(tmp_path, case_ids)
    run_checkpointed_annotation(config, client=SequenceProvider(_valid_annotation("PERF_0006")))
    (config.candidate_root / "PERF_0006__postgres.sql").write_text("select 'changed';\n", encoding="utf-8")

    provider = ExplodingProvider()
    result = run_checkpointed_annotation(config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert provider.calls == 0
    assert rows[0]["annotation_status"] == "schema_invalid"
    assert rows[0]["error_type"] == "candidate_sha_mismatch"
    assert jsonl_rows[0]["annotation_status"] == "schema_invalid"
    assert jsonl_rows[0]["error"]["status"] == "candidate_sha_mismatch"  # type: ignore[index]


def test_duplicate_jsonl_rows_fail_closed_deterministically(tmp_path: Path) -> None:
    config = _config(tmp_path)
    result = run_checkpointed_annotation(config, client=SequenceProvider(_valid_annotation("PERF_0006")))
    original = result.paths.safe_annotation_outputs_jsonl.read_text(encoding="utf-8")
    result.paths.safe_annotation_outputs_jsonl.write_text(original + original, encoding="utf-8")

    provider = ExplodingProvider()
    result = run_checkpointed_annotation(config, client=provider)

    rows = _read_csv(result.paths.annotation_manifest_csv)
    jsonl_rows = _read_jsonl(result.paths.safe_annotation_outputs_jsonl)
    assert provider.calls == 0
    assert rows[0]["annotation_status"] == "schema_invalid"
    assert rows[0]["error_type"] == "duplicate_annotation_rows"
    assert len(jsonl_rows) == 1
    assert jsonl_rows[0]["error"]["status"] == "duplicate_annotation_rows"  # type: ignore[index]
