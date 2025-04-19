"""User Entity"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ...common.base_entity import Base


class User(Base):
    """
    User class
    """

    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
