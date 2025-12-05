from sqlmodel import Session, select

from ..database import get_engine
from ..db_models import SessionLog
from ..models import SessionLogRequest, SessionLogResponse, SessionAggregateResponse


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


def list_sessions(limit: int = 20) -> list[SessionLogResponse]:
    engine = get_engine()
    with Session(engine) as session:
        rows = session.exec(select(SessionLog).order_by(SessionLog.created_at.desc()).limit(limit)).all()
        return [
            SessionLogResponse(
                id=row.id,
                learner_name=row.learner_name,
                accuracy=row.accuracy,
                focus_score=row.focus_score,
                pace_wpm=row.pace_wpm,
                level=row.level,
                note=row.note,
                created_at=row.created_at,
            )
            for row in rows
        ]


def learner_stats(name: str) -> SessionAggregateResponse:
    engine = get_engine()
    with Session(engine) as session:
        rows = session.exec(select(SessionLog).where(SessionLog.learner_name == name).order_by(SessionLog.created_at.desc())).all()
        if not rows:
            return SessionAggregateResponse(
                learner_name=name,
                count=0,
                avg_accuracy=0.0,
                avg_focus=0.0,
                avg_pace_wpm=0.0,
                last_level="A1",
            )
        count = len(rows)
        avg_accuracy = sum(r.accuracy for r in rows) / count
        avg_focus = sum(r.focus_score for r in rows) / count
        avg_pace = sum(r.pace_wpm for r in rows) / count
        last_level = rows[0].level
        return SessionAggregateResponse(
            learner_name=name,
            count=count,
            avg_accuracy=round(avg_accuracy, 2),
            avg_focus=round(avg_focus, 2),
            avg_pace_wpm=round(avg_pace, 1),
            last_level=last_level,
        )
