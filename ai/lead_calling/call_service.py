"""
Call orchestration: starts an AI-driven call for a lead using the prompt
built in prompt_generator.py, and processes the outcome into the
automatically-saved call result (step 4 of the pipeline).

TELEPHONY INTEGRATION POINT
----------------------------
`_dial_out` is where a real provider (Exotel, Twilio, Knowlarity, Ozonetel,
etc.) or an AI voice-agent platform (e.g. Bland AI, Vapi, Retell) would be
wired in: place the call, stream `prompt.system_prompt` / `prompt.opening_line`
/ `prompt.key_questions` to the voice agent, and call `complete_call(...)`
from that provider's webhook when the call ends.

When TELEPHONY_PROVIDER=MOCK (the default, no external account needed) a
call is simulated instantly so the whole pipeline can be demoed end-to-end.
"""

from __future__ import annotations

import os
import random
from uuid import UUID

from . import storage
from .ai_client import analyze_call
from .prompt_generator import build_prompt
from .schemas import AIPromptPreview, CallResult, CallResultUpdate, CallStatus, DEFAULT_NEXT_ACTION, InterestLevel

TELEPHONY_PROVIDER = os.getenv("TELEPHONY_PROVIDER", "MOCK").upper()


class LeadNotFoundError(Exception):
    pass


def get_prompt_for_lead(lead_id: UUID) -> AIPromptPreview:
    lead = storage.get_lead(lead_id)
    if not lead:
        raise LeadNotFoundError(str(lead_id))
    return build_prompt(lead)


def _mark_calling(lead_id: UUID, lead_name: str, lead_mobile: str) -> None:
    result = storage.get_call_result(lead_id) or CallResult(
        lead_id=lead_id, name=lead_name, mobile=lead_mobile
    )
    result.call_status = CallStatus.CALLING
    result.next_action = DEFAULT_NEXT_ACTION[CallStatus.CALLING]
    storage.upsert_call_result(result)


def _dial_out(lead_id: UUID, prompt: AIPromptPreview) -> None:
    """Place the outbound call. Swap this body for a real provider SDK call."""

    if TELEPHONY_PROVIDER == "MOCK":
        outcome = random.choices(
            [CallStatus.CONNECTED, CallStatus.NO_ANSWER, CallStatus.BUSY, CallStatus.FAILED],
            weights=[0.7, 0.15, 0.1, 0.05],
        )[0]

        if outcome != CallStatus.CONNECTED:
            complete_call(
                lead_id,
                CallResultUpdate(call_status=outcome, duration_seconds=0, transcript=None),
            )
            return

        duration = random.randint(45, 260)
        sample_replies = [
            "Yes I'm interested, can you tell me more about pricing?",
            "Not right now, maybe follow up next month.",
            "Sounds good, can we schedule an appointment tomorrow?",
            "Not interested, please remove my number.",
            "Ok sure, sounds good, go ahead and send details.",
        ]
        transcript = f"Lead: {random.choice(sample_replies)}"
        complete_call(
            lead_id,
            CallResultUpdate(
                call_status=CallStatus.CONNECTED,
                duration_seconds=duration,
                transcript=transcript,
            ),
        )
        return

    # Real provider integration example (pseudo-code):
    #
    # client = ExotelClient(api_key=os.environ["TELEPHONY_API_KEY"])
    # client.calls.create(
    #     to=f"+91{lead_mobile}",
    #     agent_config={"system_prompt": prompt.system_prompt, ...},
    #     webhook_url=f"{os.environ['PUBLIC_BASE_URL']}/api/v1/leads/calls/{lead_id}/result",
    # )
    raise NotImplementedError(f"Telephony provider '{TELEPHONY_PROVIDER}' is not wired up yet.")


def start_call(lead_id: UUID) -> CallResult:
    lead = storage.get_lead(lead_id)
    if not lead:
        raise LeadNotFoundError(str(lead_id))

    prompt = build_prompt(lead)
    _mark_calling(lead_id, lead.name, lead.mobile)
    _dial_out(lead_id, prompt)
    return storage.get_call_result(lead_id)  # type: ignore[return-value]


def complete_call(lead_id: UUID, update: CallResultUpdate) -> CallResult:
    """Called once the call ends (by the mock dialer above, or a real webhook).

    This is the "automatically saved" step: status, duration, interest, score
    and next action are all written to storage without manual entry.
    """

    lead = storage.get_lead(lead_id)
    if not lead:
        raise LeadNotFoundError(str(lead_id))

    result = storage.get_call_result(lead_id) or CallResult(
        lead_id=lead_id, name=lead.name, mobile=lead.mobile
    )

    result.call_status = update.call_status
    result.duration_seconds = update.duration_seconds
    result.transcript = update.transcript
    result.notes = update.notes

    if update.call_status in (CallStatus.CONNECTED,) and update.transcript:
        analysis = analyze_call(update.transcript, update.duration_seconds)
        result.interest = analysis.interest
        result.score = analysis.score
        result.call_status = analysis.suggested_status
        result.next_action = analysis.next_action
    else:
        result.interest = InterestLevel.NONE
        result.score = None
        result.next_action = DEFAULT_NEXT_ACTION.get(update.call_status, "Retry")

    storage.upsert_call_result(result)
    return result
