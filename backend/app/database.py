from functools import lru_cache
from sqlmodel import SQLModel, create_engine

<<<<<<< HEAD
DATABASE_URL = "sqlite:///./app.db"
=======
from .config import get_settings
>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)


@lru_cache
def get_engine():
<<<<<<< HEAD
    return create_engine(DATABASE_URL, echo=False)
=======
    settings = get_settings()
    return create_engine(settings.database_url, echo=False)
>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
