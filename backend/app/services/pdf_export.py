"""
PDF export — converts the Excel informe to PDF using LibreOffice headless.

Requires LibreOffice installed:
  macOS:  brew install --cask libreoffice
  Linux:  apt-get install libreoffice-calc
  Docker: RUN apt-get install -y libreoffice-calc
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.informe import InformeSemanal
from app.services.excel_export import generate_informe_excel


def _find_soffice() -> str:
    """Find the LibreOffice soffice binary."""
    # macOS (Homebrew cask)
    mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if Path(mac_path).exists():
        return mac_path

    # Linux / Docker / Homebrew linked
    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    raise RuntimeError(
        "LibreOffice no encontrado. Instalar con: brew install --cask libreoffice"
    )


def generate_informe_pdf(
    db: Session,
    informe: InformeSemanal,
    upload_dir: str | None = None,
) -> BytesIO:
    """
    Generate a PDF for the given InformeSemanal.

    1. Generate Excel using existing engine
    2. Write to temp file
    3. Convert to PDF via LibreOffice headless
    4. Return PDF as BytesIO
    """
    soffice = _find_soffice()

    # Generate Excel
    excel_buffer = generate_informe_excel(db, informe, upload_dir)

    tmpdir = tempfile.mkdtemp(prefix="informe_pdf_")
    try:
        # Write xlsx to temp file
        xlsx_path = Path(tmpdir) / f"informe_{informe.id}.xlsx"
        xlsx_path.write_bytes(excel_buffer.getvalue())

        # Convert to PDF
        result = subprocess.run(
            [
                soffice,
                "--headless",
                "--calc",
                "--convert-to", "pdf",
                "--outdir", tmpdir,
                str(xlsx_path),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"LibreOffice falló al convertir: {result.stderr or result.stdout}"
            )

        # Read resulting PDF
        pdf_path = xlsx_path.with_suffix(".pdf")
        if not pdf_path.exists():
            raise RuntimeError("LibreOffice no generó el archivo PDF")

        pdf_buffer = BytesIO(pdf_path.read_bytes())
        return pdf_buffer

    finally:
        # Cleanup temp directory
        shutil.rmtree(tmpdir, ignore_errors=True)
