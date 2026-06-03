"""
Unit tests for multi-model divergence comparison (backend/avatar.find_divergences).
Pure logic — no API calls.
"""

from backend.avatar import find_divergences, _coerce_position, _norm_key


def test_no_divergence_when_equal():
    primary = {"a": "yes", "b": "no"}
    checker = {"a": "yes", "b": "no"}
    assert find_divergences(primary, checker) == set()


def test_divergence_detected():
    primary = {"a": "yes", "b": "no", "c": "abstain"}
    checker = {"a": "no", "b": "no", "c": "yes"}
    assert find_divergences(primary, checker) == {"a", "c"}


def test_checker_omission_not_flagged():
    primary = {"a": "yes", "b": "no"}
    checker = {"a": "yes"}  # checker did not cover section b
    assert find_divergences(primary, checker) == set()


def test_empty():
    assert find_divergences({}, {}) == set()


def test_coerce_position_shapes():
    assert _coerce_position("yes") == "yes"
    assert _coerce_position("  NO ") == "no"
    assert _coerce_position({"position": "abstain", "reasoning": "x"}) == "abstain"
    # checker sometimes returns a stringified vote object
    assert _coerce_position("{'position': 'no', 'basis': 'values'}") == "no"
    # non-position fields (recommendation / tension) coerce to empty -> dropped
    assert _coerce_position("vote against on balance") == ""


def test_norm_key_unifies_formats():
    # bare number, 'Sec.', 'Section', underscores all collapse to the distinctive id
    assert _norm_key("Sec. 101") == _norm_key("sec_101") == _norm_key("Section 101") == _norm_key("101") == "101"


def test_find_divergences_tolerates_key_format_mismatch():
    # primary uses 'Sec. 1' / 'Sec. 101'; checker uses 'sec_1' / 'sec_101'
    primary = {"Sec. 1": "abstain", "Sec. 101": "no"}
    checker = {"sec_1": "yes", "sec_101": "no"}
    assert find_divergences(primary, checker) == {"Sec. 1"}
