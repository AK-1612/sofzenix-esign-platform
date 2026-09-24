"""
Pydantic schemas for the AI Call Automation from Excel feature.

Covers:
- Lead: a row imported from the sales/leads Excel sheet.
- CallStatus: the fixed lifecycle of a call attempt.
- CallResult: the record automatically saved after each AI call attempt.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class CallStatus(str, Enum):
    """Fixed set of call statuses tracked for every lead."""

    NOT_CALLED = "Not Called"
    CALLING = "Calling"
    CONNECTED = "Connected"
    NO_ANSWER = "No Answer"
    BUSY = "Busy"
    FAILED = "Failed"
    INTERESTED = "Interested"
    NOT_INTERESTED = "Not Interested"
    FOLLOW_UP = "Follow-up"
    APPOINTMENT = "Appointment"
    CONVERTED = "Converted"


class InterestLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "—"


# Statuses that represent "the phone never really connected" -> no interest/score yet.
NO_CONTACT_STATUSES = {
    CallStatus.NOT_CALLED,
    CallStatus.CALLING,
    CallStatus.NO_ANSWER,
    CallStatus.BUSY,
    CallStatus.FAILED,
}

# Default "Next Action" suggested per status, used when the AI scoring step
# does not override it explicitly.
DEFAULT_NEXT_ACTION = {
    CallStatus.NOT_CALLED: "Call Lead",
    CallStatus.CALLING: "Wait",
    CallStatus.CONNECTED: "Review Transcript",
    CallStatus.NO_ANSWER: "Retry",
    CallStatus.BUSY: "Retry",
    CallStatus.FAILED: "Retry",
    CallStatus.INTERESTED: "Sales Call",
    CallStatus.NOT_INTERESTED: "Close Lead",
    CallStatus.FOLLOW_UP: "Follow-up",
    CallStatus.APPOINTMENT: "Confirm Appointment",
    CallStatus.CONVERTED: "Onboard Client",
}


class LeadBase(BaseModel):
    name: str = Field(..., description="Lead's full name")
    mobile: str = Field(..., description="Lead's mobile number")
    service: Optional[str] = Field(None, description="Service the lead enquired about")
    budget: Optional[str] = Field(None, description="Lead's stated budget, e.g. ₹50,000")
    city: Optional[str] = Field(None, description="Lead's city / location")

    @field_validator("mobile")
    @classmethod
    def normalize_mobile(cls, value: str) -> str:
        digits = "".join(ch for ch in str(value) if ch.isdigit())
        if len(digits) < 10:
            raise ValueError(f"Invalid mobile number: {value!r}")
        return digits[-10:]


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    call_status: CallStatus = CallStatus.NOT_CALLED

    class Config:
        from_attributes = True


class LeadUploadSummary(BaseModel):
    total_rows: int
    imported: int
    skipped: int
    errors: list[str] = Field(default_factory=list)
    leads: list[Lead] = Field(default_factory=list)


class AIPromptPreview(BaseModel):
    """The structured prompt handed to the AI calling agent for one lead."""

    lead_id: UUID
    system_prompt: str
    opening_line: str
    key_questions: list[str]
    context: dict


class CallResult(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lead_id: UUID
    name: str
    mobile: str
    call_status: CallStatus = CallStatus.NOT_CALLED
    duration_seconds: int = 0
    interest: InterestLevel = InterestLevel.NONE
    score: Optional[int] = Field(None, ge=0, le=100)
    next_action: str = DEFAULT_NEXT_ACTION[CallStatus.NOT_CALLED]
    transcript: Optional[str] = None
    notes: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

    @property
    def duration_display(self) -> str:
        minutes, seconds = divmod(max(self.duration_seconds, 0), 60)
        return f"{minutes:02d}:{seconds:02d}"


class CallResultUpdate(BaseModel):
    """Payload the telephony/AI voice webhook posts back after a call ends."""

    call_status: CallStatus
    duration_seconds: int = 0
    transcript: Optional[str] = None
    notes: Optional[str] = None
