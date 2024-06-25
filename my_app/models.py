import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    id_category = Column(Integer, index=True, default=1)
    question = Column(String, index=True)
    answer = Column(String, index=True)
    popularity = Column(Integer, index=True, default=1)
    date = Column(TIMESTAMP, index=True, default=datetime.datetime.utcnow)
