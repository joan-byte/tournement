from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.exportacion_service import ExportacionService
from typing import Literal

router = APIRouter()

@router.get("/ranking/{campeonato_id}")
def exportar_ranking(
    campeonato_id: int,
    formato: Literal["pdf", "excel"],
    db: Session = Depends(get_db)
):
    """
    Exportar ranking del campeonato en PDF o Excel.
    """
    service = ExportacionService(db)
    if formato == "pdf":
        content, filename = service.exportar_ranking_pdf(campeonato_id)
        media_type = "application/pdf"
    else:
        content, filename = service.exportar_ranking_excel(campeonato_id)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/resultados/{campeonato_id}")
def exportar_resultados(
    campeonato_id: int,
    formato: Literal["pdf", "excel"],
    db: Session = Depends(get_db)
):
    """
    Exportar resultados del campeonato en PDF o Excel.
    """
    service = ExportacionService(db)
    if formato == "pdf":
        content, filename = service.exportar_resultados_pdf(campeonato_id)
        media_type = "application/pdf"
    else:
        content, filename = service.exportar_resultados_excel(campeonato_id)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    ) 