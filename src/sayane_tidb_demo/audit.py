from __future__ import annotations

from typing import Any


def lightweight_audit(query: str, selected_chunks: list[dict[str, Any]]) -> dict[str, Any]:
    contents = "\n".join(str(chunk.get("content", "")) for chunk in selected_chunks)
    drift_risk = "low" if any(term.lower() in contents.lower() for term in query.split()) else "medium"
    return {
        "preserved": ["retrieved source chunks are logged"],
        "inferred": [],
        "drift_risk": drift_risk,
        "unresolved": ["full RDE scoring is outside this demo"],
    }
