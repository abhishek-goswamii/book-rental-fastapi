import os
import pytest
import schemas
from jose import jwt
from dotenv import load_dotenv, dotenv_values
load_dotenv()


def test_add_book(authorized_client):
    res = authorized_client.post('/add-book', json={
        "Title": "c7",
        "Author": "author3",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())
    assert res.json().get('Title') == 'c7'
    assert res.status_code == 200

def test_add_book_with_missing_field(authorized_client):
    res = authorized_client.post('/add-book', json={
        "Title": "c7",
        "Author": "author3",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
    })
    print(res.json())
    assert res.status_code == 422

def test_add_book_when_book_exists(authorized_client,test_add_book_fixture):
    res = authorized_client.post('/add-book', json={
        "Title": "c7",
        "Author": "author3",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())
    assert res.json() == 'Book already exists'
    assert res.status_code == 200

def test_add_book_when_user_is_not_admin(authorized_client_non_admin):
    res = authorized_client_non_admin.post('/add-book', json={
        "Title": "c7",
        "Author": "author3",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())
   
    assert res.status_code == 200


def test_book_list(authorized_client):
    res = authorized_client.get('/book-list')
    assert res.status_code == 200
