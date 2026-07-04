"""
Module 6: Drift Report Generation
Generates downloadable CSV and Excel drift reports.
"""

import pandas as pd
import io
from typing import Tuple


REPORT_COLUMNS = [
    "feature",
    "feature_type",
    "method",
    "statistic",
    "p_value",
    "psi",
    "drift_status",
    "psi_status",
]


def build_report(drift_df: pd.DataFrame) -> pd.DataFrame:
    """
    Select and rename columns to build a clean drift report DataFrame.
    """
    available = [c for c in REPORT_COLUMNS if c in drift_df.columns]
    report = drift_df[available].copy()

    # Rename for readability
    report.columns = [c.replace("_", " ").title() for c in report.columns]
    return report


def to_csv_bytes(report_df: pd.DataFrame) -> bytes:
    """Convert drift report DataFrame to CSV bytes for download."""
    return report_df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(report_df: pd.DataFrame) -> bytes:
    """Convert drift report DataFrame to Excel bytes for download."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        report_df.to_excel(writer, sheet_name="Drift Report", index=False)

        # Auto-adjust column widths
        ws = writer.sheets["Drift Report"]
        for col_cells in ws.columns:
            max_len = max(
                len(str(cell.value)) if cell.value else 0 for cell in col_cells
            )
            ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 40)

    buffer.seek(0)
    return buffer.read()


def save_report_to_disk(report_df: pd.DataFrame,
                        csv_path: str = "reports/drift_report.csv",
                        excel_path: str = "reports/drift_report.xlsx") -> Tuple[str, str]:
    """
    Save the report to CSV and Excel files on disk.
    Returns the paths of saved files.
    """
    report_df.to_csv(csv_path, index=False)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        report_df.to_excel(writer, sheet_name="Drift Report", index=False)

    return csv_path, excel_path
