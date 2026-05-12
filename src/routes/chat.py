from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import json

from ..models.enums import CreationStep
from ..services.ai_service import chat_stream, get_contextual_tip

router = APIRouter(prefix="/api/chat", tags=["chat"])

chat_histories: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str
    step: int = 1
    model: str = "deepseek-v4-flash"


@router.post("")
async def chat(request: ChatRequest):
    step = CreationStep(request.step)
    history = chat_histories.setdefault(request.session_id, [])
    history.append({"role": "user", "content": request.message})

    async def event_generator():
        full_response = ""
        async for token in chat_stream(request.message, step, history, request.model):
            full_response += token
            yield {"data": json.dumps(token, ensure_ascii=False)}
        history.append({"role": "assistant", "content": full_response})
        yield {"data": "[DONE]"}

    return EventSourceResponse(event_generator())


@router.get("/tip/{step}")
def get_tip(step: int):
    creation_step = CreationStep(step)
    return {"tip": get_contextual_tip(creation_step)}


@router.delete("/history/{session_id}")
def clear_history(session_id: str):
    chat_histories.pop(session_id, None)
    return {"status": "cleared"}
