import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, JSON, DateTime
from sqlalchemy import TypeDecorator, UniqueConstraint
from pgvector.sqlalchemy import Vector

from typing import Optional


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


class MyJsonType(TypeDecorator):
    impl = JSON

    cache_ok = True

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)


class Status(db.Model):
    __tablename__ = "statuses"
    url: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[Optional[dict|list]] = mapped_column(type_=JSON)
    ingested_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class StatusEmbedding(db.Model):
    __tablename__ = "status_embeddings"
    url: Mapped[str] = mapped_column(primary_key=True)
    embedding = mapped_column(Vector(384))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
