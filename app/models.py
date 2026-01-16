from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, false
from sqlalchemy.orm import relationship, Mapped, mapped_column, Relationship
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

    comments = relationship(
        "Comment",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
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

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan",)


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


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    parent_id = Column(
        Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )

    parent = relationship("Comment", back_populates="comments_arr", remote_side=[id])

    comments_arr = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
