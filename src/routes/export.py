from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response, JSONResponse

from ..services.export_service import export_json, export_excel, import_json
from ..models.character import CharacterCard
from ..models.creation_state import CreationSession
from ..routes.character import sessions

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/json/{session_id}")
def export_session_json(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    data = export_json(session.character)
    return JSONResponse(
        content=data,
        headers={"Content-Disposition": f"attachment; filename=character_{session_id[:8]}.json"},
    )


@router.post("/excel/{session_id}")
def export_session_excel(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        excel_bytes = export_excel(session.character)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=character_{session_id[:8]}.xlsx"},
    )


@router.post("/import/json")
async def import_character_json(file: UploadFile = File(...)):
    content = await file.read()
    try:
        data = __import__("json").loads(content)
        card = import_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid character JSON: {e}")

    session = CreationSession()
    session.character = card
    session.current_step = 6
    session.completed_steps = [1, 2, 3, 4, 5, 6]
    sessions[session.id] = session
    return {"session_id": session.id, "character": card.model_dump()}
