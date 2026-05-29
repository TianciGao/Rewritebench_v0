import pytest

from sql_rewrite_bench.pocr.json_output_guard import guarded_json_loads


def test_guarded_json_loads_strict_object() -> None:
    result = guarded_json_loads('{"case_id": "PERF_0006"}')

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "PERF_0006"}
    assert result.repaired is False
    assert result.fence_stripped is False
    assert result.original_status == "valid_json_object"
    assert result.final_status == "parsed"


def test_guarded_json_loads_safe_json_fence() -> None:
    result = guarded_json_loads('```json\n{"case_id": "CONS_0005"}\n```')

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "CONS_0005"}
    assert result.repaired is True
    assert result.fence_stripped is True
    assert result.repair_strategy == "strip_json_code_fence"


def test_guarded_json_loads_surrounding_whitespace() -> None:
    result = guarded_json_loads('\n  {"case_id": "PERF_0006"}  \n')

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "PERF_0006"}
    assert result.repaired is False


def test_provider_text_before_after_json_fails_closed_by_default() -> None:
    result = guarded_json_loads('Here is JSON: {"case_id": "PERF_0006"} done')

    assert result.raw_status == "provider_text_around_json"
    assert result.parsed is None
    assert result.schema_status == "schema_invalid"


def test_provider_text_can_be_extracted_only_when_explicitly_allowed() -> None:
    result = guarded_json_loads('Here is JSON: {"case_id": "PERF_0006"} done', allow_surrounding_text=True)

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "PERF_0006"}
    assert result.repaired is True
    assert result.repair_strategy == "extract_single_json_object"


def test_guarded_json_loads_malformed_json_fails_closed() -> None:
    result = guarded_json_loads('{"case_id": "PERF_0006", "atoms": [}')

    assert result.raw_status == "malformed_json"
    assert result.parsed is None
    assert result.schema_status == "schema_invalid"
    assert result.repaired is False


def test_truncated_json_is_classified() -> None:
    result = guarded_json_loads('{"case_id": "PERF_0006", "atoms": [')

    assert result.raw_status == "truncated_json"
    assert result.parsed is None


def test_empty_response_is_classified() -> None:
    result = guarded_json_loads("")

    assert result.raw_status == "empty_response"
    assert result.parsed is None


def test_non_object_json_fails_closed() -> None:
    result = guarded_json_loads('["not", "an", "object"]')

    assert result.raw_status == "not_json_object"
    assert result.parsed is None


def test_multi_object_response_fails_closed() -> None:
    result = guarded_json_loads('{"a": 1}\n{"b": 2}')

    assert result.raw_status == "multi_object_response"
    assert result.parsed is None


def test_timeout_response_is_classified() -> None:
    result = guarded_json_loads(None, timed_out=True)

    assert result.raw_status == "timeout"
    assert result.parsed is None


def test_guarded_json_repair_mode_is_not_authorized() -> None:
    with pytest.raises(ValueError, match="not implemented or authorized"):
        guarded_json_loads('{"case_id": "PERF_0006"}', repair_mode=True)
