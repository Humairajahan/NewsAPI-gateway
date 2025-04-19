"""
Base Entity
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, Identity, DateTime
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    """
    Base class
    """

    id = mapped_column(Integer, Identity(start=1000, cycle=True), primary_key=True)
    uuid = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
