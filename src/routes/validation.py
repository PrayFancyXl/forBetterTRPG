from fastapi import APIRouter, HTTPException

from ..models.enums import CreationStep
from ..rule_engine.engine import validate_step
from .character import sessions

router = APIRouter(prefix="/api/validation", tags=["validation"])


@router.post("/{session_id}")
def validate_session_step(session_id: str, step: int = None):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    target_step = CreationStep(step) if step else session.current_step
    result = validate_step(session.character, target_step)
    return result
