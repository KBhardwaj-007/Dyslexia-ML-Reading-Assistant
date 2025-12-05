from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import speech, attention, adapt, assist, mentor, sessions
from .database import init_db

app = FastAPI(
    title="Dyslexia ML Reading Assistant API",
    version="0.1.0",
    description="Prototype API with modules for speech analysis, attention sensing, adaptive difficulty, multisensory cues, and mentor persona.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(speech.router, prefix="/listen", tags=["speech"])
app.include_router(attention.router, prefix="/observe", tags=["attention"])
app.include_router(adapt.router, prefix="/adapt", tags=["adaptation"])
app.include_router(assist.router, prefix="/assist", tags=["assist"])
app.include_router(mentor.router, prefix="/mentor", tags=["mentor"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])


@app.get("/")
async def root() -> dict:
    return {
        "message": "Dyslexia ML Reading Assistant API",
        "docs": "/docs",
        "modules": ["listen", "observe", "adapt", "assist", "mentor", "sessions"],
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.on_event("startup")
def _startup() -> None:
    init_db()
