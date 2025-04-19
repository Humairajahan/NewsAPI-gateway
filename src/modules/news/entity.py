"""News Entity"""

from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from ...common.base_entity import Base


class NewsEntity(Base):
    """
    News entity class
    """

    __tablename__ = "news"

    author: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    urlToImage: Mapped[str] = mapped_column(Text)
    publishedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    content: Mapped[str] = mapped_column(Text)
