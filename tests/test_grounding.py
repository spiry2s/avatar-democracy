"""
Unit tests for delegate grounding (recorded positions) in backend/profile.py
and their inclusion in the Avatar's config block (backend/avatar.py). Pure logic,
no API calls.
"""

import pytest

from backend import avatar
from backend.profile import CitizenProfile


def make_profile_with_delegate():
    p = CitizenProfile()
    p.add_delegate("surveillance", "ACLU", "civil liberties")
    p.delegates[0].active_at = 0.0  # bypass cooling-off so the delegate is active
    return p


def test_add_source_to_delegate():
    p = make_profile_with_delegate()
    src = p.add_source("surveillance", "2023 statement", "Opposes warrantless bulk collection.")
    assert src["id"]
    assert p.delegates[0].sources[0]["text"] == "Opposes warrantless bulk collection."


def test_add_source_requires_text():
    p = make_profile_with_delegate()
    with pytest.raises(ValueError):
        p.add_source("surveillance", "title", "   ")


def test_add_source_unknown_delegate():
    p = make_profile_with_delegate()
    with pytest.raises(ValueError):
        p.add_source("fiscal", "t", "text")


def test_remove_source():
    p = make_profile_with_delegate()
    src = p.add_source("surveillance", "s", "some position")
    assert p.remove_source("surveillance", src["id"]) is True
    assert p.delegates[0].sources == []
    assert p.remove_source("surveillance", "nonexistent") is False


def test_sources_survive_serialization_round_trip():
    p = make_profile_with_delegate()
    p.add_source("surveillance", "2023 statement", "Opposes bulk collection.")
    restored = CitizenProfile.from_dict(p.to_dict())
    assert restored.delegates[0].sources[0]["title"] == "2023 statement"
    assert restored.delegates[0].sources[0]["text"] == "Opposes bulk collection."


def test_config_block_includes_grounded_sources():
    p = make_profile_with_delegate()
    p.compass = {}
    p.add_source("surveillance", "2023 ACLU statement", "Opposes warrantless surveillance expansion.")
    block = avatar._build_config_block(p)
    assert "RECORDED POSITIONS" in block
    assert "2023 ACLU statement" in block
    assert "Opposes warrantless surveillance expansion." in block


def test_config_block_marks_ungrounded_delegate():
    p = make_profile_with_delegate()  # no sources attached
    p.compass = {}
    block = avatar._build_config_block(p)
    assert "no recorded positions attached" in block
