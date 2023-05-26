from fastapi.testclient import TestClient
from main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from database import get_db, Base
from config import settings


db_url = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.Testing_DB_PORT}/{settings.TESTING_DB_NAME}'
print(db_url)

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
        "isAdmin": "true"
    })
    assert user_data.json().get('email') == 'e'
    assert user_data.status_code == 200
    new_user = user_data.json()
    new_user['password'] = 'e'
    return new_user


@pytest.fixture()
def token(test_register_for_login):
    return create_access_token({"user_id": test_register_for_login['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_register_non_admin_user(client):
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


@pytest.fixture()
def token_non_admin(test_register_non_admin_user):
    return create_access_token({"user_id": test_register_non_admin_user['id']})


@pytest.fixture()
def authorized_client_non_admin(client, token_non_admin):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_non_admin}"
    }
    return client


@pytest.fixture()
def test_add_book_fixture(client):

    res = client.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })

    assert res.json().get('Title') == 'cc'
    assert res.status_code == 200
    return res.json()

@pytest.fixture()
def test_add_genre_fixture(client):
            
    res = client.post('/add-genre', json={
                "GenreName": "genre1"
            })
    
    assert res.json().get('GenreName') == 'genre1'
    assert res.status_code == 200
    return res.json()

@pytest.fixture()
def test_rent_book_fixture(authorized_client):
    
    res = authorized_client.post('/rentbook', json={
        "BookName": "cc",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
        "ReturnDate": "2023-05-28"
    })
    assert res.status_code == 200
    assert res.json().get('message') == "Book rented successfully"
    