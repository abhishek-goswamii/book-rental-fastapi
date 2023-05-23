from fastapi.testclient import TestClient
from main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from database import get_db, Base
from dotenv import load_dotenv, dotenv_values
load_dotenv()

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")

db_url = f'postgresql://{db_username}:{db_password}@localhost/fastapi_testing'

engine = create_engine(db_url)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overide_get_db


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_register_for_login(client):
    user_data = client.post('/register', json={
        "firstname": "e",
        "lastname": "e",
        "email": "e",
        "number": 1234567890,
        "profile": "e",
        "password": "e",
        "isAdmin": "false"
    })
    assert user_data.json().get('email') == 'e'
    assert user_data.status_code == 200
    new_user = user_data.json()
    new_user['password'] = 'e'
    return new_user