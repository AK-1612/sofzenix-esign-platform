"""
REST API for the AI Call Automation from Excel feature.

Endpoints
---------
POST   /api/v1/leads/upload           Upload an Excel sheet of leads
GET    /api/v1/leads                  List imported leads
GET    /api/v1/leads/{lead_id}/prompt Preview the AI prompt built for a lead
POST   /api/v1/leads/{lead_id}/call   Start an AI call for a lead
POST   /api/v1/leads/{lead_id}/result Webhook: telephony/AI provider posts the outcome
GET    /api/v1/leads/results          List all call results (the dashboard table)
GET    /api/v1/leads/results/export   Download the call results as .xlsx
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
import io

from . import call_service, storage
from .call_service import LeadNotFoundError
from .excel_export import export_call_results
from .excel_parser import parse_leads_excel
from .schemas import (
    AIPromptPreview,
    CallResult,
    CallResultUpdate,
    CallStatus,
    Lead,
    LeadUploadSummary,
)

router = APIRouter(prefix="/api/v1/leads", tags=["Lead Calling Automation"])


@router.on_event("startup")
def _startup() -> None:
    storage.init_db()


@router.post("/upload", response_model=LeadUploadSummary)
async def upload_leads(file: UploadFile = File(...)) -> LeadUploadSummary:
    """Excel Data -> AI Prompt: import leads (Name, Service, Budget, City, Mobile)."""

    if not file.filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(400, "Please upload an .xlsx Excel file.")

    contents = await file.read()
    summary = parse_leads_excel(contents)

    for lead in summary.leads:
        storage.save_lead(lead)

    return summary


@router.get("", response_model=list[Lead])
def list_leads() -> list[Lead]:
    return storage.list_leads()


@router.get("/{lead_id}/prompt", response_model=AIPromptPreview)
def preview_prompt(lead_id: UUID) -> AIPromptPreview:
    """See exactly what the AI agent will say/ask for this specific lead."""

    try:
        return call_service.get_prompt_for_lead(lead_id)
    except LeadNotFoundError as exc:
        raise HTTPException(404, "Lead not found") from exc


@router.post("/{lead_id}/call", response_model=CallResult)
def start_call(lead_id: UUID) -> CallResult:
    """Trigger the AI call for one lead."""

    try:
        return call_service.start_call(lead_id)
    except LeadNotFoundError as exc:
        raise HTTPException(404, "Lead not found") from exc


@router.post("/{lead_id}/result", response_model=CallResult)
def post_call_result(lead_id: UUID, update: CallResultUpdate) -> CallResult:
    """Telephony/AI voice provider webhook: reports the finished call outcome.

    This is what makes the results table update automatically once a call
    ends, with no manual data entry.
    """

    try:
        return call_service.complete_call(lead_id, update)
    except LeadNotFoundError as exc:
        raise HTTPException(404, "Lead not found") from exc


@router.get("/results", response_model=list[CallResult])
def list_results(status: CallStatus | None = Query(default=None)) -> list[CallResult]:
    return storage.list_call_results(status=status)


@router.get("/results/export")
def export_results() -> StreamingResponse:
    results = storage.list_call_results()
    file_bytes = export_call_results(results)
    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=call_results.xlsx"},
    )
