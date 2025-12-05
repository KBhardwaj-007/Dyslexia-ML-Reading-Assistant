from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class SessionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    learner_name: str = Field(index=True)
    accuracy: float
    focus_score: float
    pace_wpm: float
    level: str
    note: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
