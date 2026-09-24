# AI Call Automation from Excel

Implements the two features requested:

1. **Excel Data → AI Prompt** — upload a leads sheet (`Name`, `Service`,
   `Budget`, `City`, + a mobile/phone column) and each row is turned into a
   structured, lead-specific AI prompt (system prompt, opening line, and
   relevant qualifying questions based on the `Service` column) instead of
   one generic script for every lead.
2. **Call Result Automatically Saved** — starting a call runs it through the
   AI agent (mocked by default, pluggable to a real telephony/voice-AI
   provider) and automatically writes back `Call Status`, `Duration`,
   `Interest`, `Score`, and `Next Action` — no manual data entry.

## Where things live

```
ai/
├── main.py                    FastAPI app entrypoint (mounted by docker-compose as ai-service)
├── requirements.txt
├── Dockerfile
└── lead_calling/
    ├── schemas.py             Lead, CallStatus enum, CallResult, etc. (Pydantic)
    ├── excel_parser.py        Excel Data -> AI Prompt: step 1, parses the uploaded sheet
    ├── prompt_generator.py    Excel Data -> AI Prompt: step 2, builds the per-lead prompt
    ├── ai_client.py           Scores a finished call (LLM if AI_API_KEY set, else heuristic)
    ├── call_service.py        Orchestrates dialing + saving the result; telephony integration point
    ├── storage.py             SQLite persistence (leads + call_results tables)
    ├── excel_export.py        Exports the results table back to .xlsx
    ├── router.py               REST API
    └── sample_leads.xlsx      Sample sheet matching the requested column layout

database/schema/V2__create_lead_calling_schema.sql   Production Postgres schema (Flyway)
frontend/src/pages/leads/index.tsx                   Dashboard: upload, "Call Now", live results table
frontend/src/services/leadCallingService.ts          Frontend API client
```

## Running it locally

```bash
cd ai
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000/docs for interactive API docs, or run the
frontend (`cd frontend && npm install && npm run dev`) and visit
`/leads` for the dashboard UI.

## API

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/leads/upload` | Upload the Excel sheet, import leads |
| GET | `/api/v1/leads` | List imported leads |
| GET | `/api/v1/leads/{id}/prompt` | Preview the AI prompt built for a lead |
| POST | `/api/v1/leads/{id}/call` | Start the AI call for a lead |
| POST | `/api/v1/leads/{id}/result` | Webhook: telephony/voice-AI provider reports the outcome |
| GET | `/api/v1/leads/results` | The auto-saved results table (optional `?status=` filter) |
| GET | `/api/v1/leads/results/export` | Download results as `.xlsx` |

## Call statuses

`Not Called`, `Calling`, `Connected`, `No Answer`, `Busy`, `Failed`,
`Interested`, `Not Interested`, `Follow-up`, `Appointment`, `Converted` —
exactly the set requested, enforced by the `CallStatus` enum and a Postgres
`CHECK` constraint in the migration.

## Plugging in a real telephony / voice-AI provider

`call_service._dial_out()` is the single integration point. Replace the
`TELEPHONY_PROVIDER == "MOCK"` branch with your provider's SDK call (Exotel,
Twilio, Knowlarity, Ozonetel, or an AI voice-agent platform like Bland AI /
Vapi / Retell), passing it `prompt.system_prompt`, `prompt.opening_line` and
`prompt.key_questions`, and have its webhook call
`POST /api/v1/leads/{id}/result` with the transcript when the call ends —
`ai_client.analyze_call()` then scores it and `call_service.complete_call()`
saves everything automatically. Set `AI_API_KEY` (OpenAI-compatible) to use
real LLM scoring instead of the built-in keyword heuristic.
