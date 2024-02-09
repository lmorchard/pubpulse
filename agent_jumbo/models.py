from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, JSON
from sqlalchemy import TypeDecorator

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