# services/session.py
from contextlib import contextmanager
from typing import Iterator
from db import SessionLocal

@contextmanager
def get_session() -> Iterator:
    """
    Context-managed SQLAlchemy session that:
    - Commits on success
    - Rolls back on exception
    - Closes always
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
