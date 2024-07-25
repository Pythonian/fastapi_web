#!/usr/bin/env python3
"""The database module"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from api.utils.settings import BASE_DIR, settings


def get_db_engine(test_mode: bool = False):  # type: ignore
    """Create a SQLAlchemy engine instance.

    Args:
        test_mode (bool): If True, use a SQLite database for testing purposes.

    Returns:
        Engine: SQLAlchemy engine instance.
    """
    if settings.DB_TYPE == "sqlite" or test_mode:
        # If the database type is SQLite or we are in test mode, use a SQLite database
        BASE_PATH = f"sqlite:///{BASE_DIR}"
        DATABASE_URL = BASE_PATH + ("/test.db" if test_mode else "/db.sqlite3")
    else:
        # For other database types, use the provided DATABASE_URL
        DATABASE_URL = settings.DB_URL

    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
        if settings.DB_TYPE == "sqlite"
        else {},
    )


# Create an engine instance
engine = get_db_engine()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a configured "scoped_session" factory
db_session = scoped_session(SessionLocal)

# Create a base class for declarative class definitions
Base = declarative_base()


def create_database():
    """Create all tables in the database."""
    return Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session.

    This function provides a context manager for database sessions, ensuring that
    each session is properly closed after use.

    Yields:
        Session: SQLAlchemy session instance.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()
