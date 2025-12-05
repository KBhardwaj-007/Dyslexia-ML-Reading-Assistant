from functools import lru_cache
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./app.db"


@lru_cache
def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
