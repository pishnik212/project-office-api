from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = crud.get_question_by_text(db, text=question.question)
    if db_question:
        raise HTTPException(status_code=400, detail="Question already registered")
    return crud.create_question(db=db, question=question)


@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.get("/questions/", response_model=list[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = crud.get_questions(db, skip=skip, limit=limit)
    return questions




@app.post("/questions_check/")
def question_check(new_question: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_question = crud.get_question_by_text(db, text=new_question)
    if db_question:
        return db_question
    else:
        # questions = crud.get_questions(db, skip=skip, limit=limit)
        # return questions
        return None

@app.post("/get_answer/")
def get_answer(first_qustion, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, sklearn=None):
    import spacy
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    nlp = spacy.load('ru_core_news_lg')

    # questions.append(question)
    questions_ = crud.get_questions(db, skip=skip, limit=limit)
    questions = list()
    answers = list()
    ids = list()
    for i in questions_:
        q1 = i.question
        questions.append(q1)
        a1 = i.answer
        answers.append(a1)
        id = i.id
        ids.append(id)

    if first_qustion in questions:
        q0 = crud.get_question_by_text(db, first_qustion)
        return q0
    else:

        questions.append(first_qustion)
        n = len(questions)
        parsed = [None] * n
        tx2 = [None] * n

        for i in range(n):
            parsed[i] = nlp(questions[i])
            tx2[i] = " ".join([token.lemma_ for token in parsed[i] if token.pos_ != 'PUNCT'])

        vectorizer = CountVectorizer()
        tk = vectorizer.fit_transform(tx2)

        tk_tfidf = TfidfTransformer().fit_transform(tk)

        # Считаем косинусные расстояния между текстами
        tstat_tfidf = cosine_similarity(tk_tfidf, tk_tfidf)

        max_index = np.argmax(tstat_tfidf[n - 1, 0:(n - 2)])
        que = questions[max_index]
        res_question = crud.get_question_by_text(db, que)

        return res_question

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}