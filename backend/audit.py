"""
Append-only audit log.

Every consequential Avatar action is logged here: profile changes, delegate
adds/revocations, votes cast, and citizen overrides. The white paper makes
auditability a core legitimacy property — every Avatar action must be reviewable.

Storage is a simple JSON-lines file (one event per line). Append-only by
convention: we never rewrite history.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AUDIT_FILE = DATA_DIR / "audit.jsonl"


def log_event(event_type: str, details: dict[str, Any]) -> dict[str, Any]:
    """
    Append an event to the audit log.

    Args:
        event_type: e.g. "profile_created", "delegate_added", "delegate_revoked",
                    "vote_cast", "vote_overridden".
        details: arbitrary JSON-serializable context.

    Returns:
        The stored event record (including its timestamp).
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": time.time(),
        "event_type": event_type,
        "details": details,
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return event


def read_events(limit: int | None = None) -> list[dict[str, Any]]:
    """
    Read audit events, newest first.

    Args:
        limit: optional cap on number of events returned.

    Returns:
        List of event records, most recent first.
    """
    if not AUDIT_FILE.exists():
        return []

    events: list[dict[str, Any]] = []
    with AUDIT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    events.reverse()  # newest first
    if limit is not None:
        events = events[:limit]
    return events
