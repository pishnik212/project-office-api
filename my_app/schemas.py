from datetime import datetime
from typing import Union

from pydantic import BaseModel

class QuestionBase(BaseModel):
    id: int
    id_category: int
    question: str
    answer: str
    popularity: int
    date: datetime


class QuestionCreate(QuestionBase):
    id: int
    id_category: int
    question: str
    answer: str
    popularity: int
    date: datetime


class Question(QuestionBase):
    id: int
    id_category: int
    question: str
    answer: str
    popularity: int
    date: datetime

    class Config:
        orm_mode = True