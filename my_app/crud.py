from sqlalchemy.orm import Session

from . import models, schemas


def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_question_by_text(db: Session, text: str):
    return db.query(models.Question).filter(models.Question.question == text).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(question=question.question, answer=question.answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question