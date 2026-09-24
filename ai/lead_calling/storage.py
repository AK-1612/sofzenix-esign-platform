"""
Call Result Automatically Saved (step 4 of the pipeline).

Lightweight persistence for leads and their call results. Uses SQLite by
default (zero external dependencies, works out of the box for local dev and
demos); point DATABASE_URL at Postgres in production and swap this module
for a SQLAlchemy/asyncpg implementation against the
`database/schema/V2__create_lead_calling_schema.sql` tables — the row shape
is identical so the API layer does not need to change.
"""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator
from uuid import UUID

from .schemas import CallResult, CallStatus, DEFAULT_NEXT_ACTION, InterestLevel, Lead

DB_PATH = os.getenv("LEAD_CALLING_DB_PATH", "lead_calling.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    service TEXT,
    budget TEXT,
    city TEXT,
    call_status TEXT NOT NULL DEFAULT 'Not Called',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS call_results (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL REFERENCES leads(id),
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    call_status TEXT NOT NULL DEFAULT 'Not Called',
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    interest TEXT NOT NULL DEFAULT '—',
    score INTEGER,
    next_action TEXT NOT NULL,
    transcript TEXT,
    notes TEXT,
    updated_at TEXT NOT NULL
);
"""


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(_SCHEMA)


def save_lead(lead: Lead) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO leads (id, name, mobile, service, budget, city, call_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(lead.id),
                lead.name,
                lead.mobile,
                lead.service,
                lead.budget,
                lead.city,
                lead.call_status.value,
                lead.created_at.isoformat(),
            ),
        )
        # Every imported lead starts life as a "Not Called" row in the results
        # table too, so the dashboard shows the full pipeline immediately.
        conn.execute(
            """
            INSERT OR IGNORE INTO call_results
                (id, lead_id, name, mobile, call_status, duration_seconds, interest, score, next_action, updated_at)
            VALUES (?, ?, ?, ?, ?, 0, ?, NULL, ?, ?)
            """,
            (
                str(lead.id),
                str(lead.id),
                lead.name,
                lead.mobile,
                CallStatus.NOT_CALLED.value,
                InterestLevel.NONE.value,
                DEFAULT_NEXT_ACTION[CallStatus.NOT_CALLED],
                datetime.utcnow().isoformat(),
            ),
        )


def get_lead(lead_id: UUID) -> Lead | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (str(lead_id),)).fetchone()
    if not row:
        return None
    return Lead(
        id=row["id"],
        name=row["name"],
        mobile=row["mobile"],
        service=row["service"],
        budget=row["budget"],
        city=row["city"],
        call_status=CallStatus(row["call_status"]),
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def list_leads() -> list[Lead]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM leads ORDER BY created_at DESC").fetchall()
    return [
        Lead(
            id=r["id"],
            name=r["name"],
            mobile=r["mobile"],
            service=r["service"],
            budget=r["budget"],
            city=r["city"],
            call_status=CallStatus(r["call_status"]),
            created_at=datetime.fromisoformat(r["created_at"]),
        )
        for r in rows
    ]


def _row_to_result(row: sqlite3.Row) -> CallResult:
    return CallResult(
        id=row["id"],
        lead_id=row["lead_id"],
        name=row["name"],
        mobile=row["mobile"],
        call_status=CallStatus(row["call_status"]),
        duration_seconds=row["duration_seconds"],
        interest=InterestLevel(row["interest"]),
        score=row["score"],
        next_action=row["next_action"],
        transcript=row["transcript"],
        notes=row["notes"],
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def upsert_call_result(result: CallResult) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO call_results
                (id, lead_id, name, mobile, call_status, duration_seconds, interest, score, next_action, transcript, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                call_status=excluded.call_status,
                duration_seconds=excluded.duration_seconds,
                interest=excluded.interest,
                score=excluded.score,
                next_action=excluded.next_action,
                transcript=excluded.transcript,
                notes=excluded.notes,
                updated_at=excluded.updated_at
            """,
            (
                str(result.id),
                str(result.lead_id),
                result.name,
                result.mobile,
                result.call_status.value,
                result.duration_seconds,
                result.interest.value,
                result.score,
                result.next_action,
                result.transcript,
                result.notes,
                result.updated_at.isoformat(),
            ),
        )
        conn.execute(
            "UPDATE leads SET call_status = ? WHERE id = ?",
            (result.call_status.value, str(result.lead_id)),
        )


def get_call_result(lead_id: UUID) -> CallResult | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM call_results WHERE lead_id = ?", (str(lead_id),)).fetchone()
    return _row_to_result(row) if row else None


def list_call_results(status: CallStatus | None = None) -> list[CallResult]:
    with _connect() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM call_results WHERE call_status = ? ORDER BY updated_at DESC",
                (status.value,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM call_results ORDER BY updated_at DESC").fetchall()
    return [_row_to_result(r) for r in rows]
