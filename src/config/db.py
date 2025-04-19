"""
Module for database engine setup and async session management.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import DB_URL


def get_engine():
    """
    Returns a new async SQLAlchemy engine.
    """
    return create_async_engine(DB_URL)


def session_factory():
    """
    Creates an async DB session tied to the current event loop.
    """
    # Get current event loop
    loop = asyncio.get_event_loop()

    # Get or create an engine for this loop
    if not hasattr(loop, "sqlalchemy_engine"):
        loop.sqlalchemy_engine = get_engine()

    # Create a session bound to this loop's engine
    async_session = sessionmaker(
        loop.sqlalchemy_engine, class_=AsyncSession, expire_on_commit=False
    )

    return async_session()
