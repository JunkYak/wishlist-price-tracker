# db/base.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# --- DB connection string ---
# Default: sqlite file named wishlist.db in project root.
# You can override with env var WISHLIST_DATABASE_URL for testing or prod.
DATABASE_URL = os.getenv("WISHLIST_DATABASE_URL", "sqlite:///wishlist.db")

# --- Engine ---
# create_engine returns an Engine which manages connections.
# echo=True prints SQL statements (helpful during development).
# future=True opts into SQLAlchemy 2.0 style behavior.
engine = create_engine(DATABASE_URL, echo=True, future=True)

# --- Session factory ---
# SessionLocal() will give you a session bound to the engine.
# autoflush=False and autocommit=False are explicit dev-friendly defaults.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# --- Declarative Base ---
# All ORM models inherit from this Base class.
# DeclarativeBase is SQLAlchemy's modern base class (2.0-style).
class Base(DeclarativeBase):
    pass
