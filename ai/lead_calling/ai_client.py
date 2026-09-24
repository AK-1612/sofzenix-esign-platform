"""
Thin AI client used to score a finished call.

If AI_API_KEY / OPENAI_API_KEY is configured, the transcript is sent to the
LLM to classify interest level, produce a 0-100 lead score, and suggest the
next action. Otherwise a deterministic keyword-based heuristic is used, so
the whole feature still runs end-to-end without any external API key
(useful for local dev / demos).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from .schemas import CallStatus, InterestLevel

AI_API_KEY = os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")
AI_MODEL = os.getenv("AI_SCORING_MODEL", "gpt-4o-mini")

POSITIVE_WORDS = {
    "interested", "yes", "sounds good", "sure", "definitely", "book",
    "appointment", "proceed", "go ahead", "when can", "how much",
}
NEGATIVE_WORDS = {
    "not interested", "no thanks", "remove my number", "stop calling",
    "already have", "not now", "busy",
}


@dataclass
class CallAnalysis:
    interest: InterestLevel
    score: int
    suggested_status: CallStatus
    next_action: str


def _heuristic_analysis(transcript: str, duration_seconds: int) -> CallAnalysis:
    text = (transcript or "").lower()

    if any(phrase in text for phrase in NEGATIVE_WORDS):
        return CallAnalysis(InterestLevel.LOW, 15, CallStatus.NOT_INTERESTED, "Close Lead")

    positive_hits = sum(1 for phrase in POSITIVE_WORDS if phrase in text)

    if positive_hits >= 3 or "appointment" in text or "schedule" in text:
        return CallAnalysis(InterestLevel.HIGH, 90, CallStatus.APPOINTMENT, "Confirm Appointment")
    if positive_hits >= 1:
        base = 60 + min(positive_hits * 8, 30)
        return CallAnalysis(InterestLevel.MEDIUM, base, CallStatus.INTERESTED, "Sales Call")
    if duration_seconds >= 60:
        return CallAnalysis(InterestLevel.MEDIUM, 55, CallStatus.FOLLOW_UP, "Follow-up")

    return CallAnalysis(InterestLevel.LOW, 30, CallStatus.FOLLOW_UP, "Follow-up")


def _llm_analysis(transcript: str, duration_seconds: int) -> CallAnalysis | None:
    if not AI_API_KEY:
        return None
    try:
        import urllib.request

        payload = {
            "model": AI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You score a sales call transcript. Respond ONLY with JSON: "
                        '{"interest": "High|Medium|Low", "score": 0-100, '
                        '"status": "Interested|Not Interested|Follow-up|Appointment|Converted", '
                        '"next_action": "short string"}'
                    ),
                },
                {"role": "user", "content": transcript or "(no speech captured)"},
            ],
            "max_tokens": 200,
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AI_API_KEY}",
            },
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            body = json.loads(response.read().decode())
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(re.search(r"\{.*\}", content, re.S).group())
        return CallAnalysis(
            interest=InterestLevel(parsed.get("interest", "Medium")),
            score=int(parsed.get("score", 50)),
            suggested_status=CallStatus(parsed.get("status", "Follow-up")),
            next_action=parsed.get("next_action", "Follow-up"),
        )
    except Exception:
        # Any failure (network, parsing, quota) -> fall back to the heuristic.
        return None


def analyze_call(transcript: str, duration_seconds: int) -> CallAnalysis:
    """Score a call transcript. Tries the LLM first, falls back to a heuristic."""

    return _llm_analysis(transcript, duration_seconds) or _heuristic_analysis(
        transcript, duration_seconds
    )
