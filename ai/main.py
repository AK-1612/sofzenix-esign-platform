"""
Sofzenix AI Workspace Service - FastAPI entrypoint.

Currently wires up the AI Call Automation from Excel feature
(`lead_calling/`). Other AI submodules (ocr, classification, extraction,
contract_analysis, risk_detection, smart_search, assistant) will register
their routers here as they are implemented.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lead_calling.router import router as lead_calling_router

app = FastAPI(
    title="Sofzenix AI Workspace Service",
    description="AI & Document Intelligence microservice, including AI Call Automation from Excel.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lead_calling_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
