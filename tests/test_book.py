import os
import pytest
import schemas
from jose import jwt

from config import settings
db_url = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.TESTING_DB_HOST}:{settings.TESTING_DB_PORT}/{settings.TESTING_DB_NAME}'
print(db_url)


def test_add_book(authorized_client):

    res = authorized_client.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())
    assert res.json().get('Title') == 'cc'
    assert res.status_code == 200


def test_add_book_with_missing_field(authorized_client):
    res = authorized_client.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
    })
    print(res.json())
    assert res.status_code == 422


def test_add_book_when_book_exists(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())
    assert res.json() == 'Book already exists'
    assert res.status_code == 200


def test_delete_book(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/delete-book/cc')
    assert res.json().get('message') == 'Book deleted successfully'
    assert res.status_code == 200


def test_delete_book_when_book_does_not_exist(authorized_client):
    res = authorized_client.get('/delete-book/cc')
    assert res.json().get('error') == 'Book not found'
    assert res.status_code == 200


def test_delete_book_when_user_is_not_admin(authorized_client_non_admin):
    res = authorized_client_non_admin.get('/delete-book/cc')
    assert res.json().get('error') == 'Only Admin can delete books'
    assert res.status_code == 200


def test_add_book_when_user_is_not_admin(authorized_client_non_admin):
    res = authorized_client_non_admin.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
        "Description": "sample book.",
        "CoverImage": "book.jpg",
        "Available": "true",
        "RentingPeriod": 20,
        "PricePerDay": 82
    })
    print(res.json())

    assert res.status_code == 200


def test_add_book_when_user_is_not_admin(authorized_client_non_admin):
    res = authorized_client_non_admin.post('/add-book', json={
        "Title": "cc",
        "Author": "author3",
        "Genre": "h",
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


def test_book_list_when_no_books(authorized_client):
    res = authorized_client.get('/book-list')
    assert res.status_code == 200


def test_book_details(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/books-detail/cc')
    assert res.status_code == 200


def test_book_details_when_book_does_not_exist(authorized_client):
    res = authorized_client.get('/books-detail/cc')
    assert res.json().get('message') == 'Book not found'
