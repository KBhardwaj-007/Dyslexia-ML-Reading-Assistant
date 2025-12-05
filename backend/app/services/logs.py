from sqlmodel import Session

from ..database import get_engine
from ..db_models import SessionLog
from ..models import SessionLogRequest, SessionLogResponse


def log_session(payload: SessionLogRequest) -> SessionLogResponse:
    engine = get_engine()
    with Session(engine) as session:
        record = SessionLog(
            learner_name=payload.learner_name,
            accuracy=payload.accuracy,
            focus_score=payload.focus_score,
            pace_wpm=payload.pace_wpm,
            level=payload.level,
            note=payload.note or "",
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return SessionLogResponse(
            id=record.id,
            learner_name=record.learner_name,
            accuracy=record.accuracy,
            focus_score=record.focus_score,
            pace_wpm=record.pace_wpm,
            level=record.level,
            note=record.note,
            created_at=record.created_at,
        )
