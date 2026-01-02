from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Enum as SQLEnum

from app.database import Base
from app.schemas import Role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    profile_pic = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="role_enum"),
        default=Role.USER,
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="posts",
        passive_deletes=True,
    )


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )
