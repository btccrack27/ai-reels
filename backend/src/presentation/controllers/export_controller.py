from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from io import BytesIO
from ...application.dto.content_dto import ExportPDFRequestDTO, ExportPDFResponseDTO
from ...application.use_cases.export_pdf_use_case import ExportPDFUseCase
from ..middlewares import get_current_user
from ..dependencies import get_export_pdf_use_case


router = APIRouter(prefix="/api/export", tags=["export"])


# ============== Endpoints ==============

@router.get("/pdf/{content_id}")
async def export_pdf(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    use_case: ExportPDFUseCase = Depends(get_export_pdf_use_case)
):
    """
    Exportiert Content als PDF.

    Requires: Authentication
    Rate-Limited: Ja (PDF Export hat eigenes monatliches Limit)

    Supported Content Types:
    - Hook (10 Hooks)
    - Script (Szenen + CTA)
    - Shotlist (3-4 Shots)
    - Voiceover (Text)
    - Caption (Text + Hashtags)
    - B-Roll (10 Ideas)
    - Calendar (30-Tage Plan)

    Returns:
    - PDF File (application/pdf)
    - Content-Disposition: attachment mit Filename

    Errors:
    - 401: Not authenticated
    - 403: Content gehört nicht diesem User
    - 404: Content nicht gefunden
    - 429: PDF-Limit erreicht
    - 500: PDF Generation Error
    """
    try:
        dto = ExportPDFRequestDTO(
            user_id=current_user["user_id"],
            content_id=content_id
        )
        result = await use_case.execute(dto)

        # PDF als StreamingResponse zurückgeben
        pdf_stream = BytesIO(result.pdf_bytes)

        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{result.filename}"'
            }
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim PDF-Export: {str(e)}"
        )
