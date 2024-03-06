from __future__ import annotations

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    url=settings.postgresql.url, pool_recycle=1800, pool_size=100, max_overflow=50
)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
