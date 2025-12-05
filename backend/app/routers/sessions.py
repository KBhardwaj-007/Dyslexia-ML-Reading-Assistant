from fastapi import APIRouter

from ..models import SessionLogRequest, SessionLogResponse, SessionAggregateResponse
from ..services.logs import log_session, list_sessions, learner_stats

router = APIRouter()


@router.post("/log", response_model=SessionLogResponse)
async def log_session_endpoint(payload: SessionLogRequest) -> SessionLogResponse:
    return log_session(payload)


@router.get("/recent", response_model=list[SessionLogResponse])
async def recent_sessions(limit: int = 20) -> list[SessionLogResponse]:
    return list_sessions(limit=limit)


@router.get("/learner/{name}", response_model=SessionAggregateResponse)
async def learner_summary(name: str) -> SessionAggregateResponse:
    return learner_stats(name)
