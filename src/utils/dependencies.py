"""
This file handles utility functions for database session management.
"""

from ..config.db import session_factory


async def get_db():
    """
    Yields a database session.
    """
    db = session_factory()
    try:
        yield db
    finally:
        await db.close()
