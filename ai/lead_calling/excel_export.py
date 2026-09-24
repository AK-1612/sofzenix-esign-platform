"""Export the call-results table back to an .xlsx file for download/reporting."""

from __future__ import annotations

import io

from openpyxl import Workbook
from openpyxl.styles import Font

from .schemas import CallResult

COLUMNS = ["Name", "Mobile", "Call Status", "Duration", "Interest", "Score", "Next Action"]


def export_call_results(results: list[CallResult]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Call Results"

    sheet.append(COLUMNS)
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    for result in results:
        sheet.append(
            [
                result.name,
                result.mobile,
                result.call_status.value,
                result.duration_display,
                result.interest.value,
                result.score if result.score is not None else "—",
                result.next_action,
            ]
        )

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = max(12, length + 2)

    buffer = io.BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
