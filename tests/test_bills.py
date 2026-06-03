"""
Unit tests for the bill lifecycle state machine (backend/bills.py).

These exercise the pure transition + tally logic — no API calls, no disk.
Run from the repo root:  python -m pytest
"""

import time

import pytest

from backend import bills, config
from backend.bills import BillState


def make_open_bill(scope: str = "ordinary") -> bills.Bill:
    b = bills.propose("Test Bill", "Some substantive bill text.", scope)
    bills.open_for_endorsement(b)
    return b


# ── propose / versions / open ────────────────────────────────────────────────


def test_propose_defaults():
    b = bills.propose("Title", "text", "ordinary")
    assert b.state == BillState.DRAFT
    assert b.current_version == 1
    assert len(b.versions) == 1
    assert b.endorsement_threshold == config.ENDORSEMENT_THRESHOLDS["ordinary"]


def test_propose_requires_text():
    with pytest.raises(ValueError):
        bills.propose("Title", "   ", "ordinary")


def test_scope_threshold_tiers():
    for scope in ("ordinary", "major", "constitutional"):
        assert bills.propose("a", "x", scope).endorsement_threshold == config.ENDORSEMENT_THRESHOLDS[scope]
    # invalid scope falls back to ordinary
    assert bills.propose("a", "x", "bogus").scope == "ordinary"


def test_add_version_only_in_draft():
    b = bills.propose("T", "v1 text")
    bills.add_version(b, "v2 text", "second")
    assert b.current_version == 2 and len(b.versions) == 2
    bills.open_for_endorsement(b)
    with pytest.raises(ValueError):
        bills.add_version(b, "v3", "nope")


def test_open_for_endorsement():
    b = bills.propose("T", "text")
    bills.open_for_endorsement(b)
    assert b.state == BillState.ENDORSING
    with pytest.raises(ValueError):
        bills.open_for_endorsement(b)  # no longer a draft


# ── endorsement ──────────────────────────────────────────────────────────────


def test_endorse_idempotent_and_total():
    b = make_open_bill()
    bills.endorse(b, "local")
    bills.endorse(b, "local")  # idempotent
    assert len(b.endorsements) == 1
    b.simulated_endorsements = 5
    assert bills.total_endorsements(b) == 6


def test_endorse_requires_endorsing_state():
    b = bills.propose("T", "text")  # still a draft
    with pytest.raises(ValueError):
        bills.endorse(b)


def test_revoke_within_and_outside_window():
    b = make_open_bill()
    bills.endorse(b, "local")
    assert bills.revoke_endorsement(b, "local") is True
    assert len(b.endorsements) == 0

    bills.endorse(b, "local")
    b.endorsements[0]["revocable_until"] = time.time() - 1  # window expired
    assert bills.revoke_endorsement(b, "local") is False
    assert len(b.endorsements) == 1  # locked in


def test_revoke_missing_returns_false():
    b = make_open_bill()
    assert bills.revoke_endorsement(b, "local") is False


# ── freeze / cooling-off ─────────────────────────────────────────────────────


def test_freeze_below_threshold_is_noop():
    b = make_open_bill()
    bills.endorse(b)
    assert bills.freeze_if_threshold_met(b) is False
    assert b.state == BillState.ENDORSING


def test_freeze_at_threshold():
    b = make_open_bill()
    b.simulated_endorsements = b.endorsement_threshold
    assert bills.freeze_if_threshold_met(b) is True
    assert b.state == BillState.COOLING_OFF
    assert b.frozen_version == b.current_version
    assert b.cooling_off_until is not None


def test_refresh_state_promotes_after_cooldown():
    b = make_open_bill()
    b.simulated_endorsements = b.endorsement_threshold
    bills.freeze_if_threshold_met(b)

    b.cooling_off_until = time.time() + 1000  # not yet
    assert bills.refresh_state(b) is False
    assert b.state == BillState.COOLING_OFF

    b.cooling_off_until = time.time() - 1  # elapsed
    assert bills.refresh_state(b) is True
    assert b.state == BillState.VOTING


def test_frozen_text_picks_frozen_version():
    b = bills.propose("T", "v1 body")
    bills.add_version(b, "v2 final body", "edit")
    b.frozen_version = 1
    assert bills.frozen_text(b) == "v1 body"
    b.frozen_version = 2
    assert bills.frozen_text(b) == "v2 final body"


# ── tally / result ───────────────────────────────────────────────────────────


def test_tally_single_vote():
    av = {"section_votes": [
        {"section_id": "a", "position": "yes"},
        {"section_id": "b", "position": "no"},
        {"section_id": "c", "position": "abstain"},
    ]}
    t = bills.tally_single_vote(av)
    assert (t[0]["yes"], t[1]["no"], t[2]["abstain"]) == (1, 1, 1)


def test_compute_result_all_pass():
    r = bills.compute_result([{"section_id": "a", "heading": "", "yes": 1, "no": 0, "abstain": 0}], 0.5)
    assert r["passed"] is True
    assert r["sections_passed"] == 1


def test_compute_result_one_fail_kills_bill():
    tallies = [
        {"section_id": "a", "heading": "", "yes": 1, "no": 0, "abstain": 0},
        {"section_id": "b", "heading": "", "yes": 0, "no": 1, "abstain": 0},
    ]
    r = bills.compute_result(tallies, 0.5)
    assert r["passed"] is False
    assert (r["sections_passed"], r["sections_total"]) == (1, 2)


def test_compute_result_all_abstain_not_passed():
    r = bills.compute_result([{"section_id": "a", "heading": "", "yes": 0, "no": 0, "abstain": 1}], 0.5)
    assert r["per_section"][0]["passed"] is False
    assert r["per_section"][0]["contested"] is False
    assert r["passed"] is False  # no contested sections at all -> bill does not pass


def test_compute_result_procedural_no_contest_does_not_block():
    # A passing substantive section + an all-abstain procedural section (e.g. a title).
    tallies = [
        {"section_id": "s1", "heading": "substantive", "yes": 10, "no": 2, "abstain": 0},
        {"section_id": "title", "heading": "short title", "yes": 0, "no": 0, "abstain": 12},
    ]
    r = bills.compute_result(tallies, 0.5)
    assert r["passed"] is True              # the no-contest title does not sink the bill
    assert r["sections_passed"] == 1
    assert r["sections_contested"] == 1


def test_compute_result_ratio_boundary():
    tie = [{"section_id": "a", "heading": "", "yes": 1, "no": 1, "abstain": 0}]
    assert bills.compute_result(tie, 0.5)["per_section"][0]["passed"] is True   # >= 0.5
    assert bills.compute_result(tie, 0.6)["per_section"][0]["passed"] is False  # < 0.6


def test_compute_result_empty():
    r = bills.compute_result([], 0.5)
    assert r["passed"] is False
    assert r["sections_total"] == 0
