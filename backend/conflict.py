"""
Cross-bill conflict detection.

When a bill freezes, check whether it conflicts with already-passed bills —
contradicts, repeals, overrides, duplicates, or is legally incompatible with them.
One cheap LLM call; best-effort (a failure never blocks the lifecycle).
"""

from __future__ import annotations

import json
import os
from typing import Any

from anthropic import Anthropic

from backend.config import CHECKER_MODEL


def get_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set.")
    return Anthropic(api_key=api_key)


def detect_conflicts(
    analysis: dict[str, Any],
    passed_bills: list[dict[str, Any]],
    client: Anthropic | None = None,
) -> list[dict[str, Any]]:
    """Compare a new bill's analysis against previously passed bills.

    Args:
        analysis: the new bill's analysis dict (title, plain_summary, sections).
        passed_bills: [{"id", "title", "summary"}] of already-passed bills.

    Returns:
        [{"bill_id", "title", "conflict"}] for passed bills the new bill conflicts with.
    """
    if not analysis or not passed_bills:
        return []
    if client is None:
        client = get_client()

    sections = "; ".join(s.get("heading", "") for s in analysis.get("sections", []))
    lines = [
        "A NEW bill is proposed. Identify which, if any, of the PREVIOUSLY PASSED bills it",
        "directly conflicts with — it contradicts, repeals, overrides, duplicates, or is",
        "legally incompatible with them. Be conservative: only flag genuine conflicts.",
        "",
        f"NEW BILL: {analysis.get('title', '')}",
        f"  summary: {analysis.get('plain_summary', '')}",
        f"  sections: {sections}",
        "",
        "PREVIOUSLY PASSED BILLS:",
    ]
    for b in passed_bills:
        lines.append(f"  [{b['id']}] {b.get('title', '')}: {b.get('summary', '')}")
    lines.append("")
    lines.append('Output ONLY JSON: a list of {"bill_id": "<id>", "conflict": "<one sentence>"}.')
    lines.append("Return [] if there are no genuine conflicts. No prose, no markdown fences.")

    message = client.messages.create(
        model=CHECKER_MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": "\n".join(lines)}],
    )
    text = "".join(b.text for b in message.content if hasattr(b, "text")).strip()
    if text.startswith("```"):
        rows = text.split("\n")
        end = len(rows) - 1 if rows[-1].strip() == "```" else len(rows)
        text = "\n".join(rows[1:end])

    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("conflicts", [])
    if not isinstance(data, list):
        return []

    titles = {b["id"]: b.get("title", "") for b in passed_bills}
    out = []
    for item in data:
        if not isinstance(item, dict):
            continue
        bid = str(item.get("bill_id", "")).strip()
        if bid in titles:  # only real passed-bill ids (drops hallucinations)
            out.append({"bill_id": bid, "title": titles[bid], "conflict": str(item.get("conflict", "")).strip()})
    return out
