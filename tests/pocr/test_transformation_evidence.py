from sql_rewrite_bench.pocr.transformation_evidence import (
    candidate_aligns_with_positive_span,
    is_source_like_noop,
    normalize_sql_for_pocr_diff,
    source_candidate_changed,
    span_present_in_candidate_but_absent_or_different_from_source,
)


def test_normalize_sql_for_pocr_diff_strips_comments_and_normalizes_tokens() -> None:
    assert normalize_sql_for_pocr_diff("SELECT  A -- local\nFROM t") == "select a from t"
    assert normalize_sql_for_pocr_diff("select /* hint */ a from t") == "select a from t"


def test_source_like_noop_uses_normalized_sql_text() -> None:
    assert is_source_like_noop("SELECT a FROM t", "select  a\nfrom t")
    assert not is_source_like_noop("SELECT a FROM t", "SELECT b FROM t")


def test_candidate_specific_span_requires_absence_from_source() -> None:
    assert span_present_in_candidate_but_absent_or_different_from_source(
        "where rn = 1",
        source_sql="select * from t",
        candidate_sql="select * from t where rn = 1",
    )
    assert not span_present_in_candidate_but_absent_or_different_from_source(
        "from t",
        source_sql="select * from t",
        candidate_sql="select * from t where rn = 1",
    )


def test_candidate_aligns_with_positive_span_is_comparison_only() -> None:
    assert candidate_aligns_with_positive_span(
        "where rn = 1",
        candidate_sql="select * from t where rn = 1",
        positive_sql="select * from t where rn = 1",
    )
    assert not candidate_aligns_with_positive_span(
        "where rn = 1",
        candidate_sql="select * from t",
        positive_sql="select * from t where rn = 1",
    )


def test_source_candidate_changed_is_text_diff_only_not_semantics() -> None:
    assert source_candidate_changed("select * from t", "select a from t")
