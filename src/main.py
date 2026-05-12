from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .services.knowledge_loader import knowledge
from .routes.character import router as character_router
from .routes.validation import router as validation_router
from .routes.knowledge import router as knowledge_router
from .routes.chat import router as chat_router
from .routes.export import router as export_router

app = FastAPI(title="forBetterTRPG", version="0.2.0", description="狩魂者TRPG AI建卡器后端")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(character_router)
app.include_router(validation_router)
app.include_router(knowledge_router)
app.include_router(chat_router)
app.include_router(export_router)


@app.on_event("startup")
def startup():
    knowledge.load()


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.2.0"}
