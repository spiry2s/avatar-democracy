"""
Unit tests for delegate drift detection's pure selection logic
(backend.avatar._delegate_followed_sections). The LLM derivation in
detect_drift() is exercised live, not here.
"""

from backend.avatar import _delegate_followed_sections
from backend.profile import CitizenProfile


def grounded_profile():
    p = CitizenProfile()
    p.add_delegate("surveillance", "ACLU")
    p.delegates[0].active_at = 0.0  # make active (bypass cooling-off)
    p.add_source("surveillance", "2023 statement", "Opposes warrantless surveillance.")
    return p


def test_selects_only_grounded_delegate_sections():
    p = grounded_profile()
    section_votes = [
        {"section_id": "S1", "basis": "delegate:ACLU", "position": "no"},
        {"section_id": "S2", "basis": "values", "position": "yes"},
        {"section_id": "S3", "basis": "delegate:ACLU", "position": "yes"},
    ]
    targets = _delegate_followed_sections(p, section_votes)
    assert {t["section_id"] for t in targets} == {"S1", "S3"}
    assert all(t["delegate"] == "ACLU" and t["sources"] for t in targets)


def test_ungrounded_delegate_not_checked():
    p = CitizenProfile()
    p.add_delegate("fiscal", "Sen. X")          # no recorded positions
    p.delegates[0].active_at = 0.0
    sv = [{"section_id": "S1", "basis": "delegate:Sen. X", "position": "no"}]
    assert _delegate_followed_sections(p, sv) == []


def test_pending_delegate_not_checked():
    p = CitizenProfile()
    p.add_delegate("surveillance", "ACLU")      # left in cooling-off (pending)
    p.add_source("surveillance", "t", "text")
    sv = [{"section_id": "S1", "basis": "delegate:ACLU", "position": "no"}]
    assert _delegate_followed_sections(p, sv) == []


def test_non_delegate_basis_ignored():
    p = grounded_profile()
    sv = [{"section_id": "S1", "basis": "compass", "position": "no"}]
    assert _delegate_followed_sections(p, sv) == []
