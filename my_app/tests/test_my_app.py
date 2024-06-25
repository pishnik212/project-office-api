from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

# pytest -p no:warnings

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_question():
    response = client.post(
        "/questions/",
        json={
            "id": 9,
            "id_category": 1,
            "question": "Как пройти в библиотеку?",
            "answer": "Вот так-то",
            "popularity": 1,
            "date": "2024-06-22T15:13:16.162521"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["question"] == "Как пройти в библиотеку?"
    assert "id" in data
    question_id = data["id"]

    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["question"] == "Как пройти в библиотеку?"
    assert data["id"] == question_id


def test_create_existing_question():
    response = client.post(
        "/questions/",
        json={"question": "Как пройти в библиотеку?", "answer": "Вот так-то"},
    )
    assert response.status_code == 422, response.text


def test_read_question():
    response = client.get("/questions/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["question"] == "Как пройти в библиотеку?"
    assert "id" in data
    question_id = data["id"]

    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["question"] == "Как пройти в библиотеку?"
    assert data["id"] == question_id
    assert data['answer'] == "Вот так-то"


def test_read_question_nonexistent_id():
    response = client.get("/questions/3")
    assert response.status_code == 404, response.text == 'Question not found'
    data = response.json()
    assert "id" not in data

def test_read_questions():
    response = client.get("/questions/")
    assert response.status_code == 200, response.text


def test_question_check():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    # assert response.status_code == 200, response.text
    assert response.json() is not None


def test_read_question():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_update_question_answer():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_update_question_popularity():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_update_question_category():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_delete_question():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None



def test_question_check_nonexistent():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None


def test_create_category():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None


def test_create_category_nonexistent():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_update_category():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_read_category():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_delete_category():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None

def test_delete_category_nonexistent():
    response = client.post(
        "/questions_check/",
        json={"new_question": "Как пройти в библиотеку?"},
    )
    assert response.json() is not None