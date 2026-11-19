
from datetime import datetime

from sqlalchemy import (
    Integer, String, Text, DateTime, Boolean,
    Enum, ForeignKey, Table, Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


# Проміжна таблиця для зв'язку багато-до-багатьох
post_tags = db.Table(
    "post_tags",
    Column(
        "post_id",
        Integer,
        ForeignKey("posts.id"),
        primary_key=True
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id"),
        primary_key=True
    )
)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    posted: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        Enum(
            "news",
            "publication",
            "tech",
            "other",
            name="post_category"
        ),
        nullable=False,
        default="other"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # Зв'язок один-до-багатьох з користувачем
    user: Mapped["User | None"] = relationship(
        back_populates="posts"
    )

    # Зв'язок багато-до-багатьох з тегами
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    # Зв'язок багато-до-багатьох з дописами
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
