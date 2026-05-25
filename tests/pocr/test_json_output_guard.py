import pytest

from sql_rewrite_bench.pocr.json_output_guard import guarded_json_loads


def test_guarded_json_loads_strict_object() -> None:
    result = guarded_json_loads('{"case_id": "PERF_0006"}')

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "PERF_0006"}
    assert result.repaired is False
    assert result.fence_stripped is False


def test_guarded_json_loads_safe_json_fence() -> None:
    result = guarded_json_loads('```json\n{"case_id": "CONS_0005"}\n```')

    assert result.raw_status == "parsed"
    assert result.parsed == {"case_id": "CONS_0005"}
    assert result.repaired is False
    assert result.fence_stripped is True


def test_guarded_json_loads_malformed_json_fails_closed() -> None:
    result = guarded_json_loads('{"case_id": "PERF_0006", "atoms": [}')

    assert result.raw_status == "malformed_json"
    assert result.parsed is None
    assert result.schema_status == "schema_invalid"
    assert result.repaired is False


def test_guarded_json_repair_mode_is_not_authorized() -> None:
    with pytest.raises(ValueError, match="not implemented or authorized"):
        guarded_json_loads('{"case_id": "PERF_0006"}', repair_mode=True)
