from fastapi import APIRouter

from ..models import SessionLogRequest, SessionLogResponse
from ..services.logs import log_session

router = APIRouter()


@router.post("/log", response_model=SessionLogResponse)
async def log_session_endpoint(payload: SessionLogRequest) -> SessionLogResponse:
    return log_session(payload)
