import os
import pytest
import schemas
from jose import jwt
from config import settings

def test_root(client):
    res = client.get('/')
    assert res.status_code == 200


def test_register_user(client):
    res = client.post('/register', json={
        "firstname": "e",
        "lastname": "e",
        "email": "e",
        "number": 1234567890,
        "profile": "e",
        "password": "e",
        "isAdmin": "false"
    })
    assert res.json().get('email') == 'e'
    assert res.status_code == 200


def test_register_user_with_missing_field(client):
    res = client.post('/register', json={
        "firstname": "e",
        "lastname": "e",
        "email": "e",
        "number": 1234567890,
        "profile": "e",
        "password": "e",
    })
    assert res.status_code == 422


def test_register_user_when_user_exists(client, test_register_for_login):

    res = client.post('/register', json={
        "firstname": "e",
        "lastname": "e",
        "email": "e",
        "number": 1234567890,
        "profile": "e",
        "password": "e",
        "isAdmin": "false"
    })

    assert res.json() == 'User already exists'
    assert res.status_code == 200


def test_login_user(client, test_register_for_login):
    res = client.post('/login', data={
        "username": test_register_for_login['email'],
        "password": test_register_for_login['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY , algorithms=[settings.ALGORITHM])
    id: str = str(payload.get("user_id"))
    assert id == str(test_register_for_login['id'])
    assert res.status_code == 200


def test_login_user_with_wrong_password(client, test_register_for_login):
    res = client.post('/login', data={
        "username": test_register_for_login['email'],
        "password": "wrong password"
    })
    assert res.status_code == 403
    assert res.json() == {'detail': 'Invalid credentials'}


def test_login_user_with_wrong_email(client, test_register_for_login):
    res = client.post('/login', data={
        "username": "wrong email",
        "password": test_register_for_login['password']
    })
    assert res.status_code == 403
    assert res.json() == {'detail': 'Invalid credentials'}


def test_login_with_missing_field(client, test_register_for_login):
    res = client.post('/login', data={
        "username": test_register_for_login['email'],
    })
    assert res.status_code == 422
